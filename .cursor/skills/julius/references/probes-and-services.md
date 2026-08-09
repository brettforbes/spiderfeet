# Julius Supported Services (live `list` — 63 probes)

Source of truth for this host: **`julius list`** on `C:\projects\spiderfeet\.tools\julius\julius.exe` (**2026-08-10**). Count: **63** probe names (including `openai-compatible`). Bundled README may advertise slightly different totals; prefer live `list`.

Julius fingerprints **HTTP(S) LLM inference, gateway, MCP, RAG/orchestration, and cloud AI** endpoints via embedded YAML probes. Port hints **prioritize** probe order; Julius still runs the probe set.

## Categories (aligned with README + live names)

| Category | Approx. count | Examples |
|----------|---------------|----------|
| Self-hosted LLM servers | 25 | `ollama`, `vllm`, `localai`, `sglang`, `huggingface-tgi`, … |
| Gateway / proxy | 8 | `litellm`, `bifrost`, `kong-proxy`, `envoy-ai-gateway`, … |
| MCP | 1 | `mcp-server` |
| RAG & orchestration | 18 | `open-webui`, `dify`, `flowise`, `anythingllm`, … |
| Cloud-managed | 10 | `aws-bedrock`, `azure-openai`, `vertex-ai`, `groq`, … |
| Generic fallback | 1 | `openai-compatible` (specificity 1) |

## Probe names (alphabetical, from live `list`)

```
anythingllm, aphrodite-engine, astrbot, aws-bedrock, azure-openai,
baseten-truss, bentoml, betterchatgpt, bifrost, cloudflare-ai-gateway,
deepspeed-mii, dify, envoy-ai-gateway, fastchat-controller, fireworks-ai,
flowise, gpt4all, gradio, groq, h2ogpt, helicone, huggingface-chat-ui,
huggingface-tgi, jan, koboldcpp, kong-proxy, langflow, librechat, litellm,
llama-cpp, lm-studio, lobehub, localai, mcp-server, mlc-llm, modal,
nextchat, nvidia-nim, ollama, omniroute, onyx, open-webui, openai-compatible,
openclaw, petals, portkey-ai-gateway, powerinfer, privategpt, quivr,
ragflow, ray-serve, replicate, salesforce-einstein, sglang, sillytavern,
tabbyapi, tensorrt-llm, tensorzero, text-generation-webui, together-ai,
triton-inference-server, vertex-ai, vllm
```

## Common port hints (targeting)

| Ports | Likely services |
|-------|-----------------|
| 11434 | Ollama |
| 8000, 8080 | vLLM, LocalAI, NIM, gateways |
| 7860 | Gradio, Langflow, h2oGPT |
| 4000 | LiteLLM |
| 3000, 3001, 3080, 3210 | Web UIs (Open WebUI, Flowise, LibreChat, LobeHub, …) |
| 1234 | LM Studio |
| 443 | Cloud APIs, HTTPS frontends, MCP |
| 8265 | Ray Serve |
| 18789 | OpenClaw |
| 30000 | SGLang |

Full human descriptions: bundled `.tools/julius/README.md` and [Supported Services wiki](https://github.com/praetorian-inc/julius/wiki/Supported-Services).

## Match strategies (probe YAML)

| `require` | Behavior |
|-----------|----------|
| `any` (default) | First matching request wins |
| `all` | Every request must match |

## Custom probes

```bash
julius validate ./probes
julius probe -p ./probes -o jsonl https://target:9000
```

See `match-rules-and-probes.md`.
