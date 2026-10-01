---
name: using-docs-skills
description: Use for every repository request or discussion to find its canonical work-item node, then route document discovery, writing, placement, management, modification, or review to the correct owner.
---

# Using Docs Skills

Every request and discussion needs a trace in the configured work-item history when the
project has configured a canonical document repository. Start by reading project
instructions and `AGENTS.local.md`, then locate that repository and its local
`.docs-schema/manifest.json`. Search existing work items by subject and links;
append to the existing owning node or create one from the local template. The
local schema wins over this plugin's bundled starter. If configuration or the
canonical repository is missing, report that gap; do not silently create a
second history. Use [maintaining-work-records](../maintaining-work-records/SKILL.md)
for this recurring record and local record types.

The work-item tree preserves the user's and agent's thinking over time: each request,
discussion outcome, action, correction, evidence, current goal, code identity,
and next action. A short question still gets a timeline entry in its owning
work item. Record the user's request before dependent work where practical and
append the result after it. A separate `decision`, `design`, `plan`, or `tdd`
requires its registered creation condition; do not create one for every message.
When parallel agents need durable history, use
[coordinating-parallel-document-work](../coordinating-parallel-document-work/SKILL.md)
to give independent tasks separate linked work items and one owner for each
overlapping artifact. The local schema controls whether child nodes are
available; do not silently replace an older schema.

## Find the authoritative content

Determine whether the task concerns a product behavior contract, experiment,
local work history, reusable knowledge, public reader-facing documentation, or
a domain-owned artifact. Search existing files and applicable project rules
before choosing a location. Preserve user-designated paths and formats unless
they conflict with the governing owner. Use the following owners:

- **Product behavior:** Identify the project's governing contract. When
  OpenSpec owns it, read the relevant main spec first. For a changed or missing
  contract, use its CLI-selected store, schema, and paths to write delta
  requirements and testable scenarios. Proposal, design, and tasks alone do
  not establish that contract. Check a bug against an existing main spec when
  it violates one. If the active schema cannot provide a required spec, surface
  the configuration problem. Without OpenSpec, follow the project's configured
  contract process; do not replace any required spec with a local plan.
- **Research experiments:** Use research-skills when installed, or the
  project's configured experiment workflow. That workflow owns its scientific
  protocol, template, root, and evidence. Link it from the work item. If none
  is configured, surface the gap instead of inventing a record format. This
  router handles document placement and edits without changing the scientific
  rules or sending the work back in a loop.
- **Local work history and weekly reports:**
  [maintaining-work-records](../maintaining-work-records/SKILL.md) owns them.
- **Reusable sourced note:**
  [curating-reference-notes](../curating-reference-notes/SKILL.md) owns its
  evidence and validity; the local `reference-note` schema owns its path.
- **Reader-facing documentation:**
  [maintaining-documentation](../maintaining-documentation/SKILL.md) owns
  focused edits and retirement; [auditing-documentation](../auditing-documentation/SKILL.md)
  owns factual audits. A requested read-only review remains read-only.
- **Editable diagrams:** [maintaining-diagrams](../maintaining-diagrams/SKILL.md)
  owns representation and verification; the containing artifact keeps its
  owner and path.

Domain workflows still determine their content, authorization, and lifecycle.
When they forward document work here, resolve the correct source and location,
perform the file operation with their rules, then return evidence to the caller.
Use specialized installed workflows or native commands where they own an
artifact, especially OpenSpec. Do not route back and forth indefinitely.

## Finish

Check the changed document against its owner, sources, format, and links. Run
the local schema validator for changed local records. State which record and
domain artifact were updated and any unresolved configuration or evidence gap.
Do not create a document branch. Use the configured repository's existing
primary branch and access policy; avoid leaking private work records into
public artifacts.
