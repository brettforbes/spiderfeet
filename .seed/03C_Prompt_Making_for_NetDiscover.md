# Creating a Skill and Documentation for NetDiscover, Using NetDiscover to find Network Devices

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for NetDiscover, When we are scanning networks and systems.


This skill will teach you how to use this tool to scan networks and systems. More importantly it should teach you how to adapt your technique, and your sequence of techniques in order to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.

You will use this skill to exercise Pius in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables yout o get the wideset view on the source material you are going to caolsece into the skill and documentation.

- [netdiscover github](https://github.com/netdiscover-scanner/netdiscover)
- [netdiscover man page](https://manpages.ubuntu.com/manpages/bionic/man8/netdiscover.8.html)
- [Netdiscover Command guide: Network Discovery and ARP Reconnaissance Tool](https://infosecone.com/blog/netdiscover-command-network-discovery-tool/)

The Python for Netowrk Engineers Book

- [Netdiscover: The ARP-based Network Discovery Tool Every Pentester Should Know ](https://blog.geekinstitute.org/2025/05/netdiscover-arp-based-network-discovery-tool.html)
- [Unlocking Network Visibility: How to Discover Hosts Efficiently with NetDiscover](https://www.examcollection.com/blog/unlocking-network-visibility-how-to-discover-hosts-efficiently-with-netdiscover/)
- [Network Discovery with Nmap and Netdiscover](https://spreadsecurity.github.io/2016/09/25/network-discovery-with-nmap-and-netdiscover.html)

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\netdiscover\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- Refences directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.

3. References Directory (`.cursor\skills\netdiscover\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\NetDiscover-Zero-to-Hero.md`): A markdown docuemnt that takes the user from zero to hero in using NetDiscover to scan networks and systems, including using each of the modules in a coordinated, orchestrated manner to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\NetDiscover-CLI-Options.md`): A markdown document that lists the standard NetDiscover CLI Options doc for each of the modules to make a comprehensive summary of the options for each module.

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to check out an e-book"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the  tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option.
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.
- Include a Strategies and Tactics section, which are the best strategies for combining some sequences of operations, and adapting depending on the results of the previous operations to maximise the returned data.
- Understand how to combine NetDiscover and NMAP to get the best results.