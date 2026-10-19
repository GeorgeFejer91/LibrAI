# Decision log

Record only durable choices whose rationale future agents would otherwise have
to rediscover. Source and tests remain the authority for implementation facts.

## D-0001 — Minimal control plane before product scaffolding

- Date: 2026-10-19
- Status: Accepted
- Context: The project needs a predictable AI entrypoint without choosing an
  application stack or inventing product structure prematurely.
- Decision: Use a short root `AGENTS.md` that routes to a lowercase `for-ai/`
  control plane. Keep product output outside that folder and add project files,
  skills, and protocols only for current requirements.
- Consequences: New agents get a reliable map and readiness gates. The first
  product task must still choose the smallest suitable output structure.
- Supersedes: None

## D-0002 — Cross-platform feature parity with WordPlai

- Date: 2026-10-19
- Status: Accepted
- Context: LibrAI is the LibreOffice Writer counterpart to WordPlai, and the user requires every function in either sibling to be fulfilled by the other.
- Decision: Treat equivalent user-facing behavior, user control, safeguards, and evidence as a release requirement in both directions. Permit host-native implementation protocols, UI, and storage to differ. Keep capability gaps explicit and incomplete until both hosts meet the shared contract.
- Consequences: Update the parity contract in both repositories when the shared baseline changes, and verify each host independently. See [`CROSS-PLATFORM-COMPATIBILITY.md`](./CROSS-PLATFORM-COMPATIBILITY.md) in both repositories.
- Supersedes: None

## D-0003 — Python-UNO for the Writer extension host

- Date: 2026-10-19
- Status: Accepted
- Context: Writer extensions can use Basic, Python, JavaScript, Java, BeanShell, or C++ through the UNO component API. WordPlai's C#/COM/WinForms code is a behavioral reference only.
- Decision: Build the Writer product as a Python-UNO extension packaged as an `.oxt`, using the Python runtime bundled with LibreOffice, with menus declared through `Addons.xcu`. The AI/MCP transport, persistence format, and packaging tool remain undecided until a focused task selects them.
- Consequences: No separate runtime or build toolchain is required to start. Document access goes through UNO, so tracked changes, comments, and undo must be verified in Writer itself. Revisit if a required host capability is unavailable from Python-UNO.
- Supersedes: None

## Record format

For later decisions, add one compact entry with:

- identifier and title;
- date and status (`Proposed`, `Accepted`, `Superseded`, or `Rejected`);
- context;
- decision;
- consequences;
- supersession link when applicable.

Do not rewrite accepted history to hide a changed direction. Add a superseding
decision and link both entries.
