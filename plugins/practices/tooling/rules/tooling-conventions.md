---
description: Organisational tooling conventions — which tool for which function. Agents must reference these tools, not generic alternatives.
---

# Tooling Conventions

When recommending, configuring, or referencing tools, use the organisation's standard stack. Never suggest alternatives to adopted tools without an explicit evaluation request.

These are org **defaults**, and a project's `docs/tooling-register.md` is the source of truth that overrides them. Two things follow. A function only applies if the project actually has it — a backend service or a library has no frontend to host, so the Vercel default simply does not apply to it; don't push it in. And where the register records a choice, the register wins, no evaluation needed (the choice was already made when the register was written).

## Standard tools

| Function | Tool | NOT these |
|---|---|---|
| Source control | GitHub | GitLab, Bitbucket |
| Issue tracking | GitHub Issues | Jira, Linear, Trello, Asana |
| Code review | GitHub PRs + Claude Code | Gerrit, Crucible |
| CI/CD | GitHub Actions | CircleCI, Jenkins, GitLab CI, Travis |
| Team discussions / RFCs | GitHub Discussions | Confluence, Notion |
| Operational documentation | GitHub Wiki | Confluence, Notion |
| Frontend hosting | Vercel | Netlify, AWS Amplify, Cloudflare Pages |
| Code quality / SAST | SonarCloud | CodeClimate, Codacy, Snyk Code |
| Communication (real-time) | Microsoft Teams | Slack, Discord |
| Communication (async/external) | Microsoft Outlook | Gmail |
| Documents / spreadsheets | Microsoft 365 (Word, Excel, SharePoint) | Google Docs/Sheets |
| Task / calendar management | useMotion | Asana, Monday, Todoist |
| LLM API gateway | OpenRouter | Direct provider APIs (unless specific model required) |
| AI-powered research | Perplexity | Generic web search for research tasks |
| Accounting / finance | Xero | QuickBooks, MYOB |
| Domain / DNS | Gandi | Cloudflare, Route53 (for registration) |

## Rules

- **Check the tooling register first.** Before recommending any tool, check `docs/tooling-register.md` in the project. If a tool is adopted for that function, use it.
- **Never suggest alternatives to adopted tools** unless the user explicitly asks for an evaluation (use `/architect:evaluate-technology` for that).
- **GitHub is the hub.** Issues for tracking, PRs for review, Actions for CI/CD, Discussions for decisions, Wiki for operational docs. Do not fragment across multiple platforms.
- **Technical docs in-repo, operational docs in Wiki.** ADRs, specs, test strategies, architecture docs live in `docs/`. Runbooks, onboarding guides, team processes live in GitHub Wiki.
- **Tool changes require an ADR.** Switching an adopted tool requires a formal evaluation and decision record.

## GitHub conventions

- **Issues**: labelled by domain (`bug`, `feature`, `security`, `infrastructure`, `documentation`), assigned to responsible agent/role
- **PRs**: conventional commits, linked to issues via `Closes #N`, code-reviewer runs multi-pass review
- **Actions**: CI pipeline stages: lint → test → SonarCloud → deploy. DevOps owns pipeline definitions
- **Discussions**: used for RFCs, architecture decisions, requirement clarifications. Link resulting ADRs back to the discussion
- **Wiki**: operational docs, team processes, onboarding guides. NOT technical specs (those live in `docs/`)
