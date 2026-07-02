# TASK_TEMPLATE.md

Minimal task template placeholder.

Delivery handoffs and final task reports must end with the seven-field textual envelope:
`task_id`, `status`, `executive_summary`, `artifacts`, `gates`, `next_recommended`, `risks`.
The envelope is final text, never a tool call. After a checker NO-GO/change_required, remediate,
re-run affected gates, re-judge the result, and repeat at most two iterations before human escalation.
