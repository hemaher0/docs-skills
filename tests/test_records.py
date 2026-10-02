import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCHEMA = Path(__file__).resolve().parents[1] / "plugins/docs-skills/templates/document-system/.docs-schema"
SCRIPT = SCHEMA / "records.py"


def load_module():
    spec = importlib.util.spec_from_file_location("records", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RecordsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(SCHEMA, self.root / ".docs-schema")
        self.records = load_module()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, relative, metadata, sections, links=""):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        frontmatter = "\n".join(f"{key}: {json.dumps(value)}" for key, value in metadata.items())
        body = "\n".join(f"## {section}\n\nContent.\n" for section in sections)
        path.write_text(f"---\n{frontmatter}\n---\n# {metadata['id']}\n\n{body}{links}", encoding="utf-8")
        return path

    def base(self, doc_type, doc_id, **extra):
        data = dict(schema_version=2, id=doc_id, type=doc_type, lifecycle="active",
                    created_at="2026-09-29T10:00:00+09:00",
                    updated_at="2026-09-29T10:00:00+09:00")
        if doc_type == "work-item":
            data["parent_work_item_id"] = None
        data.update(extra)
        return data

    def work_item(self):
        path = self.write("references/work-items/2026-09-29-feature/2026-09-29-feature-work-item.md",
                          self.base("work-item", "2026-09-29-feature"),
                          ["Current state", "Timeline", "Related records", "Next action"])
        path.write_text(path.read_text().replace("## Related records",
                        "### 2026-09-29T10:00:00+09:00 — request — user\n\nInitial request.\n\n## Related records"))
        return path

    def test_valid_record_and_list(self):
        self.work_item()
        errors = self.records.validate(self.root)
        self.assertEqual(errors, [])
        listed = self.records.list_records(self.root)
        self.assertEqual(listed[0]["id"], "2026-09-29-feature")

    def test_missing_metadata_and_section(self):
        data = self.base("work-item", "2026-09-29-feature")
        del data["updated_at"]
        self.write("references/work-items/2026-09-29-feature/2026-09-29-feature-work-item.md",
                   data, ["Current state"])
        errors = "\n".join(self.records.validate(self.root))
        self.assertIn("updated_at", errors)
        self.assertIn("Timeline", errors)

    def test_duplicate_id_and_orphan(self):
        self.work_item()
        metadata = self.base("decision", "2026-09-29-feature", lifecycle="pending", work_item_id="2026-09-29-unknown")
        self.write("references/work-items/2026-09-29-unknown/2026-09-29-feature.md", metadata,
                   ["Context", "Options", "Decision", "Rationale", "Consequences"])
        errors = "\n".join(self.records.validate(self.root))
        self.assertIn("duplicate id", errors)
        self.assertIn("orphan", errors)

    def test_invalid_date_and_broken_link(self):
        metadata = self.base("work-item", "2026-02-30-feature")
        self.write("references/work-items/2026-02-30-feature/2026-02-30-feature-work-item.md",
                   metadata, ["Current state", "Timeline", "Related records", "Next action"],
                   "\n[missing](./missing.md)\n")
        errors = "\n".join(self.records.validate(self.root))
        self.assertIn("invalid date", errors)
        self.assertIn("broken link", errors)

    def test_broken_local_link_with_spaces(self):
        path = self.work_item()
        path.write_text(path.read_text() + "\n[missing](<./missing file.md>)\n")
        self.assertIn("broken link", "\n".join(self.records.validate(self.root)))

    def test_broken_local_image_link(self):
        path = self.work_item()
        path.write_text(path.read_text() + "\n![diagram](./missing.svg)\n")
        self.assertIn("broken link", "\n".join(self.records.validate(self.root)))

    def test_weekly_period(self):
        self.write("references/weekly-reports/2026-09-28-weekly-report.md",
                   self.base("weekly-report", "2026-09-28-weekly-report",
                             lifecycle="draft",
                             period_start="2026-09-28", period_end="2026-10-05",
                             as_of="2026-09-29T10:00:00+09:00"),
                   ["Summary", "Completed", "In progress", "Decisions and evidence",
                    "Deferred and blocked", "Next actions", "Sources", "Corrections"])
        self.assertEqual(self.records.validate(self.root), [])

    def test_templates_and_standalone_cli_without_installed_plugin(self):
        self.work_item()
        replacements = {"{{date}}": "2026-09-29", "{{topic}}": "feature",
                        "{{topic_title}}": "Feature", "{{timestamp_with_offset}}": "2026-09-29T10:00:00+09:00",
                        "{{work_item_id}}": "2026-09-29-feature", "{{week_start_date}}": "2026-09-28",
                        "{{week_end_date}}": "2026-10-05", "{{timezone}}": "Asia/Seoul"}
        for doc_type in ("decision", "design", "plan", "tdd", "reference-note", "weekly-report"):
            content = (self.root / ".docs-schema/templates" / f"{doc_type}.md").read_text()
            for source, target in replacements.items():
                content = content.replace(source, target)
            if doc_type in ("decision", "design", "plan", "tdd"):
                path = self.root / f"references/work-items/2026-09-29-feature/2026-09-29-feature-{doc_type}.md"
            elif doc_type == "reference-note":
                path = self.root / "references/reference-notes/2026-09-29-feature-reference-note.md"
            else:
                path = self.root / "references/weekly-reports/2026-09-28-weekly-report.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        command = [sys.executable, ".docs-schema/records.py", "validate"]
        result = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        weekly = self.root / "references/weekly-reports/2026-09-28-weekly-report.md"
        weekly.write_text(weekly.read_text().replace("- None. For a finalized", "- 2026-09-29T11:00:00+09:00 corrected a source.\n- None. For a finalized"))
        self.assertEqual(subprocess.run(command, cwd=self.root, capture_output=True).returncode, 0)
        self.assertEqual(len(list(weekly.parent.glob("*.md"))), 1)

    def test_schema_version_change_requires_explicit_record_update(self):
        self.work_item()
        manifest = self.root / ".docs-schema/manifest.json"
        data = json.loads(manifest.read_text())
        data["schema_version"] = 3
        manifest.write_text(json.dumps(data))
        self.assertIn("schema_version", "\n".join(self.records.validate(self.root)))
        record = self.root / "references/work-items/2026-09-29-feature/2026-09-29-feature-work-item.md"
        record.write_text(record.read_text().replace("schema_version: 2", "schema_version: 3"))
        self.assertEqual(self.records.validate(self.root), [])

    def test_registry_rejects_missing_type_template(self):
        self.work_item()
        (self.root / ".docs-schema/templates/work-item.md").unlink()
        self.assertIn("missing template", "\n".join(self.records.validate(self.root)))

    def configure(self, **settings):
        manifest = self.root / ".docs-schema/manifest.json"
        registry = json.loads(manifest.read_text())
        registry.update(settings)
        manifest.write_text(json.dumps(registry))
        return registry

    def relocate_work_item(self):
        path = self.work_item()
        registry = json.loads((self.root / ".docs-schema/manifest.json").read_text())
        registry["types"]["work-item"]["path"] = "notes/work/{id}.md"
        self.configure(types=registry["types"])
        target = self.root / "notes/work/2026-09-29-feature.md"
        target.parent.mkdir(parents=True)
        path.rename(target)
        return target

    def test_registered_custom_path_is_discovered_and_validated(self):
        self.relocate_work_item()
        self.assertEqual(self.records.validate(self.root), [])
        listed = self.records.list_records(self.root)
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["path"], "notes/work/2026-09-29-feature.md")
        self.assertEqual(self.records.work_tree(self.root)[0]["id"], "2026-09-29-feature")
        self.assertEqual(len(self.records.weekly_events(self.root, "2026-09-28")), 1)

    def test_malformed_record_under_custom_path_is_not_silently_skipped(self):
        self.relocate_work_item().write_text("Malformed record without metadata.\n")
        errors = "\n".join(self.records.validate(self.root))
        self.assertIn("notes/work/2026-09-29-feature.md", errors)
        self.assertIn("missing JSON-scalar front matter", errors)

    def test_overlapping_registered_roots_discover_each_record_once(self):
        self.relocate_work_item()
        registry = json.loads((self.root / ".docs-schema/manifest.json").read_text())
        registry["types"]["reference-note"]["path"] = "notes/{id}.md"
        self.configure(types=registry["types"])
        self.assertEqual(len(self.records.list_records(self.root)), 1)
        self.assertEqual(self.records.validate(self.root), [])

    def test_invalid_registered_path_reports_configuration_error(self):
        registry = json.loads((self.root / ".docs-schema/manifest.json").read_text())
        for pattern in ("../outside/{id}.md", "/outside/{id}.md", "notes/{unknown}.md"):
            with self.subTest(pattern=pattern):
                registry["types"]["work-item"]["path"] = pattern
                self.configure(types=registry["types"])
                self.assertTrue(self.records.validate(self.root))
                result = subprocess.run([sys.executable, ".docs-schema/records.py", "validate"],
                                        cwd=self.root, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)

    def test_weekly_events_follow_configured_timezone_and_exclusive_end(self):
        path = self.work_item()
        path.write_text(path.read_text().replace("### 2026-09-29T10:00:00+09:00", "### 2026-09-27T18:00:00+00:00")
                        .replace("## Related records",
                                 "### 2026-10-04T20:00:00+00:00 — result — agent\n\nWithin UTC week.\n\n"
                                 "### 2026-10-05T00:00:00+00:00 — result — agent\n\nNext UTC week.\n\n"
                                 "## Related records"))
        self.configure(timezone="UTC")
        events = self.records.weekly_events(self.root, "2026-09-28")
        self.assertEqual([event["timestamp"] for event in events], ["2026-10-04T20:00:00+00:00"])

    def test_configured_weekday_governs_events_and_report_validation(self):
        self.work_item()
        self.configure(timezone="UTC", week_start="sunday")
        self.assertEqual(len(self.records.weekly_events(self.root, "2026-09-27")), 1)
        with self.assertRaisesRegex(ValueError, "Sunday"):
            self.records.weekly_events(self.root, "2026-09-28")
        self.write("references/weekly-reports/2026-09-27-weekly-report.md",
                   self.base("weekly-report", "2026-09-27-weekly-report", lifecycle="draft",
                             period_start="2026-09-27", period_end="2026-10-04",
                             as_of="2026-09-29T10:00:00+00:00"),
                   ["Summary", "Completed", "In progress", "Decisions and evidence",
                    "Deferred and blocked", "Next actions", "Sources", "Corrections"])
        self.assertEqual(self.records.validate(self.root), [])

    def test_invalid_calendar_reports_configuration_error(self):
        for settings in ({"timezone": "Invalid/Timezone"}, {"timezone": "UTC", "week_start": "not-a-day"}):
            with self.subTest(settings=settings):
                self.configure(**settings)
                self.assertIn("manifest.json", "\n".join(self.records.validate(self.root)))
                with self.assertRaises(ValueError):
                    self.records.weekly_events(self.root, "2026-09-28")

    def test_invalid_manifest_shape_reports_error_without_traceback(self):
        manifest = self.root / ".docs-schema/manifest.json"
        for value in (None, [], "not an object"):
            with self.subTest(value=value):
                manifest.write_text(json.dumps(value))
                self.assertIn("manifest must be an object", "\n".join(self.records.validate(self.root)))
                result = subprocess.run([sys.executable, ".docs-schema/records.py", "validate"],
                                        cwd=self.root, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)

    def test_weekly_events_include_timeline_from_older_work_items(self):
        path = self.work_item()
        previous = "### 2026-09-27T20:00:00+09:00 — request — user\n\nPrevious week.\n\n"
        path.write_text(path.read_text().replace("### 2026-09-29T10:00:00+09:00", previous +
                        "### 2026-09-29T10:00:00+09:00").replace("## Related records",
                        "### 2026-09-29T11:00:00+09:00 — result — agent\n\nThis week.\n\n## Related records"))
        events = self.records.weekly_events(self.root, "2026-09-28")
        self.assertEqual(len(events), 2)
        self.assertIn("This week", events[1]["content"])
        self.assertEqual(events[1]["work_item_id"], "2026-09-29-feature")
        result = subprocess.run([sys.executable, ".docs-schema/records.py", "events", "--week", "2026-09-28"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 2)

    def test_work_item_requires_dated_timeline_event(self):
        path = self.work_item()
        path.write_text(path.read_text().replace("### 2026-09-29T10:00:00+09:00 — request — user",
                                               "### someday — request — user"))
        self.assertIn("invalid timeline event", "\n".join(self.records.validate(self.root)))

    def test_parallel_children_are_discoverable_without_editing_parent(self):
        parent = self.work_item()
        original_parent = parent.read_text()
        for suffix in ("parser", "normalizer"):
            child_id = f"2026-09-29-feature-{suffix}"
            path = self.write(
                f"references/work-items/{child_id}/{child_id}-work-item.md",
                self.base("work-item", child_id, parent_work_item_id="2026-09-29-feature"),
                ["Current state", "Timeline", "Related records", "Next action"],
            )
            path.write_text(path.read_text().replace(
                "## Related records",
                f"### 2026-09-29T11:00:00+09:00 — result — {suffix}\n\nTask result.\n\n## Related records",
            ))
        self.assertEqual(parent.read_text(), original_parent)
        self.assertEqual(self.records.validate(self.root), [])
        tree = self.records.work_tree(self.root, "2026-09-29-feature")
        self.assertEqual([child["id"] for child in tree["children"]],
                         ["2026-09-29-feature-normalizer", "2026-09-29-feature-parser"])
        self.assertEqual(len(self.records.weekly_events(self.root, "2026-09-28")), 3)
        result = subprocess.run(
            [sys.executable, ".docs-schema/records.py", "tree", "--work-item", "2026-09-29-feature"],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["children"]), 2)

    def test_invalid_parent_and_cycle_are_rejected(self):
        self.work_item()
        child_id = "2026-09-29-feature-parser"
        child = self.write(
            f"references/work-items/{child_id}/{child_id}-work-item.md",
            self.base("work-item", child_id, parent_work_item_id="2026-09-29-missing"),
            ["Current state", "Timeline", "Related records", "Next action"],
        )
        child.write_text(child.read_text().replace(
            "## Related records",
            "### 2026-09-29T11:00:00+09:00 — result — agent\n\nTask result.\n\n## Related records",
        ))
        self.assertIn("missing parent work-item", "\n".join(self.records.validate(self.root)))
        child.write_text(child.read_text().replace("2026-09-29-missing", "2026-09-29-feature"))
        parent = self.root / "references/work-items/2026-09-29-feature/2026-09-29-feature-work-item.md"
        parent.write_text(parent.read_text().replace("parent_work_item_id: null",
                                                     f'parent_work_item_id: "{child_id}"'))
        self.assertIn("cycle", "\n".join(self.records.validate(self.root)))

    def test_tree_includes_task_specific_local_records(self):
        self.work_item()
        decision_id = "2026-09-29-feature-decision"
        self.write(
            f"references/work-items/2026-09-29-feature/{decision_id}.md",
            self.base("decision", decision_id, lifecycle="pending",
                      work_item_id="2026-09-29-feature"),
            ["Context", "Decision drivers", "Options", "Decision", "Rationale",
             "Consequences", "Confirmation"],
        )
        self.assertEqual(self.records.validate(self.root), [])
        tree = self.records.work_tree(self.root, "2026-09-29-feature")
        self.assertEqual([record["id"] for record in tree["records"]], [decision_id])

    def test_v1_work_item_requires_explicit_graph_migration(self):
        path = self.work_item()
        path.write_text(path.read_text().replace("schema_version: 2", "schema_version: 1")
                        .replace("parent_work_item_id: null\n", ""))
        errors = "\n".join(self.records.validate(self.root))
        self.assertIn("schema_version", errors)
        self.assertIn("parent_work_item_id", errors)

    def test_weekly_events_sort_by_instant_across_offsets(self):
        path = self.work_item()
        path.write_text(path.read_text().replace("## Related records",
                        "### 2026-09-29T01:00:00+00:00 — result — agent\n\nLater instant.\n\n## Related records"))
        events = self.records.weekly_events(self.root, "2026-09-28")
        self.assertEqual(events[0]["kind"], "request")
        self.assertEqual(events[1]["kind"], "result")


if __name__ == "__main__":
    unittest.main()
