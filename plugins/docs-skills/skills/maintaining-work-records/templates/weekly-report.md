---
schema_version: 2
id: "{{week_start_date}}-weekly-report"
type: "weekly-report"
lifecycle: "draft"
created_at: "{{timestamp_with_offset}}"
updated_at: "{{timestamp_with_offset}}"
period_start: "{{week_start_date}}"
period_end: "{{week_end_date}}"
as_of: "{{timestamp_with_offset}}"
---
# {{week_start_date}}-weekly report

## Summary

- Period: {{week_start_date}} 00:00 to {{week_end_date}} 00:00 {{timezone}} (end exclusive)
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
