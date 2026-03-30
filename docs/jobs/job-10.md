# Job 10 — Configure enablement and help tools

## Metadata

| Field | Value |
| --- | --- |
| Category | Configure |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #10 |
| Status | Not started |

## Job statement

When supporting developer onboarding, I want to configure learning aids and quickstarts so that users can quickly adopt the platform and find help when needed.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 5. Customizing the Learning Paths... | Configure Learning Paths to guide developer onboarding |
| 5.2. Customizing... by using a hosted JSON file | Load Learning Paths from a JSON file to provide structured training modules |
| 5.3. Customizing... by using a customization service | Load Learning Paths from a service to serve dynamic training content |
| Chapter 8. Customizing the Quickstart plugin | Customize Quickstart guides to provide interactive assistance |
| 8.2. Manage user access... RBAC | Control Quickstart visibility to target guides to specific user roles |
| 8.3. Customizing your... Quickstart | Define custom Quickstart content to provide internal onboarding instructions |
| Chapter 9. Customizing the Tech Radar... | Configure the Tech Radar to standardize technology adoption |
| 9.1. Customizing... by using a JSON file | Load Tech Radar data from a JSON file to visualize approved technologies |
| Chapter 7. Configuring a floating action button... | Configure Floating Action Buttons to provide quick access to support |
| 7.1. Configuring... as a dynamic plugin | Add floating help buttons to execute common actions or open links |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-10.md
