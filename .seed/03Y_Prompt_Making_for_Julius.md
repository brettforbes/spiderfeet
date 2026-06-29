# Creating a Skill and Documentation for Julius, Scanning Services

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for Julius, When we are scanning services, we will export them in json, and convert those results to nested nuggets

This skill will teach you how to use this tool to scan ports. More importantly it should teach you how to adapt your technique, and your sequence of techniques in order to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.

You will use this skill to exercise Julius in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables yout o get the wideset view on the source material you are going to caolsece into the skill and documentation.

- [Julius Github Repository](https://github.com/praetorian-inc/julius)
- [Julius - LLM Service Fingerprinting Tool](https://github.com/praetorian-inc/julius/wiki)
- [Architecture](https://github.com/praetorian-inc/julius/wiki/Architecture)
- [CLI Reference](https://github.com/praetorian-inc/julius/wiki/CLI-Reference)
- [Match Rules](https://github.com/praetorian-inc/julius/wiki/Match-Rules)
- [Probe YAML Reference](https://github.com/praetorian-inc/julius/wiki/Probe-YAML-Reference)
- [Supported Services](https://github.com/praetorian-inc/julius/wiki/Supported-Services)
- [Security Policy](https://github.com/praetorian-inc/julius/blob/main/SECURITY.md)


Some Naabu Blog Posts

- [Introducing Julius: Open Source LLM Service Fingerprinting](https://www.praetorian.com/blog/introducing-julius-open-source-llm-service-fingerprinting/)
- [Shadow AI Is Everywhere: Meet Julius, the Open-Source LLM Fingerprinting Tool ](https://dev.to/praetorian_guard/shadow-ai-is-everywhere-meet-julius-the-open-source-llm-fingerprinting-tool-410g)
- [Julius v0.2.0: From 33 to 63 Probes — Now Detecting Cloud AI, Enterprise Inference, and RAG Pipelines](https://www.praetorian.com/blog/julius-v020-cloud-ai-rag-detection/)
- [There’s Always a Secret Hiding Somewhere — We Built a Tool to Find It](https://medium.com/@praetorianguard/theres-always-a-secret-hiding-somewhere-we-built-a-tool-to-find-it-d5398b155a4f)

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\julius\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- Refences directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.

3. References Directory (`.cursor\skills\julius\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\Julius-Zero-to-Hero.md`): A markdown document that takes the user from zero to hero in using Julius for OSINT scanning and nugget mapping.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\Julius-CLI-Options.md`): A markdown document that lists the standard Julius CLI Options doc

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to check out an e-book"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the  tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option.
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.
- Include a Strategies and Tactics section, which are the best strategies for combining some sequences of operations, and adapting depending on the results of the previous operations to maximise the returned data.