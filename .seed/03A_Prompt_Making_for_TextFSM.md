# Creating a Skill and Documentation for TextFSM, Parsing CLI App Output into Nuggets

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for TextFSM, When we are parsing CLI App Output into Nuggets.

We will install many CLI tools, run them through their options. Any that export text output, we will:

- capture that output, 
- identify all of the data nuggets we can extract from the output, and then 
- use TextFSM to parse the output into a structured format, 
- which is then converted into nuggets.



## Source Material

The total source material, from code to docs to blog posts enables yout o get the wideset view on the source material you are going to caolsece into the skill and documentation.

- [textfsm GitHub Repository](https://github.com/google/textfsm)
- [How-to Wiki](https://code.google.com/archive/p/textfsm/wikis/TextFSMCodeLab.wiki)
- [TextFSM Code Lab](https://textfsm.readthedocs.io/en/latest/blog/)
- [TextFSM Table Extraction](hhttps://code.google.com/archive/p/textfsm/wikis/CliTableHowTo.wiki)

The Python for Netowrk Engineers Book

- [Getting Started with TextFSM](https://pyneng.readthedocs.io/en/latest/book/21_textfsm/README.html#)
- [TextFSM template syntax](https://pyneng.readthedocs.io/en/latest/book/21_textfsm/textfsm_syntax.html)
- [Examples of TextFSM Usage](https://pyneng.readthedocs.io/en/latest/book/21_textfsm/textfsm_examples.html)
- [TextFSM Table Extraction](https://pyneng.readthedocs.io/en/latest/book/21_textfsm/textfsm_clitable.htmll)

Blog Posts

- [Parsing Output](https://codingnetworker.com/2015/08/parse-cli-outputs-textfsm/)

## Instructions

Assume that you want to write the skill for the following scenario

### Build a Skill to fit this Scenario

The agent using the skill will  be provided with one or more pairs of details:

- output text sample from the CLI tool
- the hierarchy of data nuggets we want to extract from the output as a nodes and edges array

The agent will need to use the skill to create a function using the TextFSM library to create the nodes and edges array from the output text. If multiple samples of text and nugget/edge arrays are provided, the agent will seek to make a common function if at all possible.

### How to Build the Skill

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\textfsm\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- Refences directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.

3. References Directory (`.cursor\skills\textfsm\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\TextFMS-Zero-to-Hero.md`): A markdown docuemnt that takes the user from zero to hero in using TextFSM to parse CLI App Output into Nuggets.

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to check out an e-book"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the  tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option. Do not overly simplify detail, instead pack it in the references and index it in the skill document itself
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.