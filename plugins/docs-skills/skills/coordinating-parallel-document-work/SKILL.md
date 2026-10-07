---
name: coordinating-parallel-document-work
description: Use when parallel agents may write to one canonical document repository or overlapping durable documents. Give independent tasks linked child work items where supported and integrate shared Git changes. Not for a lone agent or parallel read-only investigation.
---

# Coordinating Parallel Document Work

Coordinate document ownership for already authorized tasks. The selected
development or research workflow retains task scheduling and technical review;
this skill does not dispatch extra agents or parallelize sequential implementation.

## Give each task its own record

Read the configured repository's local schema before dispatch. When it supports
`parent_work_item_id`, keep the user's topic as the root work item and assign
each independently delegated task needing separate history a unique dated
child work-item ID and path under the established capture policy.
Set the child's `parent_work_item_id` to the root or its owning subtask. The
worker owns only that child's timeline and its task-specific local records;
the coordinator owns the root timeline and integration decisions. A child
points to its parent in metadata, so workers never edit a parent merely to add
a backlink. Discover the tree with `python3 .docs-schema/records.py tree --work-item <id>`;
do not maintain an index file.
Record the assigned child IDs and actual assigned workspace locations in the root's
delegation event so unfinished work can be recovered before integration.

If the current host lists
[maintaining-work-records](../maintaining-work-records/SKILL.md), apply its
record procedure at the exact installed name/resource path reported by that
catalog. A sibling or vendor folder alone is not availability. When it is not
listed, apply the established capture policy directly with the canonical
repository's local manifest, lifecycle, and work-item template: locate the root
with `records.py list` and `tree` or search tools, append material events with
actual authorship, reconcile current state and next action, and run
`records.py validate`. Do not read an unlisted skill or its bundled templates.
The root preserves the goal, coordination decisions and accepted outcomes; each
child preserves the relevant assignment, decisions, progress, evidence, code
identity and continuation state.
The child's parent ID supplies the link; the root summarizes its accepted outcome
without copying the child's event stream. The resuming owner reads relevant
history; give fresh workers bounded context, requirements/revision, authority,
and required results. Do not close a parent while a required child outcome remains
unresolved.

If the repository's local schema cannot represent child work items, use one
designated writer and worker handoffs under that schema until an explicit
schema migration. Installing this skill does not change the local schema.

## Keep writes and Git operations separate

Give each worker exclusive ownership of its child path. For OpenSpec,
experiments, reports, or any other overlapping artifact, name one writer for
that artifact and have other workers return evidence to that writer. The
artifact's domain workflow still owns its content and lifecycle.

Use the project's Git workflow to reuse or allocate checkouts and designate
the integration owner. Default to one active writer per checkout; read-only
workers can share it. Concurrent disjoint writers in one checkout require an
explicit project exception and one index owner. Separate record paths alone
do not isolate the index. Independent clones on a dedicated document primary
branch are an option only when that project's Git policy selects them.
Workers stage or commit only within their assignment and existing authority;
the Git owner performs reviewed integration and publication. Do not create
resources or an automatic commit schedule merely to record delegation.

A child node is durable task history, not a brief/report or handoff. Use the
selected agent communication procedure for assignments and results; the
requester retains responsibility. A handoff transfers the named scope with
no acknowledgement requirement. Preserve work/request identity, pending
requests, author attribution, current owner, and reply routing. Read-only
reviewers return evidence to the permitted recorder rather than edit records.
Workers report their child path, source/code revision, dirty state, checks,
unresolved findings, and outcome to the current owner.

## Integrate the tree

Before accepting a child, inspect its current file and evidence rather than
relying on a worker's summary. The Git owner rechecks actual branch, HEAD,
working tree, candidate content, and applicable remote state before mutations.
Integrate only the intended changes under that procedure, then update the
root's current state and integration event. Run the
local validator and tree command to catch duplicate IDs, orphan or cyclic
relations, broken links, and incomplete nodes; inspect the exact diff. Follow
the repository's review, authorization, and remote sync policy. If another writer
changed an overlapping file, reconcile its event history before updating it.
If ownership or reconciliation cannot be established, preserve the child
evidence and leave the affected integration pending.
