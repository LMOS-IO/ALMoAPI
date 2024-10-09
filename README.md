# ALMoAPI

ALMoAPI, Agentic Language Model API, is a fork of [tabbyAPI](https://github.com/theroyallab/tabbyAPI/), designed to improve the suitability of the application for home user scale agentic systems.

Although this fork is still relatively new, we do not aim to maintain the ability to act as a drop in replacement for TabbyAPI.

> [!TIP]
>
> Join the [discord](https://discord.gg/6YZNN25KFN) for updates and discussions.

> [!IMPORTANT]
> 
>  ALMoAPI targets advanced users, If you want a simpler project please refer to tabbyAPI.

## Core differences btween us and tabbyAPI

User facing differences:
- Multiple API key support
- Optional Redis backed auth provider
- First class docker support
- No KoboldAI support (this will be reimplemented using an external conversion layer)
- No sampler Presets (this will be a per model setting instead)
- (TODO) multi model support
- (TODO) whisper API support
- (TODO) ctranslate2 backend support

Developer facing differences:
- General file structure changes
- (IN PROGRESS) migrating the internal codebase to remove all instances of `**kwargs`
- (IN PROGRESS) Migrate subsystems to have clearly defined interfaces (see `auth/interface.py`)

Auth keys and config.yml are not compatible with tabbyAPI. We do not use start scripts.

## Getting Started

### initial install

The recommended installation method is to use docker-compose.

If you do not want to use docker, you can install ALMoAPI manually. Please create a virtual environment, and then install the dependencies using pip. Use any of:

```
pip install .[cu121]
pip install .[cu118]
pip install .[amd]
```

Optional: Some dependencies can be installed via `pip install .[extras]` (required for text embeddings) and `pip install .[redis]` (required for redis auth provider) Optional

### setup

Generate a new config file run `python almoapi/main.py --export-config true --config-export-path "config.yml"`

Enable an auth provider of your choice in the config file (defaults to simple)

Add a new API key with `python almoapi/main.py --add-api-key true --key-permission admin`

Run the API server with `python almoapi/main.py`

## Features

- OpenAI compatible API
- Loading/unloading models
- HuggingFace model downloading
- Embedding model support
- JSON schema + Regex + EBNF support
- Speculative decoding via draft models
- Multi-lora with independent scaling (ex. a weight of 0.9)
- Inbuilt proxy to override client request parameters/samplers
- Flexible Jinja2 template engine for chat completions that conforms to HuggingFace
- Concurrent inference with asyncio
- Utilizes modern python paradigms
- Continuous batching engine using paged attention
- Fast classifier-free guidance
- OAI style tool/function calling
- Parallel batching (Nvidia Ampere GPUs and higher)

## Supported Model Types

ALMoAPI uses Exllamav2 as a powerful and fast backend for model inference, loading, etc. Therefore, the following types of models are supported:

- Exl2 (recommended)
- GPTQ
- Pure FP16

## Contributing

The basic contribution guidelines are:
- make sure all relevant code is documented
- explain the changes made in detail
- avoid adding external dependencies unless needed
- format all code with ruff (you can install this via `pip install .[dev]`, or just use the system version)
- use type annotations where possible
- avoid `**kwargs`

## Acknowledgements

ALMoAPI would not exist without the work of other contributors and FOSS projects:

- [tabbyAPI](https://github.com/theroyallab/tabbyAPI/)
- [ExllamaV2](https://github.com/turboderp/exllamav2)
- [infinity-emb](https://github.com/michaelfeil/infinity)
- [FastAPI](https://github.com/fastapi/fastapi)
