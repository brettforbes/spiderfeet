# Creating a Skill and Documentation for Aircrack-ng, Scanning and Crack Wireless Networks

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for Aircrack-ng, When we are scanning networks and systems.

This skill will teach you how to use this tool to scan networks and systems. More importantly it should teach you how to adapt your technique, and your sequence of techniques in order to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.

The key is to exercise all of the different modules of aircrack-ng in a coordinated, orchestrated manner, to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan. You must be able to synthesis these techniques, and trhre various emans of hacking the network, distilling it all into the skill and references described below

You will use this skill to exercise Aircrack-ng in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables yout o get the wideset view on the source material you are going to caolsece into the skill and documentation.

- [aircrack-ng GitHub](https://github.com/aircrack-ng/aircrack-ng)
- [aircrack documentation](https://www.tuto-fr.com/tutoriaux/crack-wep/FAQ/en-aircrack-documentation.php#q000)
- [Airbase-ng](https://www.aircrack-ng.org/doku.php?id=airbase-ng)
- [Aircrack-ng](https://www.aircrack-ng.org/doku.php?id=aircrack-ng)
- [Airdecap-ng](https://www.aircrack-ng.org/doku.php?id=airdecap-ng)
- [Airdecloak-ng](https://www.aircrack-ng.org/doku.php?id=airdecloak-ng)
- [Airdrop-ng](https://www.aircrack-ng.org/doku.php?id=airdrop-ng)
- [Aireplay-ng](https://www.aircrack-ng.org/doku.php?id=aireplay-ng)
- [Aigraph-ng](https://www.aircrack-ng.org/doku.php?id=airgraph-ng)
- [Airmon-ng](https://www.aircrack-ng.org/doku.php?id=airmon-ng)
- [Airodump-ng](https://www.aircrack-ng.org/doku.php?id=airodump-ng)
- [Airolib-ng](https://www.aircrack-ng.org/doku.php?id=airolib-ng)
- [Easside-ng](https://www.aircrack-ng.org/doku.php?id=easside-ng)
- [Besside-ng](https://www.aircrack-ng.org/doku.php?id=besside-ng)
- [Wesside-ng](https://www.aircrack-ng.org/doku.php?id=wesside-ng)



Tutorials

- [Tutorial: WPA Packet Capture Explained](https://www.aircrack-ng.org/doku.php?id=wpa_capture)
- [Tutorial: ARP Request Injection Packet Capture Explained](https://www.aircrack-ng.org/doku.php?id=arp_inject_capture)
- [Tutorial: The art of ARP amplification](https://www.aircrack-ng.org/doku.php?id=arp_amplification)
- [Tutorial: How to crack WEP on a Wireless Distribution System (WDS)?](https://www.aircrack-ng.org/doku.php?id=wds)
- [Tutorial: Simple WEP Crack](https://www.aircrack-ng.org/doku.php?id=simple_wep_crack)
- [Simple Wep Cracking with a flowchart](https://www.aircrack-ng.org/doku.php?id=flowchart)
- [Tutorial: I am injecting but the IVs don't increase!](https://www.aircrack-ng.org/doku.php?id=i_am_injecting_but_the_ivs_don_t_increase)
- [Tutorial: How to crack WEP with no wireless clients](https://www.aircrack-ng.org/doku.php?id=how_to_crack_wep_with_no_clients)
- [Tutorial: How to crack WEP via a wireless client ?](https://www.aircrack-ng.org/doku.php?id=how_to_crack_wep_via_a_wireless_client)
- [Tutorial: How to do shared key fake authentication ?](https://www.aircrack-ng.org/doku.php?id=shared_key)
- [Tutorial: How to Crack WPA/WPA2](https://www.aircrack-ng.org/doku.php?id=cracking_wpa)



Blogs

- [Mastering Wireless Security: A Deep Dive into Aircrack-ng with Kali Linux](https://securewithsiva.in/post/08-aircrack-ng/)
- [Introduction to Wireless Security with Aircrack-ng](https://www.secureideas.com/blog/2018/09/introduction-to-wireless-security-with-aircrack-ng.html)
- [Hunt for Weak Spots in Your Wireless Network with Airodump-ng from the Aircrack-ng Suite](https://www.blackhillsinfosec.com/hunt-for-weak-spots-in-your-wireless-network-with-airodump-ng/)

## Instructions

Based strictly on the provided source materials, generate the following things:

1. Skill Trigger & Description (Max 50 words): A highly specific description of what this skill does and exactly when the AI should trigger it. (Include specific trigger words or scenarios).
2. SKILL.md Content (`.cursor\skills\Aircrack-ng\SKILL.md`): Deconstruct the workflows from my help docs into clear, step-by-step instructions for the AI. Organize it using the following headers:

- Purpose: A brief sentence on when to use this skill.
- Step-by-Step Instructions: Logical, sequential steps for how the agent should execute the task.
- If/Then Decision Rules: Any logic for edge cases based on the docs.
- Guardrails & Pitfalls: What the agent should avoid doing.
- Refences directory for details on the source material and how to use the tool, indexed through the `SKILLS.md` file.

3. References Directory (`.cursor\skills\Aircrack-ng\references`): A directory of references to the source material and how to use the tool, indexed through the `SKILLS.md` file.
4. Zero to Hero Document (`.docs\docs-for-cli-tools\Aircrack-Ng-Zero-to-Hero.md`): A markdown docuemnt that takes the user from zero to hero in using Aircrack-ng to Scanning and Crack Wireless Networks, including using each of the modules in a coordinated, orchestrated manner to maximise the resulting data from any network, regardless of how its systems seek to defeat your scan.
5. CLI Options Documentation (`.docs\docs-for-cli-tools\Aircrack-Ng-CLI-Options.md`): A markdown document that lists the standard Aircrack-ng CLI Options, for each of the modules to make a comprehensivce summary of the options for each module.

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- Meaning and Goals: The skill should tell the AI about the meaning of actions, and how they may be combined together to achieve a goal.
- Focus on Workflows over Features: The skill should tell the AI how to do something (e.g., "How to check out an e-book"), not just list a tool's features.
- Comprehensive Documentation: Every aspect of the  tool should be documented in the `references` sub directory next to the `SKILL.md` file, so the agent can use every option.
- Keep Descriptions Distinct: The short description of punchy sequences is critical. If it is too vague, the AI won't know when to use your skill instead of its standard tools.
- Include Comprehensive Examples: Include an example for every option in the `SKILL.md` file.
- Include a Strategies and Tactics section, which are the best strategies for combining some sequences of operations, and adapting depending on the results of the previous operations to maximise the returned data, and to be able to hack into wireless systems.