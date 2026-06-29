# Julius Supported Services (32 probes)

Julius fingerprints **HTTP(S) LLM inference, gateway, and RAG/orchestration** endpoints via embedded YAML probes. Probes are sorted by **port_hint** relevance before execution.

## Categories

| Category | Count | Specificity range | Notes |
|----------|-------|-------------------|-------|
| Self-hosted LLM servers | 15 | 50–100 | Ollama (100), vLLM, LocalAI, llama.cpp, TGI, LM Studio, … |
| Gateway services | 3 | 75–85 | LiteLLM, Kong AI Gateway, Envoy AI Gateway |
| RAG & orchestration | 12 | 50–80 | Open WebUI, Dify, Flowise, LibreChat, NextChat, Onyx, … |
| Cloud-managed | 1 | 75 | Salesforce Einstein |
| Generic fallback | 1 | 1 | `openai-compatible` — lowest priority |

## Self-hosted (port hints)

| Service | Probe | Port hint | Specificity | Models | Augustus |
|---------|-------|-----------|-------------|--------|----------|
| Ollama | `ollama` | 11434 | 100 | Yes | Yes |
| vLLM | `vllm` | 8000 | 75 | Yes | Yes |
| LocalAI | `localai` | 8080 | 75 | Yes | Yes |
| llama.cpp | `llama-cpp` | 8080 | 50 | Yes | Yes |
| Hugging Face TGI | `huggingface-tgi` | 3000 | 75 | Yes | Yes |
| LM Studio | `lm-studio` | 1234 | 70 | Yes | Yes |
| Aphrodite Engine | `aphrodite-engine` | 2242 | 75 | Yes | Yes |
| FastChat | `fastchat-controller` | 21001 | 75 | Yes | Yes |
| GPT4All | `gpt4all` | 4891 | 75 | Yes | Yes |
| Gradio | `gradio` | 7860 | 75 | No | No |
| Jan | `jan` | 1337 | 75 | Yes | Yes |
| KoboldCpp | `koboldcpp` | 5001 | 75 | Yes | Yes |
| NVIDIA NIM | `nvidia-nim` | 8000 | 75 | Yes | Yes |
| TabbyAPI | `tabbyapi` | 5000 | 75 | Yes | Yes |
| Text Generation WebUI | `text-generation-webui` | 5000 | 75 | Yes | Yes |

## Gateway

| Service | Probe | Port | Specificity |
|---------|-------|------|-------------|
| LiteLLM | `litellm` | 4000 | 85 |
| Kong AI Gateway | `kong-ai-proxy` | 8000 | 80 |
| Envoy AI Gateway | `envoy-ai-gateway` | 80 | 75 |

## RAG & orchestration (selected)

| Service | Probe | Port | Specificity |
|---------|-------|------|-------------|
| Open WebUI | `openwebui` | 3000 | 80 |
| Dify | `dify` | 80 | 75 |
| Flowise | `flowise` | 3000 | 75 |
| LibreChat | `librechat` | 3080 | 50 |
| NextChat | `nextchat` | 3000 | 75 |
| Onyx | `onyx` | 3000 | 75 |

Full table: https://github.com/praetorian-inc/julius/wiki/Supported-Services

## Match strategies (probe YAML)

| `require` | Behavior |
|-----------|----------|
| `any` (default) | First matching request wins (e.g. Ollama `/api/tags` OR `/`) |
| `all` | Every request must match (e.g. vLLM `/version` AND `/v1/models`) |

## Agent targeting tips

When building targets from port scans, map common ports to URL seeds:

| Ports | Likely services |
|-------|-----------------|
| 11434 | Ollama |
| 8000, 8080 | vLLM, LocalAI, Kong, NIM |
| 7860 | Gradio |
| 4000 | LiteLLM |
| 3000, 3001, 3080, 3210 | Web UIs (Open WebUI, Flowise, LibreChat, LobeHub) |
| 1234 | LM Studio |
| 443 | Cloud APIs, Einstein, HTTPS gateways |

Julius still runs all probes; port_hint only **prioritizes** probe order.

## Custom probes

Use `-p ./probes` and validate with `julius validate ./probes`. See [match-rules-and-probes.md](match-rules-and-probes.md).
