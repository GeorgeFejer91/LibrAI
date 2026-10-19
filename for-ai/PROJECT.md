# Project contract

## Purpose

LibreOffice Writer counterpart to WordPlai, with equivalent user-facing writing-assistant capabilities implemented through LibreOffice-native protocols.

## Primary goal

Deliver a LibreOffice Writer product with equivalent user-facing functions to WordPlai. Every user-facing function in either sibling must be fulfilled in the other, with each host using its own appropriate implementation protocols. The complete shared behavioral baseline and parity rules are in [`CROSS-PLATFORM-COMPATIBILITY.md`](./CROSS-PLATFORM-COMPATIBILITY.md).

The current deliverable is limited to this public project page and the project control plane. Product implementation has not started; parity is a project goal, not a current capability claim.

## Non-goals

- No speculative framework, service, abstraction, compatibility layer, or
  deployment system.
- No second implementation tree or duplicate source of truth.
- No capability claim without matching evidence.

Add project-specific non-goals only after they prevent a plausible wrong turn.

## Product/control-plane boundary

- Product source and deliverables: outside `for-ai/`; exact roots are
  **Undecided until the first deliverable selects them**.
- Agent orchestration and durable project memory: `for-ai/`.
- Local generated diagnostics and scratch evidence: `.for-ai-local/` (ignored).

## Architecture and ownership

The LibreOffice extension API, supported Writer versions, document-model integration, persistence, AI/MCP transport, packaging, build stack, and implementation protocols are **Undecided**. Research and select these from current LibreOffice documentation before product code. WordPlai’s C#/COM/WinForms implementation is a behavioral reference only; do not assume its native APIs or storage transfer to Writer.

## Current verified state

- Fresh Git repository initialized on 2026-10-19.
- AI control plane created and mechanically checked.
- No LibreOffice product implementation has been scaffolded. The public page and parity control plane are the only current project deliverables.

Git and runnable checks are the authority for branch, revision, and behavior.
Do not turn this section into a second status ledger.
