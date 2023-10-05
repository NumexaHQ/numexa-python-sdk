from __future__ import annotations

import os
from typing import Any

import pytest
from dotenv import load_dotenv

import numexa
from numexa import Config, LLMOptions

# from tests.utils import assert_matches_type
load_dotenv()
base_url = os.environ.get("NUMEXA_DIRECT_URL")
api_key = os.environ.get("NUMEXA_API_KEY")
anyscale_api_key = os.environ.get("ANYSCALE_API_KEY")


class TestAnyscaleCompletions:
    client = numexa
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
        )
        # assert("True", "True")

        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
            stop_sequences=["string", "string", "string"],
            stream=False,
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")
        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion_streaming = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
            stream=True,
        )
        # assert("True", "True")

        # for chunk in completion_streaming:
        #     assert_matches_type(TextCompletionChunk, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion_streaming = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
            stream=True,
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")


class TestAnyscaleChatCompletions:
    client = numexa
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
        )
        # assert("True", "True")

        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stop_sequences=["string", "string", "string"],
            stream=False,
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")
        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion_streaming = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stream=True,
        )
        # assert("True", "True")

        # for chunk in completion_streaming:
        #     assert_matches_type(TextCompletionChunk, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                api_key=anyscale_api_key,
                provider="anyscale",
                metadata={"_user": "numexa-python-sdk"},
                model="meta-llama/Llama-2-70b-chat-hf",
            ),
        )
        client.config = config
        completion_streaming = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stream=True,
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")
