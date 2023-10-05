MISSING_API_KEY_ERROR_MESSAGE = """No API key found for Numexakey.
Please set either the NUMEXA_API_KEY environment variable or \
pass the api_key prior to initialization of Numexa.
API keys can be found or created at https://app.numexa.io/admin/keys \

Here's how you get it:
1. Visit https://app.numexa.io/admin/keys
2. click on "Generate Api Key"
"""

MISSING_BASE_URL = """No Base url provided. Please provide a valid base url.
For example: https://app.numexa.io/proxy/v1/openai
"""

MISSING_CONFIG_MESSAGE = (
    """The 'config' parameter is not set. Please provide a valid Config object."""
)
MISSING_MODE_MESSAGE = (
    """The 'mode' parameter is not set. Please provide a valid mode literal."""
)

INVALID_NUMEXA_KEY_MODE = """
Argument of type '{}' cannot be assigned to parameter "mode" of \
    type "ModesLiteral | Modes | None"
"""

DEFAULT_MAX_RETRIES = 2
VERSION = "0.1.0"
DEFAULT_TIMEOUT = 60
NUMEXA_HEADER_PREFIX = "X-Numexa-"
NUMEXA_DIRECT_URL = "https://api.openai.com/v1"

NUMEXA_API_KEY = "NUMEXA_API_KEY"
NUMEXA_PROXY_URL = "https://app.numexa.io/proxy/v1/openai"
NUMEXA_PROXY = "NUMEXA_PROXY"
OPEN_API_KEY = "OPEN_API_KEY"
