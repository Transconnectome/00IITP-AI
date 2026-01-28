# 00. Security & Privacy Rules

## 1. Data Protection

- **No Private Data Leak**: Do not upload unpublished data or private keys/access tokens to external services without explicit user permission.
- **RFP Confidentiality**: Treat `docs/00_task_description/` contents as confidential. Do not summarize specific budget/personal details in public contexts.
- **Masking**: Automatically mask any detected API keys (sk-...) or passwords in log files (`_ops/logs/`).

## 2. Tool Safety

- **MCP Declaration**: Before calling crucial MCP tools (like git push, or bulk file edits), declare intent:
  > "Calling [ToolName] to [Purpose]. Input: [Brief Spec]. Side Effect: [Change Description]."
- **FileSystem Access**: Strict restriction to Project Root (`/Users/jiookcha/Documents/git/00IITP-AI`). No `../` navigation.

## 3. Git Practices

- **Commit Messages**: Use conventional commits (feat: , fix: , docs: ) + "[NeuroX]" prefix.
- **Branching**: `main` is protected. Use `feature/` or `draft/` branches for major edits.
