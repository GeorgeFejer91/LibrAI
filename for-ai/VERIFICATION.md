# Verification and readiness gates

Evidence must match the claim. Missing dependencies, credentials, hardware, or
runtime access produce `BLOCKED` or `NOT RUN`, never `VERIFIED`.

## Result vocabulary

- `VERIFIED`: the named check directly observed the claimed surface and passed.
- `PARTIAL`: some required evidence passed and the missing scope is named.
- `BLOCKED`: a concrete external or authority blocker prevented the check.
- `NOT RUN`: the check was intentionally not applicable or not attempted, with
  the reason stated.

## Gate 0: bootstrap readiness

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File for-ai/scripts/check-context.ps1 -ProjectRoot . -RequireRemote
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Pass when the context checker succeeds, the intended tree is clean, and local
`HEAD` equals `origin/main`.

## Gate 1: task contract

Before implementation, name:

- the observable user outcome;
- affected product surface and owner;
- acceptance criteria;
- focused check that can fail for the requested behavior;
- broader checks required by affected boundaries;
- explicitly deferred work.

## Gate 2: focused change

Run the narrowest real check for the change. Add the exact commands here when
the project selects its stack. A syntax check proves syntax; a unit test proves
its tested logic; neither proves UI, deployment, hardware, performance, safety,
or scientific validity unless it directly observes that surface.

## Gate 3: integrated readiness

Run proportionate build, test, lint, type, runtime, visual, device, security,
and compatibility checks for every affected boundary. Do not run an expensive
or irrelevant full matrix for a documentation-only edit.

## Writer extension gates

From the repository root (requires python3 with the `uno` module, `soffice`,
and `unopkg` on PATH):

```bash
python3 build.py                                     # deterministic .oxt into artifacts/librai/
python3 -m unittest discover -s tests -p 'test_*.py' # pure suite, no display needed
```

Real-UNO smokes run against a disposable headless Writer with the built
extension installed in a scratch profile:

```bash
unopkg -env:UserInstallation="file://$PWD/.for-ai-local/uno-profile" add --suppress-license artifacts/librai/LibrAI.oxt
soffice --headless --norestore --nologo --nofirststartwizard \
  -env:UserInstallation="file://$PWD/.for-ai-local/uno-profile" \
  --accept="socket,host=127.0.0.1,port=2087;urp;StarOffice.ComponentContext" &
LIBRAI_WRITER_EXTENSION_SOURCE="$PWD/extension" python3 tests/uno_smoke.py --port 2087 --output .for-ai-local/uno-smoke.odt --extension-check
```

Note the `-env:` option must precede the unopkg command; after the command it
is ignored and the extension installs into the real user profile instead.
`uno_smoke.py` runs the contract verification first, which is blocked on the
local EOL branch (below); the remaining `run()` behaviors can be exercised
with the scratch driver pattern that stubs only that verification.

Known limits on the development host (LibreOffice 25.2.3.2, headless,
python3-uno 25.2.3), reproduced identically with the original wrAIter 0.4.1
code, so they are host-version/display limits rather than port regressions:

- `uno_contract_smoke` protected-fragment reconstruction cases and
  `uno_highlighting_smoke` fail in `Session.apply` (native protected insertion
  changes reconstructed or surrounding text).
- `uno_pending_rejection_lifecycle` reaches the same `apply` path.
- `uno_consent_smoke` no-fit share-button state assert fails without display
  metrics.
- `uno_dropdown_smoke` is blocked on the `pending-reopen.odt` fixture produced
  by the blocked contract smoke.
- Pure `test_connection` subprocess checks spawn soffice without an isolated
  profile; on Linux that touches the real user profile.

These limits must not be presented as completed capabilities. The M7 release
gate requires rerunning the blocked smokes on a supported branch (26.2+) with
a display before parity is claimed.

## Performance evidence

`tests/bench_read_apply.py` measures the read and mutation paths against a
disposable soffice (see its docstring). Recorded on the development host on
2026-10-19 (LO 25.2.3.2 headless, 300-paragraph synthetic document): full
reads ~40-70 ms, HTTP transport <1 ms; mutation cost is dominated by
LibreOffice's own re-formatting of dirty text regions (position-dependent,
~1.5 s for a document-start bookmark insert, ~11 ms at document end). A
`lockControllers` experiment was measured and rejected (cost relocation, no
net win in the synchronous flow); see [D-0009](./DECISIONS.md). Any
performance change must re-run this benchmark and report before/after
numbers; language-layer rewrites additionally need evidence that a measured
bottleneck is attributable to Python marshalling.

## Gate 4: publication

1. Review status and diff; preserve unrelated changes.
2. Confirm only intended paths are staged.
3. Confirm all required gates passed or are honestly reported.
4. Create one coherent commit under normal repository policy.
5. Push without force and without bypassing protection or secret scanning.
6. Verify the remote commit and required CI/deployment for that exact SHA.

## Cross-platform parity gate

For any change to a shared capability, update the contract in both repositories when needed and run the affected behavior checks independently on Writer and Word. A pass on one host does not qualify the other. A parity release is blocked while a shared capability is missing or unverified on either supported host; see [`CROSS-PLATFORM-COMPATIBILITY.md`](./CROSS-PLATFORM-COMPATIBILITY.md).

## Current public page

- The repository root `index.html` is the GitHub Pages source (`main` / `/`).
- Verify the page returns HTTP 200 and identifies LibrAI, its WordPlai
  relationship, the parity goal, and the current verified implementation state
  without claiming unverified parity.
- A public page deployment does not verify a LibreOffice add-in or feature
  parity.

## Handoff evidence

Report exact commands or observed surfaces, results, untested scope, commit SHA,
remote synchronization, CI/deployment state, and whether `for-ai/` changed.
