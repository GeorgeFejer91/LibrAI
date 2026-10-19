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

Status: M1–M6 code arrived complete via the [D-0007](./DECISIONS.md) port of the wrAIter 0.4.1 Writer add-on and passes its pure test suite locally; real-UNO verification passes on the development host except the recorded host-version and display-metric limits in [`VERIFICATION.md`](./VERIFICATION.md). Remaining work: verification on a supported LibreOffice branch (26.2+), Windows UI/install checks, the public zrok/ChatGPT client gate, and the M7 cross-platform parity gate.

A milestone is complete only when its checks are VERIFIED, never when its code merely exists. Milestones are a durable goal ladder, not a schedule; scope, not dates, orders the work.

## Current deliverable

The product is the ported and rebranded Writer extension (LibrAI 0.1.0, wrAIter 0.4.1 lineage). Parity with WordPlai is a goal verified incrementally; it is not yet a completed-capability claim.

## Non-goals

- No speculative framework, service, abstraction, compatibility layer, or
  deployment system.
- No second implementation tree or duplicate source of truth.
- No capability claim without matching evidence.

Add project-specific non-goals only after they prevent a plausible wrong turn.

## Product/control-plane boundary

- Product source and deliverables: `extension/` (`.oxt` contents), `tests/`, `assets/librai/`, and the root `build.py`. Built artifacts go to git-ignored `dist/` and `artifacts/`.
- Agent orchestration and durable project memory: `for-ai/`.
- Local generated diagnostics and scratch evidence: `.for-ai-local/` (ignored).

## Architecture and ownership

The Writer host is a Python-UNO extension per [D-0003](./DECISIONS.md), ported from the wrAIter 0.4.1 codebase per [D-0007](./DECISIONS.md): a registered UNO component (`librai_writer.py`) with a protocol handler (`vnd.librai:*`), toolbar controllers, and a Writer menu/toolbar (`Addons.xcu`). Document rules, marks and pending suggestions persist in ODT metadata; the MCP server runs in-process with a zrok2 bridge; pairing accepts WordPlai endpoints. WordPlai's C#/COM/WinForms implementation is a behavioral reference only; no native API or storage format is shared.

## Current verified state

- Repository initialized 2026-10-19; control plane and public page live.
- Writer extension ported and rebranded to LibrAI 0.1.0 (see D-0007); `python3 build.py` produces a deterministic `.oxt`.
- On the development host (LibreOffice 25.2.3.2 headless, python3-uno): 137 pure tests pass (2 Windows-only skips); the `.oxt` installs and its protocol registers; the base UNO smoke (markers, metadata reopen, Unicode, formatting, suggestion approval, direct permission, overlaps, stale rejection, isolation, popup, HTTP callbacks, revocation), peer-catalogue, connections-access and dialog-layout smokes pass. Recorded limits: protected-fragment reconstruction cases and the consent no-fit check fail on this EOL branch / headless display (identical failures reproduced with the original wrAIter code); see [`VERIFICATION.md`](./VERIFICATION.md).
- The repository is MIT-licensed per [D-0008](./DECISIONS.md); the license ships inside the `.oxt`.

Git and runnable checks are the authority for branch, revision, and behavior.
Do not turn this section into a second status ledger.
