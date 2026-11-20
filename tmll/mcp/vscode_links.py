"""Helpers to build vscode:// links that open a trace in the Trace Viewer extension.

Matches the `/open` URI handler of the vscode-trace-extension:
    vscode://eclipse-cdt.vscode-trace-extension/open?trace=<abs path>&output=<id>&start=<ns>&end=<ns>
"""
from typing import Optional
from urllib.parse import urlencode

import pandas as pd

VSCODE_TRACE_EXTENSION_ID = "eclipse-cdt.vscode-trace-extension"


def to_ns(ts) -> int:
    """Convert a timestamp (pd.Timestamp/str/datetime) to absolute nanoseconds since the epoch."""
    return int(pd.Timestamp(ts).value)


def build_open_uri(trace_path: Optional[str], output_id: Optional[str] = None,
                   start_ns: Optional[int] = None, end_ns: Optional[int] = None) -> Optional[str]:
    """Build a vscode:// URI, or None if the trace path is unknown/not absolute."""
    if not trace_path or not trace_path.startswith("/"):
        return None
    params = {"trace": trace_path}
    if output_id:
        params["output"] = output_id
    if start_ns is not None:
        params["start"] = str(start_ns)
        if end_ns is not None and end_ns >= start_ns:
            params["end"] = str(end_ns)
    return f"vscode://{VSCODE_TRACE_EXTENSION_ID}/open?{urlencode(params)}"


def experiment_trace_path(experiment) -> Optional[str]:
    """Path of the first trace of an experiment (the URI handler opens one trace path)."""
    for trace in getattr(experiment, "traces", None) or []:
        if getattr(trace, "path", None):
            return trace.path
    return None


def output_ids_by_name(outputs) -> dict:
    """Map output display name -> output id (series in AnomalyDetection are keyed by name)."""
    return {o.name: o.id for o in outputs or []}
