# Creating a Skill and Documentation for Subfinder, Enumerating Subdomains

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for Subfinder. When we enumerate subdomains, we will export results as JSON Lines (`-oJ`), parse them into a structured bundle, and convert those results to nested nuggets (`INTERNET_NAME`, `INTERNET_NAME_UNRESOLVED`, and optional `IP_ADDRESS` when actively resolved).

This skill will teach you how to use this tool to enumerate subdomains. More importantly it should teach you how to adapt your technique, and your sequence of techniques in order to maximise the resulting data from any domain, regardless of how its systems seek to defeat passive discovery.

You will use this skill to exercise Subfinder in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables you to get the widest view on the source material you are going to capture into the skill and documentation.

- https://github.com/projectdiscovery/subfinder
- https://github.com/projectdiscovery/subfinder/tree/dev/v2/examples
- https://docs.projectdiscovery.io/opensource/subfinder/overview
- https://docs.projectdiscovery.io/opensource/subfinder/install
- https://docs.projectdiscovery.io/opensource/subfinder/running
- https://docs.projectdiscovery.io/opensource/subfinder/usage

Some Subfinder blog posts

- https://projectdiscovery.io/blog
- https://securitytrails.com/blog/subfinder
- https://dhiyaneshgeek.github.io/bug/bounty/2020/02/06/recon-with-me/
- https://dhiyaneshgeek.github.io/research/bug/bounty/2024/01/03/subfinder-securitytrails/
- https://hacklido.com/blog/390-subdomain-enumeration-using-subfinder
- https://www.geeksforgeeks.org/linux-unix/subfinder-a-subdomain-discovery-tool-in-kali-linux/
- https://www.freecodecamp.org/news/using-subfinder-for-subdomain-enumeration/
- https://medium.com/ (search: "Subfinder" or "ProjectDiscovery Subfinder")
- https://infosecwriteups.com/ (search: "Subfinder")
- https://systemweakness.com/ (search: "Subfinder")
- https://www.youtube.com/results?search_query=projectdiscovery+subfinder

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\subfinder\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- References directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.
- Strategies and Tactics: Best sequences for combining operations and adapting follow-up passes when yield is thin, noisy, or rate-limited.

3. References Directory (`.cursor\skills\subfinder\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\SubFinder-Zero-to-Hero.md`): A markdown document that takes the user from zero to hero in using Subfinder for OSINT subdomain enumeration and nugget mapping.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\SubFinder-CLI-Options.md`): A markdown document that lists the standard Subfinder CLI options.

## CLI profiling alignment

When exercising Subfinder for the SpiderFeet corpus, follow `.cursor/skills/cli_app_profiling/SKILL.md` and `.cursor/rules/proj-06-spiderfeet-cli-app-exercising.mdc`:

- Draft a **semantic outcome matrix** before formal examination (rich subdomain set, clean miss, API-key failure, rate limit, wildcard/noisy parent, invalid domain).
- Prefer **`-oJ` JSONL** in exploration; at harvest, convert to a single JSON bundle with `records[]` (not raw `.jsonl` as the examination structured artifact).
- Validate argument forms in exploration before locking manifest commands (apex domain `-d`, not URL with scheme).
- Chain enrichment in strategy docs: **subfinder → dnsx → httpx → naabu → nuclei** where scope allows.

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to enumerate subdomains for an apex domain"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option.
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.
- Include a Strategies and Tactics section, which are the best strategies for combining some sequences of operations, and adapting depending on the results of the previous operations to maximise the returned data.
