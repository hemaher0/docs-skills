# Local document schema

Copy this entire `.docs-schema/` directory into the chosen document repository and commit it there. The copied manifest, templates, and script are authoritative for that repository. The installed plugin is only a starter and router. Use one canonical repository for work items: either the project repository or a configured document repository. Do not create document branches; commit validated changes on that repository's configured primary branch according to its normal access controls. An independent clone checked out at that branch can isolate local document edits without creating a branch.

For parallel work, create a separate work item for each independently delegated task. Its `parent_work_item_id` points to the root topic or owning subtask; root work items use `null`. Workers own their child files, not the parent. Prefer independent clones on the primary branch: workers commit their own child locally, then one integrator imports the commits and pushes. In a shared checkout, workers edit disjoint child files but only the integrator stages and commits after stable handoffs. No document branch or manually maintained backlink is needed.

The manifest registers the only local record types. Each type has one template, a creation condition, a path, required headings, metadata, and allowed lifecycle values. The common front matter is deliberately a flat YAML subset: each value must be a JSON scalar (`"string"`, number, boolean, or `null`). This keeps the checker independent of YAML packages. Fill placeholders and do not leave them in live records.
See [template research](TEMPLATE_SOURCES.md) for the external GitHub templates reviewed and the choices adapted to these record types.
See [lifecycle and ownership](LIFECYCLE.md) for state meanings and transitions across work items, OpenSpec, experiments, and weekly reports.

```bash
python3 .docs-schema/records.py validate
python3 .docs-schema/records.py list --format markdown
python3 .docs-schema/records.py list --format json
python3 .docs-schema/records.py tree --work-item 2026-09-29-example --format markdown
python3 .docs-schema/records.py events --week 2026-09-28 --format markdown
```

`validate` checks registered paths and types, dates, metadata, sections, ID uniqueness, parent work items, parent cycles, weekly boundaries, and local Markdown links. `list` and `tree` are generated on demand from metadata; `tree` includes child work items and local records linked by `work_item_id`. Keep OpenSpec and experiment links in the owning work item. Do not maintain an `index.md` or parent backlink list. `events` finds timeline entries within a requested Monday-to-Monday Asia/Seoul period, including child events and entries in older work items, for a manually requested weekly report. The script ignores external URLs and non-record Markdown outside the registered roots. It cannot verify the content of a remote source or the truth of a statement.

This starter is schema version 2. An existing version 1 repository stays on its local schema until its owner explicitly adopts the tree format. To migrate, review local customizations, merge the version 2 manifest, templates, and checker, add `parent_work_item_id: null` to each existing root work item (or its actual parent ID), and set every local record's `schema_version` to 2. Validate all records and inspect `tree` before committing the schema and record migration together on the primary branch. Do not silently apply a newer plugin template to an existing repository. If the installed plugin is absent, use this local README, templates, script, and ordinary file tools.

OpenSpec and research experiment records retain their own native schemas and roots. Do not copy an OpenSpec design or plan into a local `design` or `plan` for the same change. When OpenSpec owns the scope, link its artifacts from the work item instead.
