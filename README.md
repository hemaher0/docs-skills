# docs-skills

A Codex plugin marketplace with two independently installable plugins:

| Plugin | Role |
| --- | --- |
| [docs-skills](plugins/docs-skills/.codex-plugin/plugin.json) | Route document work and preserve history when the project's work-record policy is configured. |
| [openspec](plugins/openspec/.codex-plugin/plugin.json) | Explore, plan, implement, synchronize, and archive OpenSpec changes. |

## Install and configure

Install the selected plugin and configure applicable project settings using
the steps below. Recording work history requires a chosen canonical repository
and local schema; reader-facing document work can use existing project rules.

### 1. Install for a project

Use a repository marketplace and project configuration. Reuse a suitable source
checkout when present. For a first setup, run these commands from
the **target project's root**, with Git access to this repository:

```bash
mkdir -p .agents/vendor .agents/plugins .codex
git clone --branch main https://github.com/hemaher0/docs-skills.git .agents/vendor/docs-skills
```

Create or merge the following into the target project's
`.agents/plugins/marketplace.json`:

```json
{
  "name": "project-skills",
  "plugins": [
    {
      "name": "docs-skills",
      "source": {
        "source": "local",
        "path": "./.agents/vendor/docs-skills/plugins/docs-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    },
    {
      "name": "openspec",
      "source": {
        "source": "local",
        "path": "./.agents/vendor/docs-skills/plugins/openspec"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Keep existing marketplace entries. When using multiple skill repositories, add
their entries to the same `plugins` array. Paths resolve from the target
project's root. If its marketplace already has a different `name`, keep that
name and use it in the configuration keys below.

Merge this setting into the target project's `.codex/config.toml`:

```toml
[plugins."docs-skills@project-skills"]
enabled = true
```

The OpenSpec entry makes that plugin available separately. Enable it only if
needed by adding this setting to the same project configuration:

```toml
[plugins."openspec@project-skills"]
enabled = true
```

Open the target project as a trusted project in Codex, restart the app if using
the desktop client, and start a **new Codex session**. Project configuration is
loaded only for trusted projects. The marketplace source and enablement belong
to this project; Codex may still store installed copies in its shared cache.
See the [official repository marketplace and project configuration guide](https://developers.openai.com/plugins/build/plugins).

### 2. Configure project instructions

Create or update root `AGENTS.local.md` during every installation, even without
a separate request for the file. Read existing instructions and the
[project settings template](plugins/docs-skills/templates/AGENTS.md). Keep shared
capture/persistence/audience choices in effective project instructions or their
existing policy home. Keep documentation conventions, generated sources and
check commands in their existing guide/native configuration, linking them
when discovery needs a pointer. Record types, paths and validation belong to
the local `.docs-schema`; formal-store settings belong to that tool's configuration.
Omit defaults, duplicate procedures and facts already discoverable there.

Read the [local configuration template](plugins/docs-skills/templates/AGENTS.local.md)
and merge its documentation section into `AGENTS.local.md`. Fill only necessary
local paths to the same configured external record/reference store. If no local
overrides are needed, write `Local overrides: None. Use effective project settings and skill defaults.`
in that section. Remove unused template fields; preserve existing values and
other packages' sections without duplicating shared policy or defaults.

Connect the local file to root instructions. If `AGENTS.md` exists, preserve it
and add the following instruction unless it already reads or resolves to the
local file:

```markdown
Read and follow root AGENTS.local.md when it exists.
```

If `AGENTS.md` is absent, the recommended connection is a relative symbolic
link created from the project root, after writing `AGENTS.local.md`:

```bash
ln -s AGENTS.local.md AGENTS.md
```

Preserve existing files and links; do not replace them or add a self-reference
to a linked local file. If `AGENTS.override.md` takes precedence, ensure it also
reads the local file. Verify the effective connection, including link targets.

Inspect repository facts and reuse established choices first. Confirm unresolved
consequential choices with the project owner: whether to enable work history, its one canonical
repository and audience, capture and persistence policy, or a formal-contract
owner. Plugin availability alone does not select OpenSpec, a history repository,
commits after every turn, or remote
sync. If history is not selected, record `Disabled`/`None` for those settings
or omit them; reader-facing documentation still works. Keep required pending
decisions visible and finish independent setup while those choices are pending.
An unresolved choice is pending, not evidence that a setting is unnecessary.

### 3. Set up work records when selected

1. Choose **one canonical work-item repository**: this project or one existing
   document repository. Keep its shared identity, audience, capture policy and
   persistence checkpoints in project instructions or their existing source.
   An optional local path resolves the same external repository. Reuse
   established settings. Its Git procedure controls checkout/branch allocation, reviewed
   commits and publication; a dedicated record repository can explicitly
   choose primary-branch commits without document branches.
2. In the chosen repository, copy the entire
   [starter `.docs-schema/`](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
   directory **only if no local `.docs-schema/` exists**. Find it under
   `.agents/vendor/docs-skills/plugins/docs-skills/templates/document-system/`
   in the target project. Review/persist it under the chosen repository's Git
   policy and existing authority. If an older local schema already exists,
   keep it authoritative. Adopt its
   [explicit version 2 migration](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
   only when that format change is requested; until then use one record writer
   if its schema lacks child nodes. Installation does not migrate local records.
3. From the chosen document repository, run:

   ```bash
   python3 .docs-schema/records.py validate
   ```

Before declaring installation complete, verify that `AGENTS.local.md` contains
the resolved documentation settings or the explicit no-override declaration,
has no unused placeholders, and is read through effective root instructions.
Verify actual marketplace paths/name, configuration sources, and configured
locations; validate the schema only when records are configured.
Start a new session to check skill availability and resolved settings. Report
which features are configured and which are intentionally disabled or still
need a decision. Required unresolved choices remain pending; skill availability
alone does not complete configuration or establish readiness of features that
require project settings.

## Update or remove from a project

From the target project's root, update its source checkout:

```bash
git -C .agents/vendor/docs-skills pull --ff-only
```

Restart the app if using the desktop client and start a new Codex session so
the local plugin is refreshed.

To disable it for this project, set
`plugins."docs-skills@project-skills".enabled = false` in
`.codex/config.toml`, using the project's actual marketplace name. To remove
the project setup, remove that configuration entry and only the `docs-skills`
entry from `.agents/plugins/marketplace.json`. Keep other plugins' entries.
Disable or remove `openspec@project-skills` independently in the same way.
Keep the source checkout while either plugin still uses it; remove it separately
once neither plugin needs it.

## Repository documentation

| Skill | Role |
| --- | --- |
| [using-docs-skills](plugins/docs-skills/skills/using-docs-skills/SKILL.md) | Route documents to their owners and find work-item nodes under configured history capture. |
| [coordinating-parallel-document-work](plugins/docs-skills/skills/coordinating-parallel-document-work/SKILL.md) | Give parallel tasks linked child records and integrate them without competing writes. |
| [maintaining-work-records](plugins/docs-skills/skills/maintaining-work-records/SKILL.md) | Maintain work-item timelines, specialized local records, lifecycle, and manually requested weekly reports. |
| [auditing-documentation](plugins/docs-skills/skills/auditing-documentation/SKILL.md) | Compare documentation claims with current sources without changing files. |
| [maintaining-documentation](plugins/docs-skills/skills/maintaining-documentation/SKILL.md) | Make a focused repository documentation change when requested or required by repository policy. |
| [maintaining-diagrams](plugins/docs-skills/skills/maintaining-diagrams/SKILL.md) | Create or update an editable diagram that explains a repository document or managed text artifact. |
| [curating-reference-notes](plugins/docs-skills/skills/curating-reference-notes/SKILL.md) | Maintain reusable internal notes in the repository-designated reference area. |

The copied [local schema](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
controls record types, paths, templates, and validation; it works with ordinary
file tools when this plugin is unavailable. The schema also documents its
[template sources](plugins/docs-skills/templates/document-system/.docs-schema/TEMPLATE_SOURCES.md).

Development owns intent, necessary derived requirements, the active spec/plan,
execution and technical review. Documentation owns placement, durable history,
reader-facing edits and factual audits. Git owns actual checkouts, content/message
review, authorization and mutations. Product docs accompany code in its assigned
checkout; work records follow their configured repository/schema and audience.
Linked child work items retain history and do not replace briefs/reports or
transfer responsibility. One active plan and execution controller govern a
scope. Preserve accepted requirements, decisions, review outcomes and covering
evidence durably before the domain owner disposes of temporary records.

## OpenSpec

| Skill | Role |
| --- | --- |
| [openspec-explore](plugins/openspec/skills/openspec-explore/SKILL.md) | Explore an idea or change before deciding its scope. |
| [openspec-propose](plugins/openspec/skills/openspec-propose/SKILL.md) | Create a proposal and its planning artifacts. |
| [openspec-update-change](plugins/openspec/skills/openspec-update-change/SKILL.md) | Revise an existing change's planning artifacts. |
| [openspec-apply-change](plugins/openspec/skills/openspec-apply-change/SKILL.md) | Implement tasks from an OpenSpec change. |
| [openspec-sync-specs](plugins/openspec/skills/openspec-sync-specs/SKILL.md) | Sync a change's delta specs into the main specs. |
| [openspec-archive-change](plugins/openspec/skills/openspec-archive-change/SKILL.md) | Archive a completed change. |

When the project designates OpenSpec, it owns product behavior contracts and
native change artifacts; work items link them. Otherwise follow the existing
project contract process. Select one execution controller for its active tasks;
do not run OpenSpec apply and another implementation controller for the same
scope simultaneously. The
plugin supplies skills but not the CLI. Follow the
[official OpenSpec installation guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md).
For a new project, `openspec init --tools none` avoids generating a second set
of tool skills. Keep an existing project's OpenSpec configuration.
