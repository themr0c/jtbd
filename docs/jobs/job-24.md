# Job 24 — Monitor system performance and logs

## Metadata

| Field | Value |
| --- | --- |
| Category | Observe |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #24 |
| Status | Not started |

## Job statement

When operating the platform, I want to configure logging levels and metric collection so that I can troubleshoot performance issues and ensure system availability.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 1. Log Levels | Configure application log verbosity to control diagnostic detail |
| (Implicit) Setting LOG_LEVEL | Set the log level to filter events by severity |
| Chapter 2. Enabling observability... on OpenShift | Enable OpenShift observability to scrape metrics from user projects |
| 2.1. Enabling observability... (Operator) | Configure the Operator to create ServiceMonitors for metric collection |
| 2.2. Enabling metrics... (Helm) | Configure the Helm chart to expose metrics for scraping |
| Chapter 3. Monitoring... on AWS | Monitor on AWS to centralize logging and metrics |
| 3.1. Monitoring with Amazon Prometheus | Configure Amazon Prometheus to extract data from pod annotations |
| 3.1.2/3.1.3 Configuring annotations... | Add Prometheus annotations to enable metric scraping by the cloud provider |
| 3.2. Logging with Amazon CloudWatch | Configure Amazon CloudWatch to aggregate container logs |
| 3.3. Viewing logs in CloudWatch | Query CloudWatch logs to analyze application events |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-24.md
