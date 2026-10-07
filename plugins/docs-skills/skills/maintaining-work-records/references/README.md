# Record configuration

The `maintaining-work-records` skill includes a checker, default schema,
lifecycle guidance, and templates. Install the complete skill folder and use
these resources directly. The checker writes no configuration or records.

## Run from the canonical record repository

For a project installation:

```bash
python3 .agents/skills/maintaining-work-records/scripts/records.py validate
python3 .agents/skills/maintaining-work-records/scripts/records.py list
python3 .agents/skills/maintaining-work-records/scripts/records.py tree
python3 .agents/skills/maintaining-work-records/scripts/records.py events --week 2026-09-28
```

For a global installation, run from the chosen project:

```bash
python3 "$HOME/.agents/skills/maintaining-work-records/scripts/records.py" validate --root "$PWD"
```

`--root` selects the canonical repository independently of the installed skill.
Its default is the current working directory. Use the actual installed location
reported by the host when its path differs from these examples.

## Custom schema

The checker selects, in order:

1. A JSON file supplied with `--schema`.
2. `<canonical-repository>/.agents/config/docs-skills/schema.json`, when present.
3. This skill's [default schema](schema.json).

An invalid or missing selected custom file reports an error. It never silently
switches to default rules. An explicit relative `--schema` path is resolved from
the invocation's working directory.

### Start with existing record types

From the project root, create a custom file from the bundled defaults. This
preserves an existing file or link:

```bash
mkdir -p .agents/config/docs-skills
if [ ! -e .agents/config/docs-skills/schema.json ] && [ ! -L .agents/config/docs-skills/schema.json ]; then
  cp .agents/skills/maintaining-work-records/references/schema.json .agents/config/docs-skills/schema.json
fi
```

For a global skill installation, use
`$HOME/.agents/skills/maintaining-work-records/references/schema.json` as the
copy source. The custom file still belongs to the chosen project.

Edit the JSON to change record types, paths, required fields/sections, allowed
states, or the weekly calendar. A custom schema replaces the defaults
completely; retain all record types needed by existing records. No template or
checker copy is required.

### Start with a new custom type

For a new project using only a custom note type, the skill supplies a ready
[schema template](../templates/custom-schema/schema.json) and matching
[note template](../templates/custom-schema/templates/note.md). From the project
root, copy that starter only when the configuration directory is absent:

```bash
mkdir -p .agents/config
if [ ! -e .agents/config/docs-skills ] && [ ! -L .agents/config/docs-skills ]; then
  cp -R .agents/skills/maintaining-work-records/templates/custom-schema .agents/config/docs-skills
fi
```

For a global installation, the copy source is
`$HOME/.agents/skills/maintaining-work-records/templates/custom-schema`.
Edit the copied JSON and `templates/note.md` together. This starter registers
only `note`; add its type to an existing schema rather than replacing other
types still used by records. Default usage needs neither copy procedure.

### Use the file

The project file is selected automatically. Run from the project root:

```bash
python3 .agents/skills/maintaining-work-records/scripts/records.py validate
python3 .agents/skills/maintaining-work-records/scripts/records.py list
```

For a schema stored elsewhere, replace the example path:

```bash
python3 .agents/skills/maintaining-work-records/scripts/records.py validate --schema /path/to/schema.json
```

### Define the rules

The JSON defines `schema_version`, `timezone`, `week_start`, and `types`.
Each type defines its repository-relative `path`, `template`, `create_when`,
`required_sections`, `lifecycles`, and `work_item_required`; it may add
`required_fields`. Path placeholders are `{id}` and `{work_item_id}`.
Paths stay inside the canonical repository.

The supplied custom schema template defines:

```json
{
  "schema_version": 2,
  "timezone": "Asia/Seoul",
  "week_start": "monday",
  "types": {
    "note": {
      "path": "notes/{id}.md",
      "template": "templates/note.md",
      "create_when": "A reusable note is requested.",
      "required_sections": ["Finding", "Sources"],
      "required_fields": ["owner"],
      "lifecycles": ["draft", "final"],
      "work_item_required": false
    }
  }
}
```

This example needs its `templates/note.md` alongside that custom JSON. Existing
work items or other record types need their definitions retained as well.
Records use JSON-scalar frontmatter with `schema_version`, `id`, `type`,
`lifecycle`, `created_at`, and `updated_at`. IDs begin with a valid
`YYYY-MM-DD-topic`; their title begins with that date. Custom types retain
these common requirements.

The supplied note template becomes
`.agents/config/docs-skills/templates/note.md` when copied:

```markdown
---
schema_version: 2
id: "{{date}}-{{topic}}"
type: "note"
lifecycle: "draft"
created_at: "{{timestamp_with_offset}}"
updated_at: "{{timestamp_with_offset}}"
owner: "{{owner}}"
---
# {{date}}-{{topic_title}}

## Finding

## Sources
```

Fill the template fields and save the record at `notes/YYYY-MM-DD-topic.md`,
as specified by this example's path rule. Dates must be valid, and timestamps
include a UTC offset. Run `validate` again after editing the schema or records.

## Custom templates

A relative template path is looked up beside the selected custom JSON first,
then in this skill's bundled resources. Put only templates you customize there.
For example, `templates/work-item.md` in
`.agents/config/docs-skills/templates/` overrides the bundled work-item
template. Absolute paths and paths escaping either resource directory are
rejected. A template missing from both locations, or an existing broken
override, reports an error.

The bundled templates are:

- [Work item](../templates/work-item.md)
- [Decision](../templates/decision.md)
- [Design](../templates/design.md)
- [Plan](../templates/plan.md)
- [TDD](../templates/tdd.md)
- [Reference note](../templates/reference-note.md)
- [Weekly report](../templates/weekly-report.md)

Capture, storage, audience, persistence, and lifecycle policy remain project
choices. Follow a configured lifecycle guide, otherwise the bundled
[LIFECYCLE.md](LIFECYCLE.md). Installing a skill does not enable history capture,
Git publication, or external mirroring.

## Existing configurations

To replace an earlier root `.docs-schema/`, retain its `manifest.json` as the
custom JSON file and any genuinely customized templates or guidance alongside
it. Update project instructions, checker commands, and document links; validate
the existing records before removing the old directory. Keep a recovery copy
until the transition is verified. The checker can read an old manifest directly
through `--schema` during this transition.

Schema version 2 supports linked child work items. An existing version 1
configuration keeps its native rules until an explicit migration. When adopting
version 2, reconcile local customizations, add `parent_work_item_id` to work
items, and validate the records. Changing paths or stored meaning requires an
explicit transition of affected records. The checker does not rename records
or rewrite metadata.

Discovery uses the registered path prefixes, rather than a manual index.
`validate` checks only managed record paths; domain reports and other documents
retain their own checks. `list` and `tree` are generated views; `events` uses
the schema's timezone and week boundary. The checker cannot verify a remote
source or establish the truth of a document's claims.

See [template sources](TEMPLATE_SOURCES.md) for the defaults' provenance.
