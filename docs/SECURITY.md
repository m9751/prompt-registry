# Security Policy

## CI/CD Authentication (GITHUB_TOKEN)

For GitHub Actions workflows in this repository, use the **auto-provisioned `GITHUB_TOKEN`**. No setup required — GitHub injects it automatically per workflow run.

The workflow requests only the minimum permissions needed:
- `pages: write` — required for GitHub Pages deployment
- `id-token: write` — required for OIDC-based Pages deployment
- `contents: read` — implicit default for checkout

Never create a PAT for CI/CD if `GITHUB_TOKEN` covers the use case.

---

## External Read Access (Fine-Grained PAT)

For external applications, agents, or LLMs that need to fetch prompts programmatically from the GitHub API (not via the public GitHub Pages URL), issue a **Fine-Grained Personal Access Token** with these exact constraints:

### Token Configuration

| Setting | Required value |
| :--- | :--- |
| **Resource owner** | `m9751` |
| **Repository access** | **Only select repositories** → `prompt-registry` only |
| **Metadata permission** | Read-only |
| **Contents permission** | Read-only |
| **All other permissions** | No access |

### Expiration Policy

- **Maximum 90-day expiration.** Never issue a token with > 90 days validity.
- **Calendar reminder required.** When issuing a token, immediately set a reminder to rotate it 1 week before expiration.
- **Rotate immediately** on any team member departure, regardless of expiration date.

### Where to Store the Token

- **Never** commit a PAT to any file in this repository.
- **Never** store it in an `.env` file committed to git.
- Store it in your application's secret management system (e.g., GitHub Actions Secrets, AWS Secrets Manager, 1Password).

### Enterprise Organization Note

If this repository moves to an enterprise GitHub organization, tokens may require **organization-level admin approval** before they can be issued. Coordinate with your GitHub org admin in advance.

---

## Public Endpoint (No Auth Required)

The compiled `prompts_latest.json` is deployed to GitHub Pages and is **publicly accessible** without authentication:

```
https://m9751.github.io/prompt-registry/prompts_latest.json
```

This is intentional. The prompts in this registry are internal frameworks but not sensitive secrets. If that changes, disable GitHub Pages and require PAT-authenticated API access instead.

---

## Reporting Security Issues

Open a private GitHub Security Advisory at: `https://github.com/m9751/prompt-registry/security/advisories/new`
