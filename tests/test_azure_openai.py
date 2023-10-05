from __future__ import annotations

import os
from typing import Any

import pytest
from dotenv import load_dotenv

import numexa
from numexa import Config, LLMOptions, TextCompletion, TextCompletionChunk
from tests.utils import assert_matches_type

# from tests.utils import assert_matches_type
load_dotenv()
base_url = os.environ.get("NUMEXA_DIRECT_URL")
api_key = os.environ.get("NUMEXA_API_KEY")
virtual_api_key = os.environ.get("AZURE_OPENAI_VIRTUAL_KEY")


class TestAzureChatCompletions:
    client = numexa
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="azure-openai",
                metadata={"_user": "numexa-python-sdk"},
                api_version="2023-03-15-preview",
                resource_name="numexa",
                deployment_id="turbo-16k",
                retry={"attempts": 5, "on_status_codes": [429]},
            ),
        )
        client.config = config
        completion = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
        )
        assert("True", "True")

        assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="azure-openai",
                metadata={"_user": "numexa-python-sdk"},
                api_version="2023-03-15-preview",
                resource_name="numexa",
                deployment_id="turbo-16k",
                retry={"attempts": 5, "on_status_codes": [429]},
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
        assert("True", "True")
        assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="azure-openai",
                metadata={"_user": "numexa-python-sdk"},
                api_version="2023-03-15-preview",
                resource_name="numexa",
                deployment_id="turbo-16k",
                retry={"attempts": 5, "on_status_codes": [429]},
            ),
        )
        client.config = config
        completion_streaming = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stream=True,
        )
        assert("True", "True")

        for chunk in completion_streaming:
            assert_matches_type(TextCompletionChunk, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="azure-openai",
                metadata={"_user": "numexa-python-sdk"},
                api_version="2023-03-15-preview",
                resource_name="numexa",
                deployment_id="turbo-16k",
                retry={"attempts": 5, "on_status_codes": [429]},
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
        assert("True", "True")
        for chunk in completion_streaming:
            assert_matches_type(TextCompletionChunk, chunk, path=["response"])


class TestOpenaiGenerations:
    client = numexa
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_stream(self, client: Any) -> None:
        config = Config()
        client.config = config
        completion = client.Generations.create(
            prompt_id="",
        )
        assert ("True", "True")
        assert_matches_type(TextCompletion, completion, path=["response"])
