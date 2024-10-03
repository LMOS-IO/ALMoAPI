# ALMoAPI

ALMoAPI, Agentic Language Model API, is a fork of [tabbyAPI](https://github.com/theroyallab/tabbyAPI/), designed to improve the suitability of the application for home user scale agentic systems.

Although this fork is still relatively new, we do not aim to maintain the ability to act as a drop in replacement for TabbyAPI.

> [!IMPORTANT]
> 
>  ALMoAPI targets advanced users, If you want a simpler project please refer to tabbyAPI.


## Getting Started

The recommended installation method is to use docker-compose.

If you do not want to use docker, you can install ALMoAPI manually. Please create a virtual environment, and then install the dependencies using pip. Use any of:

```
pip install .[cu121]
pip install .[cu118]
pip install .[amd]
```

Some optional dependencies can be installed via `pip install .[extras]` (required for text embeddings)

Run the API server with `python almoapi/main.py`

if you want to generate a new config file run `python almoapi/main.py --export-config true --config-export-path "config.yml"`

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
