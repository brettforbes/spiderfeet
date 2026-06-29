# Creating a Skill and Documentation for Naabu, Scanning Networks and Systems

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for Naabu, When we are scanning ports, we will export them in json, and convert those results to nested nuggets

This skill will teach you how to use this tool to scan networks and systems. More importantly it should teach you how to adapt your technique, and your sequence of techniques in order to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.

You will use this skill to exercise Naabu in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables yout o get the wideset view on the source material you are going to caolsece into the skill and documentation.

- [naabu github repository](https://github.com/projectdiscovery/naabu)
- [Naabu Overview](https://docs.projectdiscovery.io/opensource/naabu/overview)
- [Installing Naabu](https://docs.projectdiscovery.io/opensource/naabu/install)
- [Naabu Usage](https://docs.projectdiscovery.io/opensource/naabu/usage)
- [Running Naabu](https://docs.projectdiscovery.io/opensource/naabu/running)

Some Naabu Blog Posts

- [Improving port scans against API servers](https://danaepp.com/improving-port-scans-against-api-servers)
- [Naabu Details](https://www.rootsec.in/tools/port-scanning/network-scanners/naabu)
- [Naabu: Cheat Sheet](https://highon.coffee/blog/naabu-cheat-sheet/)
- [Recon series #4: Port scanning – uncovering attack vectors by revealing open ports and hidden services](https://www.yeswehack.com/learn-bug-bounty/recon-port-scanning-attack-vectors)
- [Port Scanning In Cybersecurity: Fundamental Skill for Implementation](https://www.hackingloops.com/port-scanning-in-cybersecurity/)
- [naabu: powerful portscanning tool for bug hunters](https://medium.com/@loyalonlytoday/naabu-powerful-portscanning-tool-for-bug-hunters-758860a6526b)
- [naabu Port scanning tool](https://www.freshports.org/security/naabu/)
- [Naabu Port Scanner —A brief note](https://mrshan.medium.com/naabu-port-scanner-why-you-should-use-it-947d8ca025df)

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\naabu\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- Refences directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.

3. References Directory (`.cursor\skills\naabu\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\Naabu-Zero-to-Hero.md`): A markdown document that takes the user from zero to hero in using Naabu for OSINT scanning and nugget mapping.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\Naabu-CLI-Options.md`): A markdown document that lists the standard Naabu CLI Options doc

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to check out an e-book"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the  tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option.
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.
- Include a Strategies and Tactics section, which are the best strategies for combining some sequences of operations, and adapting depending on the results of the previous operations to maximise the returned data.