---
name: maintaining-work-records
description: Use to capture requests and discussion under the project's history policy, manage linked local work records and lifecycle, or manually compile a weekly report from authoritative sources.
---

# Maintaining Work Records

## Resolve the canonical repository

Resolve storage, capture and persistence rules from effective project
instructions or their existing configuration source. Use an optional local
checkout-path override only for that same configured repository; unset/None
values leave the shared setting in force. Preserve existing configuration
without an automatic move or migration. Use exactly one configured
document repository for work items, either the project repository or an
existing document repository. Read its configured custom schema, or this
skill's bundled
[default schema](references/schema.json), and the relevant template. Templates
and the checker stay in this complete skill folder; no root framework copy is
required. The [record configuration guide](references/README.md) explains the
JSON schema and custom template lookup. A selected existing schema remains
binding until an explicit migration.
For a new custom type, the [schema starter](templates/custom-schema/schema.json)
and matching [note template](templates/custom-schema/templates/note.md) are
available alongside the seven default record templates. Retain existing type
definitions when adding a type to an established configuration.

Resolve this skill's actual installed directory and run its
[scripts/records.py](scripts/records.py) with Python and `--root` set to the
canonical repository. From that repository, the checker defaults to its current
directory. It selects `.agents/config/docs-skills/schema.json` when present,
otherwise this skill's bundled definitions; `--schema` selects another complete
JSON definition explicitly. Invalid selected schemas report an error instead
of falling back. When this skill is unavailable, use established project record
rules and ordinary file tools without reading an unlisted skill's resources.
If the configured repository is inaccessible, expose the gap instead of
creating a second work-item history.

Use the canonical repository's configured checkout, branch, review, and access
policy. A dedicated document repository may explicitly require primary-branch
record commits without document branches. Its Git workflow owns allocation and
actual mutations. Product documentation accompanying code uses the code task's
assigned checkout instead. Keep private paths and sensitive history out of
public product docs or formal specs; use safe product facts or identifiers.
Validate updates at the configured persistence checkpoint. When project policy
calls for commits after interactions or other checkpoints, request the actual
candidate/message review and authorized commit through its Git procedure;
remote sync also follows that policy and existing authority. Installation alone
does not authorize commits or publication. Record-only persistence uses checks
for its actual artifact and does not restart an implementation finalization
cycle. Preserve legitimate historical requests, decisions, and attribution.
For parallel agents, use
[coordinating-parallel-document-work](../coordinating-parallel-document-work/SKILL.md)
only when the current host lists it; a sibling or vendor folder alone is not
availability. Resolve and use the exact installed name/resource path from that
catalog rather than the relative documentation link. Otherwise assign one
writer to each record or overlapping artifact, create linked child work items
only when the selected record schema supports `parent_work_item_id`, have
read-only
workers return evidence to an authorized recorder, and designate one Git/index
integrator for a shared checkout. Do not read or require the unlisted companion
skill. The selected record schema determines whether each task may own a
linked child work item.

## Capture a topic's history

Find an existing root or child work item with the resolved checker's `list`
command, search, and generated tree relations when available. Keep one root per
captured topic and one child per delegated task needing separate history under
a graph-capable schema; each has its own manifest path. Follow the established
project capture policy. When capture is enabled without a more specific policy,
use selective capture: preserve information that changes the goal or accepted
scope, explains
a consequential decision, establishes progress or verification, or affects
remaining work and continuation. Group discussion supporting the same outcome
into an accurate entry; the unit of history is a meaningful change, not a message.
An explicitly exhaustive policy can require a fuller chronology; a disabled
policy does not produce automatic history. Neither is selected merely because
this skill is installed.

For captured changes, preserve the actual source and authorship, timestamp,
outcome, rationale, and relevant evidence. Record a decision before dependent
work when practical and its observed result afterward. Maintain the current
state and next action from those events, linking the governing artifacts rather
than copying their entire contents. On context handoff,
the resuming work owner reads the relevant root/descendants and linked sources
to reconstruct what was discussed, planned, implemented, verified, and left
to do. Fresh assignees receive bounded relevant context from that owner.

A child work item retains task history; it is not a brief, report, or ownership
transfer. Link existing work/task/request IDs, spec revision and criteria,
reports, findings and their dispositions when relevant. The assignment's
requester retains responsibility; a handoff transfers only its named scope
without requiring acknowledgement. Keep the same work identity and record the
new owner, pending requests, reply destination, actual author, and consumed
review/fix limits. A read-only assignee can return events to an authorized
recorder; preserve authorship without expanding the assignee's write authority.

Use the selected schema's `create_when`, allowed path, metadata, lifecycle, and
required sections for a specialized local record. When registered, create a
`decision` for a material choice, `design` for internal architecture, `plan`
for internal tasks, and `tdd` for a durable test cycle trace only when
warranted. A TDD record requires an actual justified test cycle; a broad local
creation condition is not a requirement to manufacture RED/GREEN evidence.
Put baseline, manual, or refactoring verification in the existing work item or
domain report when no TDD cycle applies. Reuse the selected active plan and
governing design; a durable record must not become a competing plan or duplicate
OpenSpec's artifacts for the same scope. Preserve the selected execution
controller and its task format; use `Task N` extraction headings only when
that controller requires them.
Use `reference-note` for reusable sourced facts with validity bounds when that
type is registered. For an unregistered type, record the material need under
the capture policy; update the selected record schema explicitly if the type
is needed. Do not create unregistered directories or manual indexes. Read the
configured lifecycle guide, or this skill's
[LIFECYCLE.md](references/LIFECYCLE.md); use its state meanings without treating
one type's states as another's.

## Keep contracts and evidence linked

When OpenSpec governs a product behavior change, read its existing main spec.
Use the CLI-selected root, schema, and artifact paths for the change. Require
delta requirements and verifiable scenarios for a changed or missing contract;
compare implementation and tests to them. If the schema skips or omits needed
specs, surface that configuration problem rather than writing a local plan.
For a bug against an existing contract, verify against that spec. The work
item links the governing artifacts and code SHA, not a competing contract.
For research, preserve the experiment's own configured root and template and
link its protocol, outcome, and evidence from the work item.

When a code branch is merged, obtain the actual target and merged SHA from
the Git owner; this skill does not perform integration.
Compare adopted behavior with code, tests, and the governing contract. If
OpenSpec owns it, forward any remaining sync/validation/archive to its owning
procedure. Reuse an already verified transition; do not perform it twice.
Only adopted requirements belong in main specs. Append the
merge, checks, contract update, and next action to the work item. When a code
branch is abandoned, record branch name, last SHA, reason, and useful decision
or experiment links; do not adopt unmerged requirements. Preserve any change
artifacts through their owning procedure and transition the work item according
to its registered lifecycle once history is settled. In the bundled schema,
`archived` means retained history, not an invalid or deprecated claim. For
postponed work, use the registered postponed state when it has one and name the
trigger to resume. Do not silently delete a record.

Before setting a work item to `completed` or `archived`, reconcile its current
state with the latest timeline event and authoritative code, contract, and
research artifacts. Recheck the goal, progress, code branch/SHA, governing
change, evidence, blocker, and next action; update every field affected by the
transition. If progress says the goal is finished while a blocker or next
action still describes unfinished work within that goal or its required
finalization, either correct those fields or keep the item active or deferred.
Keep assignment DONE, criterion MET/NOT_MET/NOT_VERIFIED, review dispositions,
work-item lifecycle, commit success, and integration readiness distinct. The
invoking workflow owns technical review schedules and retry limits; recording
a result cannot waive an unresolved blocker. Before temporary development
records are disposed of, durable sources must retain the necessary applied
requirements, derivations, decisions, review outcomes, evidence, and unresolved
continuation state. Links to files being removed are insufficient. The domain
owner decides temporary retention; archival here preserves history.
Track a separate follow-up in its own work item. Run schema validation after
this review, but do not treat a structural pass as proof that the prose is
factually current.

When auditing a work item, compare exact values quoted in the record itself,
including earlier timeline events, with the linked sources or command output.
Checking source artifacts against each other does not verify a copied hash,
identifier, or measurement in the record. Preserve an incorrect historical
event and append a dated correction with the prior value, replacement, and
source; update the current state when affected. Claim the record's values match
only after checking the recorded values, not just their source artifacts.

## Manual weekly report

Create a report only on explicit request. Read the selected schema's `timezone`,
`week_start`, and registered `weekly-report` path and template; report a schema
gap if that type is unavailable. Use the period's inclusive start and exclusive
end to select events, and derive the report ID
and filename from that schema. When the selected checker provides it, run
the resolved checker's `events --week YYYY-MM-DD` command from the canonical
repository; verify its interval against the selected record schema. Collect
every root and child work-item timeline event in the period and verify relevant
OpenSpec specs/changes, experiment records, and code SHAs.
Summarize completed, in-progress, decisions with evidence, deferred/blocked,
and next actions with source links. State the generation `as_of` timestamp.
Follow the registered lifecycle: keep the report in a reviewable state until
its source links and claims are checked, then finalize it. Re-running the same
week updates the same file. For a finalized past week, append a dated correction
entry with the prior statement, replacement, reason,
and source before changing its summary; retain the correction history.

Run the resolved checker's `validate` command with the canonical `--root` and
use `list` to discover records. Fix missing fields, orphan links, and stale
state. For a schema update that changes stored meaning,
increment `schema_version`, explicitly migrate affected records, validate, and
persist the schema and migration together through the project's reviewed,
authorized Git procedure. Do not auto-rename legacy experiment
files or promote old notes wholesale into OpenSpec; review each
against accepted product behavior first.
