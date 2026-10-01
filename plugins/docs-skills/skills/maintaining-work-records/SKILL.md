---
name: maintaining-work-records
description: Use to append every request and discussion to its owning work item, manage linked local records and lifecycle, or manually compile a weekly report from authoritative sources.
---

# Maintaining Work Records

## Resolve the canonical repository

Read project instructions and local configuration. Use exactly one configured
document repository for work items, either the project repository or an
existing document repository. In that repository, read
`.docs-schema/manifest.json` and the relevant template. The bundled
[starter schema](../../templates/document-system/.docs-schema/README.md)
is for initial setup only; a versioned local schema is authoritative. If this
skill is unavailable in a future session, project `AGENTS.md` and the local
schema must still suffice with ordinary file tools. If the configured repository
is inaccessible, expose the gap instead of creating a second work-item history.

Do not create a document branch. Commit validated record updates on the
repository's configured primary branch under its normal review and access
policy. An independent clone checked out at that branch may isolate local
changes without creating another branch. The document repository's Git history
is the version history for its records. Private paths and sensitive contents
must not be copied into public product docs or OpenSpec. In public artifacts,
refer only to safe product facts or public identifiers.
After a completed interaction or meaningful checkpoint, validate and commit
the updated record on that branch so a later context can recover it from
Git history. Sync to a configured remote under the repository's normal policy.
For parallel agents, follow
[coordinating-parallel-document-work](../coordinating-parallel-document-work/SKILL.md)
before editing the canonical repository. The current local schema determines
whether each task may own a linked child work item; shared Git operations still
need one integrator.

## Capture a topic's history

Find an existing root or child work item with `python3 .docs-schema/records.py
list`, search, and generated tree relations when available. Keep one root per
user topic and one child per independent delegated task under a graph-capable
schema; each has its own manifest path. Append each request and discussion turn
to its owning node in order with its timestamp, source
role, concise content, and outcome. Also append actions, decisions, checks,
corrections, branch events, and relevant links as they happen. Capture a short
question too; no separate file is needed for each message. Keep the local
template's current-state and next-action fields current, including goal,
progress, code branch/SHA, governing contract or change, experiments, tests,
and blockers. On context handoff,
read the root and descendants plus their linked sources to reconstruct what was discussed,
planned, implemented, verified, and left to do.

Use the local manifest's `create_when`, allowed path, metadata, lifecycle, and
required sections for a specialized local record. When registered, create a
`decision` for a material choice, `design` for internal architecture, `plan`
for internal tasks, and `tdd` for a durable test cycle trace only when
warranted. Do not duplicate OpenSpec's design or task plan for the same scope.
Use `reference-note` for reusable sourced facts with validity bounds when that
type is registered. For an unregistered type, first capture the request in the
work item; update the local schema explicitly if the type is truly needed.
Do not create unregistered directories or manual indexes. Read the configured
repository's `.docs-schema/LIFECYCLE.md` when present; use its state meanings
without treating one type's states as another's.

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

When a code branch is merged, establish the actual target and merged SHA.
Compare adopted behavior with code, tests, and the governing contract. If
OpenSpec owns it, sync only adopted requirements to the main specs, validate,
then archive the completed change through the OpenSpec procedure. Append the
merge, checks, contract update, and next action to the work item. When a code
branch is abandoned, record branch name, last SHA, reason, and useful decision
or experiment links; do not adopt unmerged requirements. Preserve any change
artifacts through their owning procedure and transition the work item according
to its registered lifecycle once history is settled. In the starter schema,
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

Create a report only on explicit request. Read the local manifest's `timezone`,
`week_start`, and registered `weekly-report` path and template; report a schema
gap if that type is unavailable. Use the period's inclusive start and exclusive
end to select events, and derive the report ID
and filename from that schema. When the local checker provides it, run
`python3 .docs-schema/records.py events --week YYYY-MM-DD` from the canonical
repository; verify its interval against the local schema. Collect every
root and child work-item timeline event in the period and verify relevant OpenSpec
specs/changes, experiment records, and code SHAs.
Summarize completed, in-progress, decisions with evidence, deferred/blocked,
and next actions with source links. State the generation `as_of` timestamp.
Follow the registered lifecycle: keep the report in a reviewable state until
its source links and claims are checked, then finalize it. Re-running the same
week updates the same file. For a finalized past week, append a dated correction
entry with the prior statement, replacement, reason,
and source before changing its summary; retain the correction history.

Run `python3 .docs-schema/records.py validate` and use `list` to discover
records. Fix missing fields, orphan links, and stale state. For a schema update,
increment `schema_version`, explicitly migrate affected records, validate, and
commit the schema and migration together. Do not auto-rename legacy experiment
files or promote old notes wholesale into OpenSpec; review each
against accepted product behavior first.
