import json
import os
import time
import traceback
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def _build_langfuse_client() -> Langfuse | None:
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip()
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "").strip()
    host = (
        os.getenv("LANGFUSE_HOST")
        or os.getenv("LANGFUSE_BASE_URL")
        or "https://cloud.langfuse.com"
    )

    if not public_key or not secret_key:
        return None

    return Langfuse(public_key=public_key, secret_key=secret_key, host=host)


langfuse = _build_langfuse_client()


def is_langfuse_enabled() -> bool:
    return langfuse is not None


def coerce_for_langfuse(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Exception):
        return {
            "type": type(value).__name__,
            "message": str(value),
            "traceback": traceback.format_exception_only(type(value), value),
        }
    if isinstance(value, dict):
        return {str(k): coerce_for_langfuse(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [coerce_for_langfuse(item) for item in value]
    if hasattr(value, "model_dump"):
        return coerce_for_langfuse(value.model_dump())
    if hasattr(value, "dict"):
        return coerce_for_langfuse(value.dict())

    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


@contextmanager
def observe_span(
    name: str,
    *,
    input_data: Any | None = None,
    output_data: Any | None = None,
    metadata: dict | None = None,
    as_type: str = "span",
    model: str | None = None,
    provider: str | None = None,
    status_message: str | None = None,
) -> Iterator[Any]:
    if not is_langfuse_enabled():
        yield None
        return

    started_at = time.perf_counter()
    span_metadata = coerce_for_langfuse(metadata or {})
    if provider:
        span_metadata["provider"] = provider
    if model:
        span_metadata["model"] = model

    with langfuse.start_as_current_observation(
        name=name,
        as_type=as_type,
        input=coerce_for_langfuse(input_data),
        metadata=span_metadata,
        model=model,
        status_message=status_message,
    ) as observation:
        try:
            yield observation
        except Exception as exc:
            if observation is not None:
                observation.update(
                    output=coerce_for_langfuse({"error": str(exc)}),
                    metadata=coerce_for_langfuse({**span_metadata, "error": str(exc)}),
                    status_message=str(exc),
                )
            raise
        finally:
            if observation is not None:
                span_metadata["latency_ms"] = round(
                    (time.perf_counter() - started_at) * 1000, 2
                )
                observation.update(metadata=coerce_for_langfuse(span_metadata))
                if output_data is not None:
                    observation.update(output=coerce_for_langfuse(output_data))
            langfuse.flush()
