# Job 21 — Write and publish technical documentation

## Metadata

| Field | Value |
| --- | --- |
| Category | Develop |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #21 |
| Status | Not started |

## Job statement

When documenting features, I want to write, edit, and search technical documentation directly within the platform so that knowledge is accessible and stays synchronized with the code.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| (Manage) Chapter 1. Adding documentation to TechDocs... | Add documentation to the platform to centralize project knowledge |
| 1.1. Importing documentation... | Import docs-as-code from repositories to synchronize docs with code |
| (Manage) Chapter 2. Searching for relevant content... | Search technical documentation to find specific information quickly |
| (Manage) Chapter 3. Accessing and reading documentation... | Read and navigate documentation to consume project details |
| (TechDocs) Chapter 3. TechDocs add-ons | Enhance the reading experience with add-ons |
| 3.3.1. Using the ReportIssue... | Report documentation issues to provide feedback directly from the page |
| 3.3.2. Using the TextSize... | Adjust text size to improve readability |
| 3.3.3. Using the LightBox... | View images in LightBox to inspect diagrams in detail |
| (Manage) Chapter 4. Making changes to project documentation... | Edit documentation content to keep information up to date |
| (Manage) Chapter 5. Adding video content... | Embed video content to enhance documentation with media |
| (Manage) Chapter 6. Streamlining documentation builds... | Automate documentation builds with GitHub Actions to publish updates continuously |
| (TechDocs) Chapter 4. Creating a TechDocs add-on | Develop custom TechDocs add-ons to extend documentation functionality |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-21.md
