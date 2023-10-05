import os
from typing import Optional, Union
from numexa.api_resources import (
    LLMOptions,
    Modes,
    ModesLiteral,
    ProviderTypes,
    ProviderTypesLiteral,
    CacheType,
    CacheLiteral,
    Message,
    PortkeyResponse,
    ChatCompletions,
    Completions,
    Params,
    Config,
    RetrySettings,
    ChatCompletion,
    ChatCompletionChunk,
    TextCompletion,
    TextCompletionChunk,
    Generations,
)
from numexa.version import VERSION
from numexa.api_resources.global_constants import (
    NUMEXA_DIRECT_URL,
    NUMEXA_API_KEY,
    NUMEXA_PROXY_URL,
    NUMEXA_PROXY,
    OPEN_API_KEY
)

api_key = os.environ.get(NUMEXA_API_KEY)
if os.environ.get(NUMEXA_PROXY, "true").lower() == "true":
    base_url = NUMEXA_PROXY_URL
else:
    base_url = NUMEXA_DIRECT_URL
    if not os.environ.get(OPEN_API_KEY):
        raise Exception("IF NUMEXA_PROXY Is not set then please set OPEN_API_KEY os.environ['OPEN_API_KEY']='Bearer YOUR_KEY'")
config: Optional[Config] = None
mode: Optional[Union[Modes, ModesLiteral]] = None
__version__ = VERSION
__all__ = [
    "LLMOptions",
    "Modes",
    "PortkeyResponse",
    "ModesLiteral",
    "ProviderTypes",
    "ProviderTypesLiteral",
    "CacheType",
    "CacheLiteral",
    "Message",
    "ChatCompletions",
    "Completions",
    "Params",
    "RetrySettings",
    "ChatCompletion",
    "ChatCompletionChunk",
    "TextCompletion",
    "TextCompletionChunk",
    "Generations",
    "Config",
    "api_key",
    "base_url",
]
