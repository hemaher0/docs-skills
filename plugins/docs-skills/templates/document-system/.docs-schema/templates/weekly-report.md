---
schema_version: 2
id: "{{monday_date}}-weekly-report"
type: "weekly-report"
lifecycle: "draft"
created_at: "{{timestamp_with_offset}}"
updated_at: "{{timestamp_with_offset}}"
period_start: "{{monday_date}}"
period_end: "{{next_monday_date}}"
as_of: "{{timestamp_with_offset}}"
---
# {{monday_date}}-weekly report

## Summary

- Period: {{monday_date}} 00:00 to {{next_monday_date}} 00:00 Asia/Seoul (end exclusive)
- Generated as of: {{timestamp_with_offset}}
- Overall status and material change from the prior week, if supported by sources:

## Completed

- Outcome and source link:

## In progress

- State and source link:

## Decisions and evidence

- Decision, evidence, and source link:

## Deferred and blocked

- Reason, impact, action needed, owner, and source link:

## Next actions

- Action, owner, due date if known, and source link:

## Sources

- Work items, OpenSpec changes/specs, experiment records, and code SHAs used:

## Corrections

- None. For a finalized past week, append timestamp, old statement, replacement, reason, and source; never silently rewrite history.
