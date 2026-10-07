---
name: auditing-documentation
description: Use when asked to check whether repository documentation matches current behavior or to identify documentation gaps for a specified area or change. Read-only. Not for general code review, research reports, or OpenSpec change-artifact maintenance.
---

# Auditing Documentation

Compare what repository documentation tells a reader with the current sources
that define the described behavior. Keep the audit read-only. Audit when the
user requests it or repository policy calls for it; do not infer a full audit
from every code change. A question about existing behavior does not require a
documentation report.

## Choose the scope

Use the user's named documents, feature, or change as the boundary. If no
boundary is named, inspect the smallest relevant documentation surface and
source area supported by the request. Audit the whole repository only when
that scope is requested. Read repository guidance and any local documentation
locations before assuming that `docs/` or `README.md` is the canonical home.
Apply any project-local skill's document ownership and access rules for the
area under review.

Compare a document claim with the current code, configuration, public
interface, tests, generated-document source, or governing repository policy as
appropriate. A document is evidence of what it claims, not proof that the
claim is true. For a missing-document claim, check the plausible documentation
locations before concluding that none exists.

## Report findings

For each material finding, identify the document claim or gap, its source of
truth, the reader impact, and the smallest useful correction. Distinguish a
confirmed mismatch from an inferred gap or an unresolved question. Prioritize
wrong setup steps, API behavior, configuration, and user workflows over style
preferences. State the area actually inspected and any material area left
unchecked; do not call a partial inspection a complete audit.

Report in the conversation unless the user requests a durable report. Do not
edit or create documentation, code, tests, branches, worktrees, commits,
issues, or releases as an audit side effect. Use focused checks that do not
change the repository. Do not install dependencies or regenerate large output
solely to perform an audit.

OpenSpec change artifacts have their own lifecycle. When the request concerns
their internal consistency or state, use an OpenSpec skill only when the current
host lists it, resolving the exact installed name/resource path from that
catalog; a vendor or cache copy alone is not availability. When none is listed,
use the project's native OpenSpec procedure and read-only CLI commands such as
`status`, `show`, `instructions`, and `validate` as appropriate. Do not read an
unlisted skill or weaken the native checks. This skill may audit reader-facing
documentation *about* OpenSpec without taking ownership of those artifacts.
