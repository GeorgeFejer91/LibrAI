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

## D-0004 — Supported LibreOffice versions

- Date: 2026-10-19
- Status: Superseded by D-0007
- Context: LibreOffice uses year.month branches. At decision time the maintained branch is 26.2 (26.2.4 at 2026-10); the 25.8 branch reached end of life on 2026-06-12 and older branches are unsupported. The development machine runs Debian trixie's LibreOffice 25.2.3.2 (an EOL branch) with python3-uno 25.2.3; no supported branch is installable from its configured repositories.
- Decision: The minimum supported branch for LibrAI releases is LibreOffice 26.2. EOL branches are not supported targets. Extension code must stay within the extension/UNO API surface that is stable across the supported branch. Local 25.2 runs count as development evidence with that version caveat, never as release verification.
- Consequences: The M7 parity-release gate requires checks on a supported (26.2+) installation. Update this entry if TDF's branch support changes.
- Supersedes: None

## D-0005 — Packaging tool: dependency-free build-oxt.py

- Date: 2026-10-19
- Status: Superseded by D-0007
- Context: D-0003 left the packaging tool undecided until the first packaging task (M1).
- Decision: `tools/build-oxt.py` assembles `dist/librai-<version>.oxt` from the `extension/` tree using only the Python 3 standard library (`zipfile`), with a fixed entry timestamp for reproducible builds. The version comes from `extension/Scripts/python/librai/__init__.py` (`__version__`).
- Consequences: Building requires only python3; no Ant, Maven, Gradle, Make, or Node toolchain. Built artifacts live in git-ignored `dist/`; releases attach the artifact instead of committing it. Replace only if a real need appears (signing, multi-part packages).
- Supersedes: None

## D-0006 — Test harness: UNO pipe client plus scratch-profile install

- Date: 2026-10-19
- Status: Superseded by D-0007
- Context: D-0003 left the test harness undecided until implementation. No LibreOffice-specific implementation skill is installed, so checks must run locally against the installed LibreOffice.
- Decision: `tests/m1/run.sh` builds the extension, installs it into a scratch user profile under `.for-ai-local/` with `unopkg`, starts a headless `soffice` on a named URP pipe with that profile, and runs `tests/m1/check_m1.py`, a `python3-uno` client asserting (1) extension registration by identifier, (2) the Writer menu configuration node, and (3) script execution through the ScriptProviderForPython. Teardown removes the profile. Later milestones extend this pattern per capability.
- Consequences: Real host-level evidence on the installed LibreOffice without a display. Headless mode cannot visually confirm menu rendering; that stays a manual visual check plus the configuration-node assertion. CI is not configured; the harness is the local gate.
- Supersedes: None

## D-0007 — Port the wrAIter Writer add-on as the LibrAI product

- Date: 2026-10-19
- Status: Accepted
- Context: `undertree_texstudio/modules/libreoffice` already implements the complete WordPlai baseline (24-color rules, protection/reject/discard, complete document context, MCP/zrok transport, direct authorized edits, persistence, native review) as wrAIter 0.4.1 with an extensive test suite. Both repositories are the same owner's work. Building from scratch would duplicate months of verified implementation.
- Decision: Adopt that codebase as the LibrAI product, ported into this repository at the root (`extension/`, `tests/`, `build.py`, `assets/librai/`). Rebrand user-visible surfaces to LibrAI (menus, dialogs, MCP `serverInfo`, undo titles, publisher), switch installation identities to `org.librai` / `vnd.librai:` / `org.librai.*` config nodes, rename modules to `librai_*.py`, and reset the version to 0.1.0. Keep the document persistence format unchanged (`UnderTree_` bookmark names, `UnderTreeReviewV1` metadata property, limits) and the `undertree-connection` profile filename so documents and connection profiles created by wrAIter keep working; keep the legacy peer `serverInfo` names accepted for pairing and add `wordplai`. The `LibreOffice-minimal-version` metadata stays 7.6 (technical floor from the ported code); releases are only claimed for TDF-maintained branches (26.2+ at decision time), superseding D-0004. Prose that described pairing with UnderTree now describes pairing with WordPlai, matching WordPlai's actual semantics (complete current Word document, unsaved text included; MCP reads/edits do not invoke Save). The ported deterministic `build.py` replaces D-0005's packager and the ported test suite replaces D-0006's harness.
- Consequences: The ported test suite is the primary verification gate. Versioned verification history in the package README remains attributed to wrAIter. Known host-version limits on the local EOL LibreOffice 25.2 are recorded in [`VERIFICATION.md`](./VERIFICATION.md), not worked around. The repository needs a license decision (the source repository has none); this entry does not choose one.
- Supersedes: D-0004, D-0005, D-0006

## D-0008 — MIT license

- Date: 2026-10-19
- Status: Accepted
- Context: D-0007 left the repository license undecided; the repository is public and ships a `.oxt`.
- Decision: License the repository under the MIT license, copyright "LibrAI contributors". The license file ships inside the `.oxt` alongside the unchanged bundled third-party notices (`zrok-LICENSE.txt`, optional MinGit runtime).
- Consequences: Third-party components retain their own licenses; `build.py` must keep embedding `LICENSE` and the notices. Change requires a new superseding decision.
- Supersedes: None

## D-0009 — Performance policy: measured UNO costs, rejected controller locking

- Date: 2026-10-19
- Status: Accepted
- Context: The user asked whether a native (C++/Rust) implementation was warranted and proposed measuring the real user-perceived path before changing languages. Measured on the development host (LO 25.2.3.2 headless, ~300-paragraph synthetic document, external UNO socket client): a full read is ~40-70 ms and the local HTTP transport adds <1 ms; the dominant cost is LibreOffice's own re-formatting of dirty text regions after mutations (a bookmark insert at document start ~1.5 s, at document end ~11 ms — position-dependent), while single UNO round trips and Python marshalling are single-digit milliseconds.
- Decision: Keep the Python-UNO extension. Do not introduce C++ or Rust unless a benchmark demonstrably attributes a bottleneck to the language layer. A `ControllerLock` (`lockControllers`) experiment around the four mutation paths was implemented, measured, and reverted: it relocated the intrinsic formatting cost to the next model access (a read became ~2.6 s after a locked early mutation) without reducing total work, so it stays out of the synchronous MCP flow. Optimization work targets the workload instead: fewer dirty-region invalidations per logical edit, an incremental document representation with revision-gated validation, and re-measurement through `tests/bench_read_apply.py`.
- Consequences: Performance claims require benchmark evidence. When the incremental representation lands, add an end-to-end latency criterion to the M7 gate. Revisit language choice only with new measurements.
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
