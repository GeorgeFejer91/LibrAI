"""Read/apply latency benchmark for the Writer extension (see D-0009).

Run against a disposable headless soffice:

    soffice --headless -env:UserInstallation=file:///tmp/bench-profile \
        --accept="socket,host=127.0.0.1,port=2090;urp;StarOffice.ComponentContext" &
    LIBRAI_WRITER_EXTENSION_SOURCE="$PWD/extension" python3 tests/bench_read_apply.py 2090

Reports p50/p95 milliseconds for a ~300-paragraph synthetic document:
  - full read_manuscript (clean and after a small edit)
  - mark + read + direct suggestion apply cycle

Known results on LO 25.2.3.2 headless (2026-10-19): reads ~40-70 ms; the
cycle is dominated by LibreOffice's own re-formatting of dirty text regions
after mutations, not by the Python layer (see for-ai/DECISIONS.md D-0009).
"""
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extension"))
import uno  # noqa: E402
from librai_writer import Session  # noqa: E402
from librai_policy import defaults  # noqa: E402


def percentile(samples, q):
    samples = sorted(samples)
    return samples[int(len(samples) * q) - 1]


def measure(label, fn, n=10):
    samples = []
    for _ in range(n):
        start = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - start) * 1000)
    print("%-32s n=%d  p50=%.1f ms  p95=%.1f ms" % (label, n, percentile(samples, 0.5), percentile(samples, 0.95)))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 2090
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    context = resolver.resolve("uno:socket,host=127.0.0.1,port=%d;urp;StarOffice.ComponentContext" % port)
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    document = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
    text = document.Text
    for i in range(300):
        text.insertString(text.End, "Paragraph %d. The complete native text of this synthetic section describes ordinary prose " % i
                          + "with a repeating sentence body for stable extraction volume. " * 4 + "\n", False)
    session = Session(context, document)
    session.set_shared(True)
    session.start()
    session.save_rule("bench", dict(defaults()["rules"]["snappier"], mode="direct"))
    doc_id = session.document_id

    measure("read clean", lambda: session.call("read_manuscript", {"documentId": doc_id}))
    text.insertString(text.End, "x", False)
    measure("read after small edit", lambda: session.call("read_manuscript", {"documentId": doc_id}))

    def cycle():
        cursor = text.createTextCursor()
        cursor.gotoEnd(False)
        cursor.goLeft(5, True)
        document.CurrentController.select(cursor)
        marker = session.mark_selection("bench")
        snapshot = session.call("read_manuscript", {"documentId": doc_id})
        item = next(item for item in snapshot["markers"] if item["id"] == marker)
        payload = {"documentId": doc_id, "proposal": {
            "requestId": "bench-" + uuid.uuid4().hex, "revision": snapshot["revision"],
            "contextId": snapshot["contextId"],
            "from": item["from"], "to": item["to"], "quote": item["text"], "replacement": "Bench ",
            "rationale": "benchmark"}}
        result = session.call("suggest_text", payload)
        assert result.get("status") == "applied", result

    measure("mark+read+apply cycle", cycle, n=6)
    session.stop()
    session.close()
    document.setModified(False)
    document.close(True)
    print("BENCH DONE")


if __name__ == "__main__":
    main()
