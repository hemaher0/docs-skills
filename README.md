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

Keep the marketplace and enablement in the target project using the files
below. Write these project files directly: `codex plugin marketplace add` and
`codex plugin add` save user-level configuration in `~/.codex/config.toml`;
running them from a project directory does not make them project-scoped.
The plugin browser also saves user-level enablement choices.
Neither route is a step in this project-only procedure.

Reuse a suitable source checkout when present. For a first setup, run these
commands from the **target project's root**, with Git access to this repository:

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

Complete the project instructions and applicable schema setup below, then open
the project as trusted and start a **new Codex session**; restart the desktop
app when needed. Codex uses the project configuration during local marketplace
discovery and refresh. Verify that the selected plugins' skills are available
in that project session. Project configuration is loaded only for trusted projects.

Codex may keep plugin files in its shared `~/.codex/plugins/cache/`; that cache
location does not determine enablement scope. Existing user-level enablement
remains a separate setting; adding project settings does not remove it.
See the [official project plugin configuration guide](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo).

### 2. Configure project instructions

Writing root `AGENTS.local.md` is a required installation step.

1. Read existing project instructions, the
   [project settings template](plugins/docs-skills/templates/AGENTS.md) and the
   [local configuration template](plugins/docs-skills/templates/AGENTS.local.md).
   Create the local file from the template, or merge its documentation section
   into the existing file. Preserve established settings and other packages' sections.
2. Replace applicable placeholders with actual values. For work records, fill
   the one canonical repository, audience, capture policy and persistence policy.
   Use the project's established capture policy; installation does not reopen
   that decision or require logging every request and discussion.
   If history is enabled without an established policy, use selective capture:
   preserve the goal and accepted scope, consequential decisions and rationale,
   progress, verification evidence, unresolved issues and next action. Group
   related discussion by outcome. Explicit project policies remain authoritative.
   For reference notes, fill the configured location and storage boundary.
   Fill local checkout/path overrides when used.
3. Keep shared choices in effective project instructions or their existing
   policy home. Documentation conventions and check commands stay in their
   guide/native configuration; record types and paths stay in the local
   `.docs-schema`; formal-store settings stay in that tool's configuration.
   Reference actual sources where settings already exist and verify their
   contents. The workflow entrypoint is
   [using-docs-skills](plugins/docs-skills/skills/using-docs-skills/SKILL.md).
4. Remove fields for features the project does not use. `Disabled`/`None`
   denotes an unused feature, not a missing value. Required unset values keep
   configuration incomplete; a generic "use defaults" statement does not
   configure a repository or storage location.
5. Connect the local file to root instructions using the procedure below.

If root `AGENTS.md` exists, preserve it and add this instruction unless it
already reads or resolves to the local file:

```markdown
Read and follow root AGENTS.local.md when it exists.
```

If `AGENTS.md` is absent, the recommended connection is a relative symbolic
link from the project root, after writing `AGENTS.local.md`:

```bash
ln -s AGENTS.local.md AGENTS.md
```

Preserve existing files and links and avoid self-references. If
`AGENTS.override.md` takes precedence, ensure it reads the local file.

### 3. Set up work records when used

Use **one canonical work-item repository**: this project or one existing
document repository. Preserve its configured identity, audience, capture and
persistence rules. A local checkout override resolves that same repository.
Follow its Git/access policy; installing the plugin does not select commits
after every turn or remote sync.

1. In the chosen repository, copy the entire
   [starter `.docs-schema/`](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
   directory **only if no local `.docs-schema/` exists**. It is under
   `.agents/vendor/docs-skills/plugins/docs-skills/templates/document-system/`
   in this setup. Keep an existing local schema authoritative; installation
   does not migrate it. Adopt the documented version 2 migration only for a
   requested format change. Use one record writer if the schema lacks child nodes.
2. From the chosen document repository, run:

   ```bash
   python3 .docs-schema/records.py validate
   ```

Before completing installation, read the completed `AGENTS.local.md` and its
referenced configuration. Verify that applicable values are filled, no
placeholders remain, configured paths resolve, and effective instructions read
the local file. Validate the schema when work records are used. Check actual
marketplace paths/name and skill availability in a new session. Report the
configured features and any incomplete setup.

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
