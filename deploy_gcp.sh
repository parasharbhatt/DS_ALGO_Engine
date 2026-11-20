#!/bin/bash

# Exit script instantly if any command reports a non-zero termination state
set -e

# ==========================================
# PARSE CONFIGURATION VIA LOCAL .ENV FILE
# ==========================================
ENV_FILE=".env"

# Load configuration from the process environment or from a local .env file.
# Values are extracted without evaluating arbitrary shell expressions.
if [ -f "$ENV_FILE" ]; then
    ENV_PROJECT_ID=$(sed -n 's/^PROJECT_ID=//p' "$ENV_FILE" | tr -d '\r' | sed 's/^["'"'"']//;s/["'"'"']$//')
    ENV_GEMINI_API_KEY=$(sed -n 's/^GEMINI_API_KEY=//p' "$ENV_FILE" | tr -d '\r' | sed 's/^["'"'"']//;s/["'"'"']$//')
fi

PROJECT_ID="${PROJECT_ID:-$ENV_PROJECT_ID}"
GEMINI_API_KEY="${GEMINI_API_KEY:-$ENV_GEMINI_API_KEY}"
# Strict evaluation boundary guards
if [ -z "$PROJECT_ID" ]; then
    echo "ERROR: PROJECT_ID is missing. Set it in the environment or in $ENV_FILE."
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "ERROR: GEMINI_API_KEY is missing. Set it in the environment or in $ENV_FILE."
    exit 1
fi

# Shared immutable metadata constants
SERVICE_NAME="dsa-orchestration-engine"
REPO_NAME="$SERVICE_NAME-repo"
REGION="us-central1"                   # Highly cost-effective region with high availability

echo "====================================================="
echo " Starting Cost-Effective Deployment to GCP Cloud Run "
echo "====================================================="
echo "Targeting GCP Project ID: $PROJECT_ID"

# 1. Direct active terminal context to target project
gcloud config set project "$PROJECT_ID"

# 2. Enable foundational serverless orchestration APIs 
echo "Enabling necessary Cloud APIs..."
gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       artifactregistry.googleapis.com

# 3. Create a clean artifact management container repository if it doesn't exist
echo "Setting up secure container engine repository..."
gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --description="Docker repository for modern DSA App Engine" || true

# 4. Trigger cloud-native build compilation pipeline
echo "Uploading and building source context via Cloud Build..."
IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME:latest"
gcloud builds submit --tag "$IMAGE_URI" .

# 5. Deploy directly into zero-scaled Cloud Run instance using parameters parsed from .env
echo "Deploying container directly to Google Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --image="$IMAGE_URI" \
    --platform=managed \
    --region="$REGION" \
    --allow-unauthenticated \
    --set-env-vars="GEMINI_API_KEY=${GEMINI_API_KEY}" \
    --min-instances=0 \
    --max-instances=2 \
    --cpu=1 \
    --memory=512Mi

# ==========================================
# AUTOMATED CACHE PRUNING & COST MITIGATION
# ==========================================
echo ""
echo "====================================================="
echo " Running Automated Artifact Registry Cache Pruning   "
echo "====================================================="

# Target image package reference path
IMAGE_PACKAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME"

echo "Scanning for historical or untagged container builds in: $IMAGE_PACKAGE"

# Fetch all container digests sorted from oldest to newest, excluding the one currently tagged 'latest'
OLD_DIGESTS=$(gcloud artifacts docker images list "$IMAGE_PACKAGE" \
    --sort-by="CREATE_TIME" \
    --format="value(DIGEST)" \
    --filter="NOT tags=latest" 2>/dev/null || true)

if [ -z "$OLD_DIGESTS" ]; then
    echo "Storage is optimized! No old container variants or cached layers found to prune."
else
    echo "Found old or redundant container versions. Commencing safe storage cleanup..."
    for DIGEST in $OLD_DIGESTS; do
        echo "Deleting redundant build layer: $DIGEST"
        # Quietly and permanently delete the specific container digest layer without requiring interactive manual confirmations
        gcloud artifacts docker images delete "$IMAGE_PACKAGE@$DIGEST" --quiet --delete-tags
    done
    echo "Cache pruning completed. Only the active production container remains in storage."
fi

echo "====================================================="
echo " Deployment and Storage Pruning Successfully Complete!"
echo " Use the provided Cloud Run URL to access your App.  "
echo "====================================================="
