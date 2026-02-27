import asyncio
from re import Pattern
from typing import Optional, Union
from urllib.parse import parse_qsl, urlencode

from aiohttp import RequestInfo, StreamReader
from aiohttp.client_proto import ResponseHandler
from multidict import MultiDict
from yarl import URL


def stream_reader_factory(  # noqa
    loop: "Optional[asyncio.AbstractEventLoop]" = None,
) -> StreamReader:
    protocol = ResponseHandler(loop=loop)
    return StreamReader(protocol, limit=2**16, loop=loop)


def merge_params(url: "Union[URL, str]", params: dict | None = None) -> "URL":
    url = URL(url)
    if params:
        query_params = MultiDict(url.query)
        query_params.extend(url.with_query(params).query)
        return url.with_query(query_params)
    return url


def normalize_url(url: "Union[URL, str]") -> "URL":
    """Normalize url to make comparisons."""
    url = URL(url)
    return url.with_query(urlencode(sorted(parse_qsl(url.query_string))))


try:
    from aiohttp import RequestInfo
except ImportError:

    class RequestInfo:
        __slots__ = ("url", "method", "headers", "real_url")

        def __init__(self, url: URL, method: str, headers: dict, real_url: str):
            self.url = url
            self.method = method
            self.headers = headers
            self.real_url = real_url


__all__ = [
    "URL",
    "Pattern",
    "RequestInfo",
    "merge_params",
    "stream_reader_factory",
    "normalize_url",
]
