
<div align="center">
<img src="docs/images/auth.png" height=150><br />

## Build reliable, secure, and production-ready AI apps easily.

```bash
pip install numexa
```

## Install From Git
```bash
pip install git+https://github.com/NumexaHQ/numexa-python-sdk.git#egg=numexa
```
</div>

## **💡 Features**

**🚪 AI Gateway:**
*  Unified API Signature: If you've used OpenAI, you already know how to use Numexa with any other provider.
*  Interoperability: Write once, run with any provider. Switch between _any model_ from _any provider_ seamlessly. 
*  Automated Fallbacks & Retries: Ensure your application remains functional even if a primary service fails.
*  Load Balancing: Efficiently distribute incoming requests among multiple models.
*  Semantic Caching: Reduce costs and latency by intelligently caching results.

**🔬 Observability:**
*  Logging: Keep track of all requests for monitoring and debugging.
*  Requests Tracing: Understand the journey of each request for optimization.
*  Custom Tags: Segment and categorize requests for better insights.


## **🚀 Quick Start**

**4️ Steps to Integrate the SDK**
1. Get your Numexa API key and your virtual key for AI providers.
2. Construct your LLM, add Numexa features, provider features, and prompt.
3. Construct the Numexa client and set your usage mode.
4. Now call Numexa regularly like you would call your OpenAI constructor.

Let's dive in! If you are an advanced user and want to directly jump to various full-fledged examples, [click here](https://github.com/numexa-python-sdk/tree/main/examples).

---

### **Step 1️⃣ : Get your Numexa API Key and your Virtual Keys for AI providers**

**Numexa API Key:** Log into [Numexa here](https://app.numexa.io/), then click on the API Keys link on left and "Click on Generate".
```python
import os
os.environ["NUMEXA_API_KEY"] = "NUMEXA_API_KEY"
```
**Numexa Without proxy:**
```python
import os
os.environ["NUMEXA_PROXY"] = "false"
```
**Virtual Keys:** Navigate to the "API Keys" page on [Numexa](https://app.numexa.io/admin/keys) and hit the "Generate" button. Choose your AI provider and assign a unique name to your key. Your virtual key is ready!

### **Step 2️⃣ : Construct your LLM, add NUmexa features, provider features, and prompt**

**Numexa Features**:
You can find a comprehensive [list of Numexa features here](#📔-list-of-numexa-features). This includes settings for caching, retries, metadata, and more.

**Provider Features**:
Numexa is designed to be flexible. All the features you're familiar with from your LLM provider, like `top_p`, `top_k`, and `temperature`, can be used seamlessly. Check out the [complete list of provider features here](https://github.com/numexa-python-sdk/blob/af0814ebf4f1961b5dfed438918fe68b26ef5f1e/numexa/api_resources/utils.py#L137).

**Setting the Prompt Input**:
This param lets you override any prompt that is passed during the completion call - set a model-specific prompt here to optimise the model performance. You can set the input in two ways. For models like Claude and GPT3, use `prompt` = `(str)`, and for models like GPT3.5 & GPT4, use `messages` = `[array]`.

Here's how you can combine everything:

```python
from numexa import LLMOptions

# Numexa Config
provider = "openai"
virtual_key = "key_a"
trace_id = "numexa_sdk_test"

# Model Settings
model = "gpt-4"
temperature = 1

# User Prompt
messages = [{"role": "user", "content": "Who are you?"}]

# Construct LLM
llm = LLMOptions(provider=provider, virtual_key=virtual_key, trace_id=trace_id, model=model, temperature=temperature)
```

### **Step 3️⃣ : Construct the Numexa Client**

Numexa client's config takes 3 params: `api_key`, `mode`, `llms`.

* `api_key`: You can set your NUmexa API key here or with `os.ennviron` as done above.
* `mode`: There are **3** modes - Single, Fallback, Loadbalance.
  * **Single** - This is the standard mode. Use it if you do not want Fallback OR Loadbalance features.
  * **Fallback** - Set this mode if you want to enable the Fallback feature.
  * **Loadbalance** - Set this mode if you want to enable the Loadbalance feature. 
* `llms`: This is an array where we pass our LLMs constructed using the LLMOptions constructor.

```py
import numexa
from numexa import Config, LLMOptions

llm = LLMOptions(provider="openai", model="gpt-4", virtual_key="key_a"),
numexa.config = Config(mode="single",llms=[llm])

```

### **Step 4️⃣ : Let's Call the Numexa Client!**

The Numexa client can do `ChatCompletions` and `Completions`.

Since our LLM is GPT4, we will use ChatCompletions:

```py
# noinspection PyUnresolvedReferences
response = numexa.ChatCompletions.create(
  messages=[{
    "role": "user",
    "content": "Who are you ?"
  }]
)
print(response.choices[0].message)
```

You have integrated Numexa Python SDK in just 4 steps!

---

## **🔁 Demo: Implementing GPT4 to GPT3.5 Fallback Using the Numexa SDK**

```py
import os
os.environ["NUMEXA_API_KEY"] = "NUMEXA_API_KEY" # Setting the Numexa API Key

import numexa
from numexa import Config, LLMOptions

# Let's construct our LLMs.
llm1 = LLMOptions(provider="openai", model="gpt-4", virtual_key="key_a"),
llm2 = LLMOptions(provider="openai", model="gpt-3.5-turbo", virtual_key="key_a")

# Now let's construct the Numexa client where we will set the fallback logic
numexa.config = Config(mode="fallback",llms=[llm1,llm2])

# And, that's it!
response = numexa.ChatCompletions.create()
print(response.choices[0].message)
```

## **📔 Full List of Numexa Config**

| Feature             | Config Key              | Value(Type)                                      | Required    |
|---------------------|-------------------------|--------------------------------------------------|-------------|
| Provider Name       | `provider`        | `string`                                         | ✅ Required  |
| Model Name        | `model`        | `string`                                         | ✅ Required |
| Virtual Key OR API Key        | `virtual_key` or `api_key`        | `string`                                         | ✅ Required (can be set externally) |
| Cache Type          | `cache_status`          | `simple`, `semantic`                             | ❔ Optional |
| Force Cache Refresh | `cache_force_refresh`   | `True`, `False` (Boolean)                                 | ❔ Optional |
| Cache Age           | `cache_age`             | `integer` (in seconds)                           | ❔ Optional |
| Trace ID            | `trace_id`              | `string`                                         | ❔ Optional |
| Retries         | `retry`           | `integer` [0,5]                                  | ❔ Optional |
| Metadata            | `metadata`              | `json object` [More info](https://docs.numexa.io/)          | ❔ Optional |

## **🤝 Supported Providers**

|| Provider  | Support Status  | Supported Endpoints |
|---|---|---|---|
| <img src="docs/images/openai.png" width=18 />| OpenAI | ✅ Supported  | `/completion`, `/embed` |
| <img src="docs/images/azure.png" width=18>| Azure OpenAI | ✅ Supported  | `/completion`, `/embed` |
| <img src="docs/images/anthropic.png" width=18>| Anthropic  | ✅ Supported  | `/complete` |
| <img src="docs/images/cohere.png" width=18>| Cohere  | 🚧 Coming Soon  | `generate`, `embed` |


---

#### [📝 Full Documentation](https://docs.numexa.io/) | [🛠️ Integration Requests](https://github.com/numexa-python-sdk/issues) | 

<a href="#"><img src="" alt="follow on Twitter"></a>
<a href="https://discord.gg/mVBMKVCv" target="_blank"><img src="https://img.shields.io/discord/1143393887742861333?logo=discord" alt="Discord"></a>
