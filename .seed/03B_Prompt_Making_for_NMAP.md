# Creating a Skill and Documentation for NMAP, Scanning Networks and Systems

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for NMAP, When we are scanning networks and systems, we will export them in xml, and convert those results to nested nuggets

This skill will teach you how to use this tool to scan networks and systems. More importantly it should teach you how to adapt your technique, and your sequence of techniques in order to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.

You will use this skill to exercise NMAP in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables yout o get the wideset view on the source material you are going to caolsece into the skill and documentation.

- [Command-line Flags](https://nmap.org/book/output-formats-commandline-flags.html)
- [We will use XML OUtout Exclusively](https://nmap.org/book/output-formats-xml-output.html#output-formats-xml-port-elements)
- [XML-DTD](https://nmap.org/book/nmap-dtd.html)
- [Target Specification](https://nmap.org/book/man-target-specification.html)
- [Host Discovery](https://nmap.org/book/man-host-discovery.html)
- [Port Scanning Basics](https://nmap.org/book/man-port-scanning-basics.html)
- [Port Scanning Techniques](https://nmap.org/book/man-port-scanning-techniques.html)
- [OS Detection](https://nmap.org/book/man-os-detection.html)
- [OS Detection Techniques](https://nmap.org/book/osdetection-guessing.html)
- [Port Specification and Scan Order](https://nmap.org/book/man-port-specification.html)
- [The Phases of an Nmap Scan](https://nmap.org/book/nmap-phases.html)
- [Timing and Performance](https://nmap.org/book/man-performance.html)
- [Nmap Scripting Engine](https://nmap.org/book/man-nse.html)
- [Firewall/IDS Evasion and Spoofing](https://nmap.org/book/man-bypass-firewalls-ids.html)

Some NMAP Blog Posts

- [Nmap: The Complete Guide From Beginner to Advanced](https://blog.geekinstitute.org/2024/11/nmap-network-mapping-and-security-scanning.html)
- [Complete guide to parsing NMap XML output: Python scripts, automation techniques, and best practices for security professionals. Convert to CSV/JSON easily.](https://styran.com/using-nmap-xml-output/)

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\nmap\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- Refences directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.

3. References Directory (`.cursor\skills\nmap\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\NMAP-Zero-to-Hero.md`): A markdown document that takes the user from zero to hero in using Nmap for OSINT scanning and nugget mapping.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\NMAP-CLI-Options.md`): A markdown document that lists the standard NMAP CLI Options doc

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to check out an e-book"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the  tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option.
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.
- Include a Strategies and Tactics section, which are the best strategies for combining some sequences of operations, and adapting depending on the results of the previous operations to maximise the returned data.