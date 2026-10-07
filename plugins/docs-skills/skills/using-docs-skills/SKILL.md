---
name: using-docs-skills
description: Use to route repository document discovery, writing, placement, management, modification, or review to its owner, and locate the owning work item when project history capture is configured.
---

# Using Docs Skills

Treat another skill as available only when the current host's skill catalog
lists it. A sibling directory, vendor checkout, symlink target, or plugin cache
entry is not availability. Resolve and read/invoke the exact installed name and
resource path reported by that catalog; the relative links below identify the
compatible owner but are not a discovery path. Invoke a listed owner when it
applies. When it is not listed, complete the bounded fallback below from
effective project rules, the configured record rules or native tool, and ordinary
file tools. Do not read an unlisted skill's folder or templates, install it
silently, or route repeatedly.

Read effective project instructions and their referenced configuration. Read
root `AGENTS.local.md` when it exists. Shared capture, persistence, audience
and document rules stay in their existing policy sources. When history capture is
configured, follow that policy, locate the canonical work-item repository and
its configured record definitions, and find the owning node by subject and
links. Append to it or create one from the selected template. A configured
custom schema takes precedence over bundled defaults. Report a missing required source
without silently creating a second history. Reader-facing document work that
does not require work records can proceed under its own project rules.
Installation alone does not enable history capture. Installation and project
configuration follow the source README and its templates. Ordinary document
work uses the effective settings and resolves only gaps material to that work.
When the host lists
[maintaining-work-records](../maintaining-work-records/SKILL.md), use it for
configured capture and local record types. Otherwise read the canonical
repository's configured schema, lifecycle, and relevant template; locate records
with its checker or search tools, make the policy-required update, and run its
validator. Preserve a configured schema until its owner explicitly migrates it.

Keep custom record definitions in their configured JSON file and common
resources in the owning skill, formal store configuration in its native tool,
and document commands/conventions in
their existing configuration or project guide. Inspect runtime facts rather
than copying them into local settings. A selected external checkout override
must resolve the same configured canonical repository, not another history.

The work-item tree preserves enough context to reconstruct the goal, accepted
scope, consequential decisions and rationale, progress, evidence, unresolved
issues, and next action. The recorder owns capture criteria and policy defaults;
message length or type does not determine significance. A separate `decision`,
`design`, `plan`, or `tdd` requires its registered creation condition.
When parallel agents need durable history and the host lists
[coordinating-parallel-document-work](../coordinating-parallel-document-work/SKILL.md),
use it. Otherwise give each independently writable artifact one owner; create
separate child work items only when the selected record schema supports
`parent_work_item_id`; have read-only workers return evidence to an authorized
recorder; and keep one Git/index integrator for a shared checkout. The local
schema controls whether child nodes are available; do not silently replace an
older schema.

## Find the authoritative content

Determine whether the task concerns a product behavior contract, experiment,
local work history, reusable knowledge, public reader-facing documentation, or
a domain-owned artifact. Search existing files and applicable project rules
before choosing a location. Preserve user-designated paths and formats unless
they conflict with the governing owner. Before writing a requested artifact,
resolve its owner and applicable placement, format, metadata, and lifecycle
rules from these sources. Surface missing required rules rather than assuming
that an unrelated document type supplies them. Use the following owners:

- **Product behavior:** Identify the project's governing contract. When
  OpenSpec owns it, read the relevant main spec first. For a changed or missing
  contract, use its CLI-selected store, schema, and paths to write delta
  requirements and testable scenarios. Proposal, design, and tasks alone do
  not establish that contract. Check a bug against an existing main spec when
  it violates one. If the active schema cannot provide a required spec, surface
  the configuration problem. Without OpenSpec, follow the project's configured
  contract process; do not replace any required spec with a local plan.
- **Research experiments:** Use research-skills only when the current host lists
  it; otherwise use the project's configured experiment workflow. That workflow
  owns its scientific protocol, template, root, and evidence. Link it from the
  work item. If none
  is configured, surface the gap instead of inventing a record format. This
  router handles document placement and edits without changing the scientific
  rules or sending the work back in a loop.
- **Local work history and weekly reports:** When listed, use
  [maintaining-work-records](../maintaining-work-records/SKILL.md). Otherwise
  apply the configured capture policy and selected record schema directly: use `list` and
  `tree` to locate the owning record, append material events with actual
  authorship, reconcile lifecycle/current state/next action, and validate. For
  a manually requested weekly report, use the registered period and template,
  gather events with `events --week`, verify linked sources, and keep corrections.
- **Reusable sourced note:** When listed, use
  [curating-reference-notes](../curating-reference-notes/SKILL.md). Otherwise
  update an existing note or create one at the repository-designated or locally
  registered path. Separate verified facts from inference, retain sources and
  validity/recheck bounds, apply its lifecycle, check links, and validate a
  registered record.
- **Reader-facing documentation:** When listed, use
  [maintaining-documentation](../maintaining-documentation/SKILL.md) for focused
  edits and retirement, and
  [auditing-documentation](../auditing-documentation/SKILL.md) for factual audits.
  Otherwise read the relevant guide and source of truth, edit the existing
  suitable page with focused current claims, check affected commands and links,
  and report verification limits. For an audit, make no files or mutations;
  report each claim or gap, its source, reader impact, and smallest correction.
- **Editable diagrams:** When listed, use
  [maintaining-diagrams](../maintaining-diagrams/SKILL.md). Otherwise keep the
  containing artifact's owner and editable format, show only source-backed
  relationships, trace representative paths, and use an existing renderer or
  syntax check when available. Report an unverified render instead of installing
  another tool.

Domain workflows still determine their content, authorization, and lifecycle.
When they forward document work here, resolve the correct source and location,
perform the file operation with their rules, then return evidence to the caller.
Use host-listed specialized workflows or native commands where they own an
artifact, especially OpenSpec. When no specialized workflow is listed, follow
the project procedure and native tool directly without weakening its checks.
Do not route back and forth indefinitely.

Preserve the chain from original intent and necessary derived requirements to
spec criteria, active tasks, assignment results, review findings, and evidence.
Link existing identities rather than renaming them. A durable `plan` or `design`
can be the selected artifact or retain its decisions; it does not create a
second active plan. Exactly one selected execution workflow controls task
scheduling and review retries. Documentation audit checks claims against
sources; technical review and Git candidate/message review keep their owners.

## Finish

Check the changed document against its owner, sources, format, and links. Run
the selected record schema validator for changed local records. Verify that each written
or changed artifact was included in the checks applicable to its owner before
claiming it was validated. A local-record checker establishes coverage only
for the files it actually examined; validate other artifacts through their
own applicable checks. State which record and domain artifact were updated
and any unresolved configuration or evidence gap.
Product documentation accompanies its implementation in the assigned code
checkout. Canonical work history uses its configured repository, audience, and
persistence policy. Use the project's Git procedure for actual allocation,
commits, integration, and publication; this router does not authorize them.
Keep private history out of public artifacts. Return changed paths, source
revision, checks, and unresolved claims to the requesting owner without
declaring implementation completion or disposing of its temporary records.
