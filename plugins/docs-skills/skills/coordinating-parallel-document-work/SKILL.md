---
name: coordinating-parallel-document-work
description: Use when parallel agents may write to one canonical document repository or overlapping durable documents. Give independent tasks linked child work items where supported and integrate shared Git changes. Not for a lone agent or parallel read-only investigation.
---

# Coordinating Parallel Document Work

## Give each task its own record

Read the configured repository's local schema before dispatch. When it supports
`parent_work_item_id`, keep the user's topic as the root work item and assign
each independently delegated task a unique dated child work-item ID and path.
Set the child's `parent_work_item_id` to the root or its owning subtask. The
worker owns only that child's timeline and its task-specific local records;
the coordinator owns the root timeline and integration decisions. A child
points to its parent in metadata, so workers never edit a parent merely to add
a backlink. Discover the tree with `python3 .docs-schema/records.py tree --work-item <id>`;
do not maintain an index file.
Record the assigned child IDs and any isolated clone locations in the root's
delegation event so unfinished work can be recovered before integration.

Record every request and discussion in its owning node. The root
captures user requests, coordination, and acceptance; each child captures its
delegated request, actions, decisions, evidence, code identity, and next action.
The child's parent ID supplies the link; the root summarizes its accepted outcome
without copying the child's event stream. On context handoff, read the root
and descendants. Do not close a parent while a required child outcome remains
unresolved.

If the repository's local schema cannot represent child work items, use one
designated writer and worker handoffs under that schema until an explicit
schema migration. Installing this skill does not change the local schema.

## Keep writes and Git operations separate

Give each worker exclusive ownership of its child path. For OpenSpec,
experiments, reports, or any other overlapping artifact, name one writer for
that artifact and have other workers return evidence to that writer. The
artifact's domain workflow still owns its content and lifecycle.

Prefer independent clones checked out on the configured primary branch, where
workers can commit only their owned child files locally. They do not push; the
coordinator imports those commits one at a time. If a shared checkout is used,
workers may edit disjoint child files but do not stage, commit, or push its Git
index. The coordinator waits for stable handoffs before repository-wide
validation and commits completed files. Neither arrangement creates a document
branch.
Workers report their child path, actual code SHA, checks, unresolved questions,
and outcome when handing off a stable record.

## Integrate the tree

Before accepting a child, inspect its current file and evidence rather than
relying on a worker's summary. Re-read the canonical branch, HEAD, working
tree, and remote state before committing. Import only the intended child
changes, then update the root's current state and integration event. Run the
local validator and tree command to catch duplicate IDs, orphan or cyclic
relations, broken links, and incomplete nodes; inspect the exact diff. Follow
the repository's remote sync policy and never force-push. If another writer
changed an overlapping file, reconcile its event history before updating it.
If ownership or reconciliation cannot be established, preserve the child
evidence and leave the affected integration pending.
