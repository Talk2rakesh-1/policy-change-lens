import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from change_lens import __version__
from change_lens.engine import compare_documents, search_document
from change_lens.models import CompareRequest, CompareResponse, QueryRequest, SearchHit

logging.basicConfig(level="INFO", format="%(levelname)s %(message)s")
logger = logging.getLogger("change_lens")

app = FastAPI(
    title="ChangeLens",
    version=__version__,
    description="Local-first, evidence-linked document change intelligence.",
)


@app.middleware("http")
async def request_metrics(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "request method=%s path=%s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/v1/compare", response_model=CompareResponse)
def compare(request: CompareRequest) -> CompareResponse:
    return compare_documents(request)


@app.post("/v1/search", response_model=list[SearchHit])
def search(request: QueryRequest) -> list[SearchHit]:
    return search_document(request.document.content, request.query, request.limit)
