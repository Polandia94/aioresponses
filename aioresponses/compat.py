import asyncio
from typing import Union
from urllib.parse import parse_qsl, urlencode

from aiohttp import StreamReader
from aiohttp.client_proto import ResponseHandler
from multidict import MultiDict
from yarl import URL


def stream_reader_factory(
    loop: asyncio.AbstractEventLoop,
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


__all__ = [
    "merge_params",
    "stream_reader_factory",
    "normalize_url",
]
