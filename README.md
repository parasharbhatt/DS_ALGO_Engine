# AI-Driven Data Structures & Algorithms Orchestration Engine

An automated, asynchronous educational engine built with **FastAPI** and the **Google Gemini Pro SDK**. This ecosystem leverages two specialized AI agents that coordinate over an internal data protocol to synthesize standalone, interactive, single-file (`.html`) educational applications. Engineered for local development inside **VS Code** and cost-optimized serverless deployment on **Google Cloud Platform (GCP)**.

---

## 🏗️ Architecture & Agent Ecosystem

The workspace abstracts agent interactions into a structured, highly deterministic code-generation assembly line. By using strict data structures for inter-agent communication, token overhead is minimized.

### Types of Agents (Agent Development Kit - ADK)
1. **DS_Algo_PL_Selection_Agent (Strategic Planner)**: 
   * **Role**: Parses unstructured natural language user goals to establish metadata scope.
   * **Framework**: Integrates raw Gemini structured schema inference powered by Pydantic models.
   * **Execution Pattern**: Low-temperature (0.1) semantic parsing to enforce deterministic extraction.
2. **Web_Developer_Agent (Visual Systems Builder)**:
   * **Role**: Acts as a pure, zero-dependency visual and functional source-code generator.
   * **Framework**: High-context prompt blueprint compilation using Gemini models.
   * **Execution Pattern**: Generates single, self-contained HTML files containing native embedded CSS, Vanilla JavaScript state machine logic, and procedural inline SVGs.

### Inter-Agent Protocol (IAP)
The communication channel uses a strict, validated **JSON schema pipeline** powered by Pydantic models to passing data. This architecture eliminates multi-turn conversational token overhead:

```text
[User Prompt] ──> (Selection Agent) ──> [Validated JSON Protocol] ──> (Web Dev Agent) ──> [Self-Contained SPA]
```

#### Protocol Schema Specification
```json
{
  "\$defs": {},
  "properties": {
    "data_structure": { "title": "Data Structure", "type": "string" },
    "algorithm": { "title": "Algorithm", "type": "string" },
    "operations": { "items": { "type": "string" }, "title": "Operations", "type": "array" },
    "language": { "title": "Language", "type": "string" }
  },
  "required": ["data_structure", "algorithm", "operations", "language"],
  "type": "object"
}
```

---

## ⚡ MCP Server & Core Capabilities

The FastAPI backend functions as an autonomous **Model Context Protocol (MCP) Server**, providing a bridge between language models and local machine system runtimes.

### Agent Skills & Tools Matrix
* **File System Automation (`FS-WRITE`)**: Writes self-contained educational apps directly to the workspace filesystem (`generated_spas/`).
* **Visual Verification Engine (`VVE`)**: Programmatically scans output streams for required target tags (`<style>`, `<script>`, `<svg>`).
* **Algorithmic Analytics Builder (`AAB`)**: Injects precise runtime performance and big-O asymptotic tracking blocks into the UI.

---

## 🔒 Production Security Architecture

Designed for zero-trust local and public cloud host runtimes:
* **Directory Traversal Protection**: The application uses absolute path calculations (`os.path.abspath`) and prefix containment validations to prevent local file inclusion exploits when previewing assets via the dashboard.
* **Credential Isolation**: Runtime secrets (`GEMINI_API_KEY`) and infrastructure scopes (`PROJECT_ID`) are completely isolated within an untracked `.env` schema, ensuring deployment workflows remain scrubbed.
* **Container Layer Pruning**: A multi-stage Docker build strips out native C development tools and setup packages, producing an isolated runtime layer.

---

## 🚀 Cost-Effective Cloud Deployability (GCP Cloud Run)

The codebase features an automated cloud deployment loop optimized for Google Cloud Platform (GCP).

### Free-Tier Cloud Run Configuration
The platform deploys onto **Google Cloud Run** using fine-tuned auto-scaling boundaries:
* `min-instances=0`: The container scales down to absolute zero when idle, meaning **\$0.00 idle cost**.
* `max-instances=2`: Mitigates operational spending spikes and blocks denial-of-service pricing exploits.
* `cpu=1 / memory=512Mi`: Keeps execution profiles well within monthly GCP free-tier parameters.

### Local & Cloud Operational Matrix
```bash
# Execute local unit testing engine + Compile Timestamped PDF Report
python run_tests.py

# Boot regional development server locally
python run.py

# Trigger container compilation & secure cloud deployment
./deploy_gcp.sh
```
