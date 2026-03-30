# Job 11 — Configure authentication providers

## Metadata

| Field | Value |
| --- | --- |
| Category | Secure |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #11 |
| Status | Not started |

## Job statement

When setting up the platform, I want to configure authentication providers so that I can verify user identities against my organization's existing directories.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 1. Understanding authentication... | Overview of authentication concepts to plan user provisioning strategies |
| Chapter 2. Authenticating with the Guest user | Enable Guest access to explore features without external providers |
| Chapter 3. Authenticating with Red Hat Build of Keycloak (RHBK) | Configure Keycloak authentication to centralize identity management |
| 3.2. Enabling user provisioning with LDAP | Provision users from LDAP to synchronize directory groups |
| 3.3. Creating a custom transformer... | Customize user provisioning logic to map complex identity data |
| Chapter 4. Enabling authentication with GitHub | Configure GitHub authentication to enable login via GitHub organizations |
| 4.1. Enabling user authentication with GitHub... | Configure GitHub identity providers to sync users and teams |
| Chapter 5. Authenticating with Microsoft Azure | Configure Microsoft Azure authentication to integrate with corporate Entra ID |
| 5.2. Customizing the Microsoft authentication provider | Customize the Azure provider to filter tenants and scopes |
| Chapter 6. Troubleshooting authentication issues | Troubleshoot authentication issues to resolve login errors |
| 6.1. Reducing the size of issued tokens | Reduce token size to prevent HTTP header overflow errors |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-11.md
