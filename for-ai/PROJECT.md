# Project contract

## Purpose

LibreOffice Writer counterpart to WordPlai, with equivalent user-facing writing-assistant capabilities implemented through LibreOffice-native protocols.

## Primary goal

Deliver a LibreOffice Writer product with equivalent user-facing functions to WordPlai. Every user-facing function in either sibling must be fulfilled in the other, with each host using its own appropriate implementation protocols. The complete shared behavioral baseline and parity rules are in [`CROSS-PLATFORM-COMPATIBILITY.md`](./CROSS-PLATFORM-COMPATIBILITY.md).

## Definition of done

This repository is finished when:

1. The Writer extension installs and runs on the supported LibreOffice versions through a documented packaging path.
2. Every capability row in the shared baseline (see [`CROSS-PLATFORM-COMPATIBILITY.md`](./CROSS-PLATFORM-COMPATIBILITY.md)) is implemented Writer-natively and verified on Writer with recorded evidence.
3. The cross-platform parity gate passes: each shared capability is verified independently on both hosts, and no platform gap is presented as complete.
4. The public page, root README, and control plane match the verified state.

## Milestone ladder

- **M1 — Installable skeleton**: `.oxt` package with `Addons.xcu` menus that loads in Writer, plus a local test harness and packaging script.
- **M2 — Document access core**: list/open documents by name, read complete document context (text, comments, revisions), conversation target isolation.
- **M3 — Local passage rules**: marking, color/name/prompt/function rules, persistence across save/reopen.
- **M4 — AI connection**: MCP transport, conversations, ordered operations, stale-context refusal, safe retry.
- **M5 — Authorized wording changes**: edits inside user-authorized prose, native tracked changes/comments, concise rationale and protected completion marking.
- **M6 — Protection and review rules**: preserve-text, reject, discard, prompt editing, overlap precedence; AI highlighting/recoloring; scope and safety boundaries.
- **M7 — Parity release**: full baseline verified on Writer and Word, parity gate passed, public claims updated.

A milestone is complete only when its checks are VERIFIED, never when its code merely exists. Milestones are a durable goal ladder, not a schedule; scope, not dates, orders the work.

## Current deliverable

The bootstrap deliverable (public project page and project control plane) is complete. Product implementation starts at M1; parity is a project goal, not a current capability claim.

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

The Writer host is a Python-UNO extension (`.oxt`, `Addons.xcu` menus) per [D-0003](./DECISIONS.md). Supported Writer versions, document-model integration, persistence, AI/MCP transport, packaging tool, and test harness remain **Undecided**; select them from current LibreOffice documentation before product code. WordPlai’s C#/COM/WinForms implementation is a behavioral reference only; do not assume its native APIs or storage transfer to Writer.

## Current verified state

- Fresh Git repository initialized on 2026-10-19.
- AI control plane created and mechanically checked.
- No LibreOffice product implementation has been scaffolded. The public page and parity control plane are the only current project deliverables.

Git and runnable checks are the authority for branch, revision, and behavior.
Do not turn this section into a second status ledger.
