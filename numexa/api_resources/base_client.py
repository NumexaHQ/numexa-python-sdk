from __future__ import annotations

import json
import os
import socket
from datetime import datetime
from types import TracebackType
from typing import (
    Dict,
    Any,
    Union,
    Mapping,
    cast,
    List,
    Optional,
    Type,
    overload,
    Literal,
    get_args,
)
import httpx
import platform
from .global_constants import NUMEXA_HEADER_PREFIX, OPEN_API_KEY, NUMEXA_INGEST_LOGS
from .utils import (
    remove_empty_values,
    Body,
    Options,
    RequestConfig,
    OverrideParams,
    ProviderOptions,
    Params,
    Constructs,
    NumexaApiPaths,
)
from .exceptions import (
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
)
from numexa.version import VERSION
from .utils import ResponseT, make_status_error, default_api_key, default_base_url
from .common_types import StreamT
from .streaming import Stream


class MissingStreamClassError(TypeError):
    def __init__(self) -> None:
        super().__init__(
            "The `stream` argument was set to `True` but the `stream_cls` argument was\
            not given",
        )


class APIClient:
    _client: httpx.AsyncClient
    _default_stream_cls: Union[type[Stream[Any]], None] = None

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or default_api_key()
        self.base_url = base_url or default_base_url()
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Accept": "application/json"},
        )

    def _serialize_header_values(
        self, headers: Optional[Mapping[str, Any]]
    ) -> Dict[str, str]:
        if headers is None:
            return {}
        return {
            f"{NUMEXA_HEADER_PREFIX}{k}": json.dumps(v)
            if isinstance(v, (dict, list))
            else str(v)
            for k, v in headers.items()
        }

    @property
    def custom_auth(self) -> Optional[httpx.Auth]:
        return None

    @overload
    async def post(
        self,
        path: str,
        *,
        body: List[Body],
        mode: str,
        cast_to: Type[ResponseT],
        stream: Literal[True],
        stream_cls: type[StreamT],
        params: Params,
    ) -> StreamT:
        ...

    @overload
    async def post(
        self,
        path: str,
        *,
        body: List[Body],
        mode: str,
        cast_to: Type[ResponseT],
        stream: Literal[False],
        stream_cls: type[StreamT],
        params: Params,
    ) -> ResponseT:
        ...

    @overload
    async def post(
        self,
        path: str,
        *,
        body: List[Body],
        mode: str,
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
        params: Params,
    ) -> Union[ResponseT, StreamT]:
        ...

    async def post(
        self,
        path: str,
        *,
        body: Union[List[Body], Any],
        mode: str,
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
        params: Params,
    ) -> Union[ResponseT, StreamT]:
        if path in [NumexaApiPaths.CHAT_COMPLETION, NumexaApiPaths.COMPLETION]:
            body = cast(List[Body], body)
            # todo: change _construct_direct to _construct
            opts = self._construct_direct(
                method="post",
                url=path,
                body=body,
                mode=mode,
                stream=stream,
                params=params,
            )
        elif path in NumexaApiPaths.CHAT_COMPLETION_DIRECT:
            body = cast(List[Body], body)
            opts = self._construct_direct(
                method="post",
                url=path.split("/direct")[0],
                body=body,
                mode=mode,
                stream=stream,
                params=params,
            )

        elif path.endswith("/generate"):
            opts = self._construct_generate_options(
                method="post",
                url=path,
                body=body,
                mode=mode,
                stream=stream,
                params=params,
            )
        else:
            raise NotImplementedError(f"This API path `{path}` is not implemented.")

        res = await self._request(
            options=opts,
            stream=stream,
            cast_to=cast_to,
            stream_cls=stream_cls,
        )
        return res

    def _construct_generate_options(
        self,
        *,
        method: str,
        url: str,
        body: Any,
        mode: str,
        stream: bool,
        params: Params,
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        json_body = body
        opts.json_body = remove_empty_values(json_body)
        opts.headers = None
        return opts

    def _construct(
        self,
        *,
        method: str,
        url: str,
        body: List[Body],
        mode: str,
        stream: bool,
        params: Params,
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        params_dict = {} if params is None else params.dict()
        json_body = {
            "config": self._config(mode, body).dict(),
            "params": {**params_dict, "stream": stream},
        }
        opts.json_body = remove_empty_values(json_body)
        opts.headers = None
        return opts

    def _construct_direct(
            self,
            *,
            method: str,
            url: str,
            body: List[Body],
            mode: str,
            stream: bool,
            params: Params,
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        params_dict = {} if params is None else params.dict()
        json_body = {
            "model": self._config_direct(mode, body),
            "messages": params_dict.get("messages", [{}])
        }
        opts.json_body = remove_empty_values(json_body)
        opts.headers = None
        return opts

    def _config(self, mode: str, body: List[Body]) -> RequestConfig:
        config = RequestConfig(mode=mode, options=[])
        for i in body:
            override_params = cast(OverrideParams, i)
            constructs = cast(Constructs, i)
            options = ProviderOptions(
                override_params=override_params, **constructs.dict()
            )
            config.options.append(options)
        return config

    def _config_direct(self, mode: str, body: List[Body]) -> List[str]:
        config = []
        for i in body:
            config.append(i.model)
        return config

    @property
    def _default_headers(self) -> Mapping[str, str]:
        # Proxy ON
        if not os.environ.get("NUMEXA_PROXY"):
            return {
                "Content-Type": "application/json",
                f"{NUMEXA_HEADER_PREFIX}Api-Key": self.api_key,
                f"{NUMEXA_HEADER_PREFIX}package-version": f"numexa-{VERSION}",
                f"{NUMEXA_HEADER_PREFIX}runtime": platform.python_implementation(),
                f"{NUMEXA_HEADER_PREFIX}runtime-version": platform.python_version(),
                f"{NUMEXA_HEADER_PREFIX}Cache": "true",
                # "Authorization": os.environ.get(OPEN_API_KEY),

            }
        # Proxy Off
        else:
            return {
                "Content-Type": "application/json",
                "Authorization": os.environ.get(OPEN_API_KEY)
            }

    def _build_headers(self, options: Options) -> httpx.Headers:
        custom_headers = options.headers or {}
        headers_dict = self._merge_mappings(self._default_headers, custom_headers)
        headers = httpx.Headers(headers_dict)
        return headers

    def _merge_mappings(
        self,
        obj1: Mapping[str, Any],
        obj2: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Merge two mappings of the given type
        In cases with duplicate keys the second mapping takes precedence.
        """
        return {**obj1, **obj2}

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        self._client.close()

    def __enter__(self: Any) -> Any:
        return self

    def __exit__(
        self,
        exc_type: Optional[BaseException],
        exc: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def _build_request(self, options: Options) -> List[httpx.Request]:
        headers = self._build_headers(options)
        params = options.params
        json_body = options.json_body
        request = self._client.build_request(
            method=options.method,
            url=options.url,
            headers=headers,
            params=params,
            json=json_body,
            timeout=options.timeout,
        )
        return [request]

    async def _build_request_direct(self, options: Options) -> List[httpx.Request]:
        headers = self._build_headers(options)
        new_payload = dict()
        request_list = []
        params = options.params
        json_body = options.json_body
        messages = json_body.get("messages", [{}])
        models = json_body.get("model", [""])
        new_payload["messages"] = messages
        for model in models:
            new_payload["model"] = model
            request_list.append(self._client.build_request(
                method=options.method,
                url=options.url,
                headers=headers,
                params=params,
                json=new_payload,
                timeout=options.timeout,
            ))
        return request_list

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: Literal[False],
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> ResponseT:
        ...

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: Literal[True],
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> StreamT:
        ...

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        ...

    async def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        # proxy on
        if not os.environ.get("NUMEXA_PROXY"):
            # todo: change _build_request_direct to _build_request
            request_list = await self._build_request_direct(options)
        # proxy off
        else:
            request_list = await self._build_request_direct(options)
        for request in request_list:
            try:
                initiated_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                res = await self._client.send(request, auth=self.custom_auth, stream=stream)
                if os.environ.get("NUMEXA_PROXY"):
                    response_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    # Preparing Monger Request Body
                    monger_request_body = dict()
                    monger_request_body["request_time"] = initiated_timestamp
                    hostname = socket.gethostname()
                    monger_request_body["source_ip"] = socket.gethostbyname(hostname)
                    monger_request_body["request_method"] = "POST"
                    monger_request_body["request_url"] = str(request.url)
                    monger_request_body["request_body"] = json.loads(request.content.decode("utf-8"))
                    request.headers.update(
                        {"X-Numexa-Log-Type": "request", "X-Numexa-Api-Key": os.environ.get("NUMEXA_API_KEY")})
                    request.headers.update(
                        {"Content-Length": str(len(json.dumps(monger_request_body, default=str).encode("utf-8")))})
                    #  Monger Request Ingestion Start
                    monger_request_option = Options(method=request.method, headers=request.headers,
                                                    json_body=monger_request_body,
                                                    url=NUMEXA_INGEST_LOGS)
                    monger_request = self._build_monger(options=monger_request_option)
                    await self._client.send(monger_request, auth=self.custom_auth, stream=stream)
                    #  Monger Request Ingestion End

                    # Preparing Monger Response Body
                    monger_response_body = dict()
                    monger_response_body["initiated_timestamp"] = initiated_timestamp
                    monger_response_body["response_timestamp"] = response_timestamp
                    monger_response_body["response_status_code"] = res.status_code
                    monger_response_body["response_body"] = json.loads(res.content.decode("utf-8"))
                    res.headers.update(
                        {"X-Numexa-Log-Type": "response", "X-Numexa-Api-Key": os.environ.get("NUMEXA_API_KEY")})
                    res.headers.update(
                        {"Content-Length": str(len(json.dumps(monger_response_body, default=str).encode("utf-8")))})
                    # Monger Response Ingestion Start
                    monger_response_option = Options(method=request.method, headers=res.headers,
                                                     json_body=monger_response_body, url=NUMEXA_INGEST_LOGS)
                    monger_response = self._build_monger(options=monger_response_option)
                    await self._client.send(monger_response, auth=self.custom_auth, stream=stream)
                    # Monger Response Ingestion End
                res.raise_for_status()
            except httpx.HTTPStatusError as err:  # 4xx and 5xx errors
                # If the response is streamed then we need to explicitly read the response
                # to completion before attempting to access the response text.
                print(err.response.read())
                continue
                # raise self._make_status_error_from_response(request, err.response) from None
            except httpx.TimeoutException as err:
                raise APITimeoutError(request=request) from err
            except Exception as err:
                raise APIConnectionError(request=request) from err
            if stream or res.headers["content-type"] == "text/event-stream":
                if stream_cls is None:
                    raise MissingStreamClassError()
                stream_response = stream_cls(
                    response=res, cast_to=self._extract_stream_chunk_type(stream_cls)
                )
                return stream_response
            response = cast(
                ResponseT,
                cast_to(**res.json()),
            )
            return response

    def _extract_stream_chunk_type(self, stream_cls: Type) -> type:
        args = get_args(stream_cls)
        if not args:
            raise TypeError(
                f"Expected stream_cls to have been given a generic type argument, e.g. Stream[Foo] but received {stream_cls}",
            )
        return cast(type, args[0])
    
    def _build_monger(self, options: Options) -> httpx.Request:
        headers = options.headers
        method = options.method
        params = options.params
        url = options.url
        json_body = options.json_body
        return self._client.build_request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_body,
            timeout=options.timeout)

    def _make_status_error_from_response(
        self,
        request: httpx.Request,
        response: httpx.Response,
    ) -> APIStatusError:
        err_text = response.text.strip()
        body = err_text

        try:
            body = json.loads(err_text)["error"]["message"]
            err_msg = f"Error code: {response.status_code} - {body}"
        except Exception:
            err_msg = err_text or f"Error code: {response.status_code}"

        return make_status_error(err_msg, body=body, request=request, response=response)
