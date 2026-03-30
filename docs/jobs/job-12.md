# Job 12 — Manage authorization and permissions

## Metadata

| Field | Value |
| --- | --- |
| Category | Secure |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #12 |
| Status | Not started |

## Job statement

When managing access, I want to define roles and permission policies so that I can control exactly which actions users can perform on platform resources.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 1. Enabling ... access to the RBAC feature | Enable the RBAC feature to restrict access to authorized users |
| Chapter 4. Managing RBAC using the ... Web UI | Manage roles via the Web UI to configure permissions visually |
| 4.1. Creating a role... | Create roles to group users with shared responsibilities |
| 4.2. Editing a role... | Edit role details to update permission scopes |
| Chapter 5. Managing authorizations by using the REST API | Manage authorizations via the REST API to automate access controls |
| 5.1. Sending requests... by using the curl utility | Send API requests via curl to test permission updates |
| Chapter 6. Managing authorizations by using external files | Define policies in external files to manage permissions as code (GitOps) |
| 6.1. Defining authorizations ... by using the Operator | Define policies via the Operator to enforce immutable permissions |
| 6.2. Defining authorizations ... by using Helm | Define policies via Helm to streamline deployment configuration |
| Chapter 8. Delegating RBAC access | Delegate RBAC access to empower team leads with scoped permissions |
| 8.1. Delegating ... by using the web UI | Delegate access via the UI to allow self-service team management |
| Chapter 10. Conditional policies | Define conditional policies to grant dynamic access based on ownership |
| 10.1. Enabling transitive parent groups | Enable transitive ownership to support complex group hierarchies |
| Chapter 7. Configuring guest access with RBAC UI | Configure guest access with RBAC to test policies in development |
| Chapter 9. Permission policies reference | Reference permission policies to identify available resource actions |
| Chapter 11. User statistics | View user statistics to audit active platform usage |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-12.md
