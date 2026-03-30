# Job 25 — Audit system events

## Metadata

| Field | Value |
| --- | --- |
| Category | Observe |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #25 |
| Status | Not started |

## Job statement

When ensuring compliance, I want to capture and review audit logs so that I can trace user activities and maintain security accountability.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 1. Audit logs in Red Hat Developer Hub | Review audit logs to track security and compliance events |
| 1.1. Configuring audit logs... on OpenShift | Configure OpenShift logging to capture Developer Hub audit trails |
| 1.2. Forwarding... audit logs to Splunk | Forward audit logs to Splunk to centralize security analysis |
| (Implicit) Configuring ClusterLogForwarder | Define log forwarding pipelines to route audit events to external SIEMs |
| 1.3. Viewing audit logs in Developer Hub | View audit logs in the console to investigate specific events |

## Rewrite instructions

Each heading must express an action + outcome (why the reader does this step).
Replace noun-phrase titles with outcome-oriented equivalents.
Keep all technical steps intact — only headings change.

Apply to: _Confirm source file with CS_

## Acceptance criteria

- [ ] All headings follow action + outcome pattern
- [ ] No heading is a noun phrase only ("Installation", "Prerequisites")
- [ ] Source sections from the table above are all addressed
- [ ] PR linked to this Jira task
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-25.md
