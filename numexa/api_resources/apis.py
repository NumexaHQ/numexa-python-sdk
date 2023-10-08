import os
from typing import Optional, Union, overload, Literal, List, Mapping, Any
from numexa.api_resources.base_client import APIClient
from .utils import (
    Modes,
    Config,
    retrieve_config,
    Params,
    Message,
    ChatCompletionChunk,
    ChatCompletion,
    TextCompletion,
    TextCompletionChunk,
    GenericResponse,
)

from .streaming import Stream

__all__ = ["Completions", "ChatCompletions"]


class APIResource:
    _client: APIClient
    # _get: Any
    # _patch: Any
    # _put: Any
    # _delete: Any

    def __init__(self, client: APIClient) -> None:
        self._client = client
        # self._get = client.get
        # self._patch = client.patch
        # self._put = client.put
        # self._delete = client.delete

    async def _post(self, *args, **kwargs):
        return await self._client.post(*args, **kwargs)


class Completions(APIResource):
    @classmethod
    @overload
    async def create(
        cls,
        *,
        prompt: Optional[str] = None,
        config: Optional[Config] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[TextCompletionChunk]:
        ...

    @classmethod
    @overload
    async def create(
        cls,
        *,
        prompt: Optional[str] = None,
        config: Optional[Config] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> TextCompletion:
        ...

    @classmethod
    @overload
    async def create(
        cls,
        *,
        prompt: Optional[str] = None,
        config: Optional[Config] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
        ...

    @classmethod
    async def create(
        cls,
        *,
        prompt: Optional[str] = None,
        config: Optional[Config] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
        if config is None:
            config = retrieve_config()
        _client = APIClient(api_key=config.api_key, base_url=config.base_url)
        params = Params(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_k=top_k,
            top_p=top_p,
            **kwargs,
        )
        if config.mode == Modes.SINGLE.value:
            return await cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=Modes.SINGLE.value,
                params=params,
                cast_to=TextCompletion,
                stream_cls=Stream[TextCompletionChunk],
                stream=stream,
            )
        if config.mode == Modes.FALLBACK.value:
            return await cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=Modes.FALLBACK,
                params=params,
                cast_to=TextCompletion,
                stream_cls=Stream[TextCompletionChunk],
                stream=stream,
            )
        if config.mode == Modes.AB_TEST.value:
            return await cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=Modes.AB_TEST,
                params=params,
                cast_to=TextCompletion,
                stream_cls=Stream[TextCompletionChunk],
                stream=stream,
            )
        raise NotImplementedError("Mode not implemented.")


class ChatCompletions(APIResource):
    @classmethod
    @overload
    async def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Config] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[ChatCompletionChunk]:
        ...

    @classmethod
    @overload
    async def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Config] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> ChatCompletion:
        ...

    @classmethod
    @overload
    async def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Config] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
        ...

    @classmethod
    async def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Config] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
        if config is None:
            config = retrieve_config()
        _client = APIClient(api_key=config.api_key, base_url=config.base_url)
        params = Params(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_k=top_k,
            top_p=top_p,
            **kwargs,
        )
        # Proxy On
        if not os.environ.get("NUMEXA_PROXY"):
            url = "/chat/completions"
        # proxy Off
        else:
            url = "/chat/completions/direct"
        if config.mode == Modes.SINGLE.value:
            return await cls(_client)._post(
                url,
                body=config.llms,
                mode=Modes.SINGLE.value,
                params=params,
                cast_to=ChatCompletion,
                stream_cls=Stream[ChatCompletionChunk],
                stream=stream,
            )
        if config.mode == Modes.FALLBACK.value:
            return await cls(_client)._post(
                url,
                body=config.llms,
                mode=Modes.FALLBACK,
                params=params,
                cast_to=ChatCompletion,
                stream_cls=Stream[ChatCompletionChunk],
                stream=stream,
            )
        if config.mode == Modes.AB_TEST.value:
            return await cls(_client)._post(
                url,
                body=config.llms,
                mode=Modes.AB_TEST,
                params=params,
                cast_to=ChatCompletion,
                stream_cls=Stream[ChatCompletionChunk],
                stream=stream,
            )
        raise NotImplementedError("Mode not implemented.")


class Generations(APIResource):
    @classmethod
    async def create(
        cls,
        *,
        prompt_id: str,
        config: Optional[Config] = None,
        variables: Optional[Mapping[str, Any]] = None,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        if config is None:
            config = retrieve_config()
        _client = APIClient(api_key=config.api_key, base_url=config.base_url)
        body = {"variables": variables}
        return await cls(_client)._post(
            f"/v1/prompts/{prompt_id}/generate",
            body=body,
            mode=None,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=False,
        )
