import json
import tempfile
import unittest
from pathlib import Path

from scripts.sdd_status import load_specs, render_dashboard


class SddStatusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.specs_dir = Path(self.temp.name) / ".sdd" / "specs"
        self.specs_dir.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_spec(self, name="sample", **overrides):
        feature_dir = self.specs_dir / name
        feature_dir.mkdir()
        data = {
            "feature_name": name,
            "created_at": "2026-10-22T00:00:00Z",
            "updated_at": "2026-10-22T00:00:00Z",
            "language": "pt-BR",
            "phase": "initialized",
            "approvals": {
                "requirements": {"generated": False, "approved": False},
                "design": {"generated": False, "approved": False},
                "tasks": {"generated": False, "approved": False},
            },
            "ready_for_implementation": False,
        }
        data.update(overrides)
        (feature_dir / "spec.json").write_text(json.dumps(data), encoding="utf-8")
        return feature_dir

    def test_rejects_directory_without_metadata(self):
        (self.specs_dir / "orphan").mkdir()
        specs, errors = load_specs(self.specs_dir)
        self.assertEqual(specs, [])
        self.assertIn("orphan: missing spec.json", errors)

    def test_rejects_declared_artifact_when_file_is_missing(self):
        self.write_spec(
            approvals={
                "requirements": {"generated": True, "approved": False},
                "design": {"generated": False, "approved": False},
                "tasks": {"generated": False, "approved": False},
            }
        )
        _, errors = load_specs(self.specs_dir)
        self.assertTrue(any("requirements.md" in error for error in errors))

    def test_renders_explicit_blocker(self):
        feature_dir = self.write_spec(
            validation={"status": "blocked", "reason": "Resolve the mismatch."}
        )
        specs, errors = load_specs(self.specs_dir)
        self.assertEqual(errors, [])
        dashboard = render_dashboard(specs)
        self.assertIn("Resolve the mismatch.", dashboard)
        self.assertIn(feature_dir.name, dashboard)

    def test_valid_design_phase_requires_requirements_approval(self):
        feature_dir = self.write_spec(
            phase="design-generated",
            approvals={
                "requirements": {"generated": True, "approved": False},
                "design": {"generated": True, "approved": False},
                "tasks": {"generated": False, "approved": False},
            },
        )
        (feature_dir / "requirements.md").write_text("draft", encoding="utf-8")
        (feature_dir / "design.md").write_text("draft", encoding="utf-8")
        _, errors = load_specs(self.specs_dir)
        self.assertTrue(any("requirements.approved=true" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
