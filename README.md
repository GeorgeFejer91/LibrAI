# LibrAI

LibrAI is the LibreOffice Writer counterpart to [WordPlai](https://github.com/GeorgeFejer91/wordplai). The project goal is equivalent user-facing functionality across both editors, with host-native implementation protocols for each.

**Project page:** https://georgefejer91.github.io/LibrAI/

## Status

The Writer extension is implemented as a Python-UNO add-on (LibrAI 0.1.0),
ported from the wrAIter 0.4.1 Writer add-on ([D-0007](for-ai/DECISIONS.md)) and
rebranded: 24 color rules, local marking, protect/reject/discard rules,
complete document context, an in-process MCP server with a zrok2 bridge,
direct authorized edits, ODT persistence, and native Undo/Track Changes
semantics. Documents and connection profiles created by wrAIter keep working;
the persistence format is unchanged.

Verified on the development host (LibreOffice 25.2.3.2 headless, python3-uno):
137 pure tests pass (2 Windows-only skips), the `.oxt` builds and installs,
and the base UNO smoke, peer-catalogue, connections-access and dialog-layout
smokes pass. Protected-fragment reconstruction and display-metric checks on
this EOL branch are recorded as known limits in
[`for-ai/VERIFICATION.md`](for-ai/VERIFICATION.md); parity is not claimed until
the M7 gate passes on a supported LibreOffice branch with WordPlai.

## Build and test

Requires LibreOffice with Python UNO (`python3-uno`), `soffice`, and `unopkg`.

```bash
python3 build.py                                     # builds artifacts/librai/LibrAI.oxt
python3 -m unittest discover -s tests -p 'test_*.py' # pure test suite
```

Install the `.oxt` in LibreOffice via **Tools → Extensions → Add** (or
`unopkg`), restart Writer, and use the **LibrAI** menu/toolbar. See
[`extension/README.md`](extension/README.md) for the user flow and
[`for-ai/VERIFICATION.md`](for-ai/VERIFICATION.md) for the UNO smoke gates.

## Structure

- `extension/` — `.oxt` contents (UNO component, protocol handler, toolbar controllers, dialogs)
- `tests/` — pure unit tests and real-UNO smoke tests
- `build.py` — deterministic, standard-library-only package builder
- `assets/librai/` — application icons
- `for-ai/` — AI control plane, parity contract, decisions, verification gates

The shared feature baseline and parity rules are in
[`for-ai/CROSS-PLATFORM-COMPATIBILITY.md`](for-ai/CROSS-PLATFORM-COMPATIBILITY.md).

## License

Not yet chosen; see D-0007 in [`for-ai/DECISIONS.md`](for-ai/DECISIONS.md).
