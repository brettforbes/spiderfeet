# Creating a Skill and Documentation for Nuclei, Scanning Networks and Systems

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for Nuclei, When we are scanning networks and systems.


This skill will teach you how to use this tool to scan networks and systems. More importantly it should teach you how to adapt your technique, and your sequence of techniques in order to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.

You will use this skill to exercise Nuclei in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables yout o get the wideset view on the source material you are going to caolsece into the skill and documentation.

### Project Discovery Nucleis documentation:

- [Nuclei Github Repo](https://github.com/projectdiscovery/nuclei)
- [Nuclei Overview](https://docs.projectdiscovery.io/opensource/nuclei/overview)
- [Installing Nuclei](https://docs.projectdiscovery.io/opensource/nuclei/install)
- [Running Nuclei](https://docs.projectdiscovery.io/opensource/nuclei/running)
- [Running Nuclei in CI/CD](https://docs.projectdiscovery.io/opensource/nuclei/ci-cd)
- [Supported Input Formats](https://docs.projectdiscovery.io/opensource/nuclei/input-formats)
- [Authenticated Scans](https://docs.projectdiscovery.io/opensource/nuclei/authenticated-scans)
- [Mass Scanning with Nuclei](https://docs.projectdiscovery.io/opensource/nuclei/mass-scanning-cli)
- [Nuclei SDK](https://docs.projectdiscovery.io/opensource/nuclei/nuclei-sdk)

Project Discovery Nuclei Blogs:

- [Nuclei: Packing a Punch with Vulnerability Scanning](https://bishopfox.com/blog/nuclei-vulnerability-scan)
- [The ultimate beginner’s guide to Nuclei](https://www.bugcrowd.com/blog/the-ultimate-beginners-guide-to-nuclei/)

### Project Discovery Nuclei Templates documentation:

- [Introduction to Nuclei Templates](https://docs.projectdiscovery.io/templates/introduction)
- [Nuclei Template Structure](https://docs.projectdiscovery.io/templates/structure)
- [Nuclei Templates FAQ](https://docs.projectdiscovery.io/templates/faq)
- [Basic HTTP Protocol](https://docs.projectdiscovery.io/templates/protocols/http/basic-http)
- [Raw HTTP Protocol](https://docs.projectdiscovery.io/templates/protocols/http/raw-http)
- [Fuzzing Overview](https://docs.projectdiscovery.io/templates/protocols/http/fuzzing-overview)
- [Fuzzing Examples](https://docs.projectdiscovery.io/templates/protocols/http/fuzzing-examples)
- [HTTP Payloads](https://docs.projectdiscovery.io/templates/protocols/http/http-payloads)
- [HTTP Payloads Examples](https://docs.projectdiscovery.io/templates/protocols/http/http-payloads-examples)
- [Unsafe HTTP](https://docs.projectdiscovery.io/templates/protocols/http/unsafe-http)
- [Value Sharing](https://docs.projectdiscovery.io/templates/protocols/http/value-sharing)
- [Connection Tampering](https://docs.projectdiscovery.io/templates/protocols/http/connection-tampering)
- [Request Tampering](https://docs.projectdiscovery.io/templates/protocols/http/request-tampering)
- [Race Conditions](https://docs.projectdiscovery.io/templates/protocols/http/race-conditions)
- [Headless Protocol](https://docs.projectdiscovery.io/templates/protocols/headless)
- [Network Protocol](https://docs.projectdiscovery.io/templates/protocols/network)
- [DNS Protocol](https://docs.projectdiscovery.io/templates/protocols/dns)
- [File Protocol](https://docs.projectdiscovery.io/templates/protocols/file)
- [Flow Protocol](https://docs.projectdiscovery.io/templates/protocols/flow)
- [Multi-protocol](https://docs.projectdiscovery.io/templates/protocols/multi-protocol)
- [Matchers](https://docs.projectdiscovery.io/templates/reference/matchers)
- [Extractors](https://docs.projectdiscovery.io/templates/reference/extractors)
- [Variables](https://docs.projectdiscovery.io/templates/reference/variables)
- [Template Workflows Overview](https://docs.projectdiscovery.io/templates/workflows/overview)
- [Workflow Examples](https://docs.projectdiscovery.io/templates/workflows/examples)

Project Discovery Tempaltes Blogs:

- [Leveraging Nuclei Templates to Identify Risks and Threats in Critical Cloud Applications](https://orca.security/resources/blog/using-nuclei-templates-for-vulnerability-scanning/)
- [If you're not writing custom Nuclei templates, you're missing out](https://projectdiscovery.io/blog/if-youre-not-writing-custom-nuclei-templates-youre-missing-out)
- [The Power of Nuclei Templates: A Universal Language of Vulnerabilities](https://projectdiscovery.io/blog/the-power-of-nuclei-templates-a-universal-language-of-vulnerabilities)

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\nuclei\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- Refences directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.

3. References Directory (`.cursor\skills\nuclei\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\Nuclei-Zero-to-Hero.md`): A markdown docuemnt that takes the user from zero to hero in using Nuclei to scan networks and systems.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\Nuclei-CLI-Options.md`): A markdown document that lists the standard Nuclei CLI Options doc

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to check out an e-book"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the  tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option.
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.
- Include a Strategies and Tactics section, which are the best strategies for combining some sequences of operations, and adapting depending on the results of the previous operations to maximise the returned data.