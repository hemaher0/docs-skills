# Local document schema

When work records are selected during project setup,
copy this entire `.docs-schema/` directory into the one chosen canonical
repository only if no local schema exists. Preserve an existing local schema
until an explicit migration. Configure capture, persistence, access, and the
repository location in project instructions. The copied schema is authoritative;
the plugin supplies a starter and router. Client installation alone does not
choose these settings or create project instructions.

Use the canonical repository's Git procedure for reviewed, authorized
persistence and allocation. It may explicitly select primary-branch record
commits without document branches; an independent clone is an option only
when that procedure chooses it. Product documentation accompanying code stays
in the assigned code checkout rather than inheriting record-storage rules.

For already authorized parallel work, each independent task can have a child
whose `parent_work_item_id` points to its root/owning subtask; roots use `null`.
Give each artifact one writer and keep the coordinator responsible for shared
state. Default to one active writer per checkout, with suitable separate
checkouts for concurrent writers; a shared-checkout exception needs explicit
project Git policy and one index owner. A child is task history, not a brief,
report, or ownership transfer. The agent communication procedure owns those
semantics. Read-only workers return events to an authorized recorder. Preserve
work/request identity, author, current owner, evidence, and pending requests.

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

`validate` checks registered paths and types, dates, metadata, sections, ID uniqueness, parent work items, parent cycles, weekly boundaries, and local Markdown links. `list` and `tree` are generated on demand from metadata; `tree` includes child work items and local records linked by `work_item_id`. Keep OpenSpec and experiment links in the owning work item. Do not maintain an `index.md` or parent backlink list. `events` finds timeline entries in the manifest's configured weekly interval, including child events and entries in older work items, for a manually requested weekly report. The script ignores external URLs and non-record Markdown outside the registered roots. It cannot verify the content of a remote source or the truth of a statement.

Record paths are repository-relative Markdown path templates using `{id}` and
`{work_item_id}`. Discovery scans managed directories derived from the literal
directory prefix before the first placeholder, once per file. Those directories
are record-owned; keep unrelated prose outside them. Changing registered paths
changes discovery as well as path validation. Paths must resolve inside the
canonical repository. `timezone` is an IANA timezone name; `week_start` is a
weekday name. The starter uses `Asia/Seoul` and `monday`, while local settings
control both validation and event selection. `--week` supplies that week's
configured start date; the end is exclusive seven local calendar days later.

This starter is schema version 2. An existing version 1 repository stays on its
local schema until its owner explicitly adopts the tree format. To migrate,
review local customizations, merge the version 2 manifest, templates, and
checker, add `parent_work_item_id: null` to each root (or its actual parent ID),
and set each local record's `schema_version` to 2. Validate all records and
inspect `tree` before reviewing/persisting schema and migration together through
the repository's Git procedure. Do not silently apply newer plugin templates.
If the plugin is absent, use these local instructions and ordinary file tools.
The checker honors version 2's registered paths and calendar settings. Its
CLI and stored fields remain compatible; adopting an updated checker is an
explicit local update, not an automatic migration of existing records.

Formal specs and research records retain their native owners, schemas, and
roots. When OpenSpec owns the scope, link its artifacts instead of copying its
design/tasks into competing local records. Keep one active plan and execution
controller. The local plan template connects purpose and criterion IDs to task
scope, dependencies, and checks; `Task N` headings/checkboxes serve SDD when it
is selected, while another controller keeps its native task format.

The manifest's creation condition is necessary, not a command to invent a test
cycle. Use a `tdd` record only for an actual warranted RED/GREEN cycle needing
durable trace. Keep ordinary baseline/manual/refactoring verification in the
existing work item or domain report. REFACTOR may be unnecessary; broader test
suites depend on affected risk and project policy. Verification links actual
criteria, observations, source revision, limits, and review dispositions.

Before temporary domain records are removed, durable sources retain the needed
applied requirements, derivations, decisions, evidence, review results, and
continuation state. Disposable links alone are insufficient. Work-item
archival preserves history; assignment DONE, criterion outcomes, technical
review, Git commit success, and goal completion have separate meanings.
