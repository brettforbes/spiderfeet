# Creating a Skill and Documentation for Vespasian, Scanning Networks and Systems

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for Vespasian, when we are scanning networks and systems.

This skill will teach you how to use Vespasian in different reconnaissance and analysis scenarios.

You will use this skill to exercise Vespasian in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

Collect and consolidate all high-signal source material from official docs, code, releases, and strong practitioner references.

Official docs & repo:

- [https://github.com/praetorian-inc/vespasian](https://github.com/praetorian-inc/vespasian)
- [https://github.com/praetorian-inc/vespasian/blob/main/README.md](https://github.com/praetorian-inc/vespasian/blob/main/README.md)
- [https://github.com/praetorian-inc/vespasian/releases](https://github.com/praetorian-inc/vespasian/releases)
- [https://github.com/praetorian-inc/vespasian/tree/main/docs](https://github.com/praetorian-inc/vespasian/tree/main/docs)

Blogs:

- [https://www.praetorian.com/blog/vespasian-api-endpoint-discovery-tool/](https://www.praetorian.com/blog/vespasian-api-endpoint-discovery-tool/)

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. Include specific trigger words or scenarios.
2. SKILL.md Content (`.cursor\skills\vespian\SKILL.md`): Deconstruct the workflows from source docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- References directory for details on source material and usage indexed through `SKILLS.md`.

3. References Directory (`.cursor\skills\vespian\references`): A directory of references to source material and usage, indexed through `SKILLS.md`.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\Vespasian-Zero-to-Hero.md`): A markdown document that takes the user from zero to hero in using Vespasian.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\Vespasian-CLI-Options.md`): A markdown document that lists standard and advanced Vespasian CLI options.

## Best Practices for Library Skills

When reviewing the AI output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they combine to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something, not just list features.
- Comprehensive Documentation: Every major aspect of the tool should be documented in the `references` subdirectory next to `SKILL.md`.
- Keep Descriptions Distinct: The short trigger description should be specific enough that the AI knows when to use the skill.
- Include Comprehensive Examples: Include an example for each major option class.
- Include a Strategies and Tactics section for sequencing operations and adapting based on prior outputs.
