# Job 09 — Configure instance identity and localization

## Metadata

| Field | Value |
| --- | --- |
| Category | Configure |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #9 |
| Status | Not started |

## Job statement

When initializing the instance, I want to set identification details and language preferences so that the platform is correctly identified on the network and accessible to global teams.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 1. Customizing your... title | Set the platform display title to clearly identify the environment |
| Chapter 2. Customizing your... base URL | Set the base URL to ensure correct routing and redirects |
| Chapter 3. Customizing... backend secret | Define the backend secret to secure service-to-service authentication |
| Chapter 13. Customizing the RHDH Metadata card... | Customize build metadata display to control version visibility |
| Chapter 14. Localization... | Localize the platform to support global engineering teams |
| 14.1. Enabling the localization framework... | Enable the localization framework to activate multi-language support |
| 14.2. Selecting the language... | Select the active interface language to serve content in users' preferred language |
| 14.3. Localization support for plugins | Implement localization in plugins to ensure consistent translation coverage |
| 10.3.2. Enabling sidebar... localization | Localize sidebar menu items to translate navigation elements |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-09.md
