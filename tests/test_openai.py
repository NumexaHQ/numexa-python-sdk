from __future__ import annotations

import os
from typing import Any

import pytest
from dotenv import load_dotenv

import numexa
from numexa import Config, LLMOptions, TextCompletion, TextCompletionChunk
from tests.utils import assert_matches_type

load_dotenv()
base_url = os.environ.get("NUMEXA_DIRECT_URL")
api_key = os.environ.get("NUMEXA_API_KEY")
virtual_api_key = os.environ.get("OPENAI_VIRTUAL_KEY")


class TestOpenaiCompletions:
    client = numexa
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="text-davinci-003",
            ),
        )
        client.config = config
        completion = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
        )
        assert ("True", "True")

        assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="text-davinci-003",
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
        assert ("True", "True")
        assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="text-davinci-003",
            ),
        )
        client.config = config
        completion_streaming = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
            stream=True,
        )
        assert ("True", "True")

        for chunk in completion_streaming:
            assert_matches_type(TextCompletionChunk, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="text-davinci-003",
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
        assert ("True", "True")


class TestOpenaiChatCompletions:
    client = numexa
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="gpt-3.5-turbo",
            ),
        )
        client.config = config
        completion = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
        )
        assert ("True", "True")

        assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="gpt-3.5-turbo",
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
        assert ("True", "True")
        assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="gpt-3.5-turbo",
            ),
        )
        client.config = config
        completion_streaming = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stream=True,
        )
        assert ("True", "True")

        for chunk in completion_streaming:
            assert_matches_type(TextCompletionChunk, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="openai",
                metadata={"_user": "numexa-python-sdk"},
                model="gpt-3.5-turbo",
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
        assert ("True", "True")

        for chunk in completion_streaming:
            assert_matches_type(TextCompletionChunk, chunk, path=["response"])


class TestOpenaiGenerations:
    client = numexa
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_stream(self, client: Any) -> None:
        config = Config(mode="single")
        client.config = config
        completion = client.Generations.create(
            prompt_id="",
        )
        assert ("True", "True")
        assert_matches_type(TextCompletion, completion, path=["response"])
