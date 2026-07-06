import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Mock environment safety keys
os.environ["GEMINI_API_KEY"] = "fake_testing_key"

from main import app
from app.selection import SelectionSchema

class TestDSAPipeline(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        self.test_prompt = "Build a bubble sort app in Java using arrays."

    def test_dashboard_route(self):
        """Verify the system root UI renders successfully."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("DSA App Orchestrator Engine", response.text)

    @patch("app.web_dev.run_web_developer_agent")
    @patch("app.selection.run_selection_agent")
    def test_end_to_end_generation(self, mock_selection, mock_web_dev):
        """Verify full agent pipeline, file creation, and strict HTML block content rules."""
        
        mock_selection.return_value = SelectionSchema(
            data_structure="Array",
            algorithm="Bubble Sort",
            operations=["Compare", "Swap"],
            language="Java"
        )
        
        # Simulated raw output from the generator containing all strict blocks
        mock_html_content = (
            "<!DOCTYPE html><html>"
            "<head><style>:root { --bg: #000; }</style></head>"
            "<body>"
            "<svg id='flowchart'></svg>"
            "<div id='complexity-chart'>Big-O Analysis</div>"
            "<script>console.log('dsa-step');</script>"
            "</body></html>"
        )
        mock_web_dev.return_value = mock_html_content

        response = self.client.post("/generate", data={"prompt": self.test_prompt})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Execution Complete!", response.text)
        
        # Verify content requirements
        self.assertIn("<style>", mock_html_content, "Missing embedded CSS styling container.")
        self.assertIn("<script>", mock_html_content, "Missing embedded Vanilla JS orchestration engine.")
        self.assertIn("<svg", mock_html_content, "Missing native inline SVG execution flowcharts.")
        self.assertIn("complexity-chart", mock_html_content, "Missing required Big-O complexity blocks.")

        # File system cleaning hooks
        expected_path = "generated_spas/array_bubble_sort.html"
        self.assertTrue(os.path.exists(expected_path))
        if os.path.exists(expected_path):
            os.remove(expected_path)
