# CLI Tool Skills & Documentation — Build Summary

Base repo: `c:\projects\spiderfeet`

## Master table

| Tool | Agent skill | References index | Zero-to-Hero | CLI options | Primary parser |
|------|-------------|------------------|--------------|-------------|----------------|
| TextFSM | [SKILL.md](.cursor/skills/textfsm/SKILL.md) | [references/SKILLS.md](.cursor/skills/textfsm/references/SKILLS.md) | [TextFMS-Zero-to-Hero.md](.docs/docs-for-cli-tools/TextFMS-Zero-to-Hero.md) | — | TextFSM |
| TextFSM NTC Templates | [SKILL.md](.cursor/skills/textfsm_templates/SKILL.md) | [references/SKILLS.md](.cursor/skills/textfsm_templates/references/SKILLS.md) | [TextFSM-Templates-Zero-to-Hero.md](.docs/docs-for-cli-tools/TextFSM-Templates-Zero-to-Hero.md) | — | `ntc_templates.parse_output` |
| Nmap | [SKILL.md](.cursor/skills/nmap/SKILL.md) | [references/SKILLS.md](.cursor/skills/nmap/references/SKILLS.md) | [NMAP-Zero-to-Hero.md](.docs/docs-for-cli-tools/NMAP-Zero-to-Hero.md) | [NMAP-CLI-Options.md](.docs/docs-for-cli-tools/NMAP-CLI-Options.md) | XML (`-oX`) |
| Naabu | [SKILL.md](.cursor/skills/naabu/SKILL.md) | [references/SKILLS.md](.cursor/skills/naabu/references/SKILLS.md) | [Naabu-Zero-to-Hero.md](.docs/docs-for-cli-tools/Naabu-Zero-to-Hero.md) | [Naabu-CLI-Options.md](.docs/docs-for-cli-tools/Naabu-CLI-Options.md) | JSON Lines (`-json`) |
| NetDiscover | [SKILL.md](.cursor/skills/netdiscover/SKILL.md) | [references/SKILLS.md](.cursor/skills/netdiscover/references/SKILLS.md) | [NetDiscover-Zero-to-Hero.md](.docs/docs-for-cli-tools/NetDiscover-Zero-to-Hero.md) | [NetDiscover-CLI-Options.md](.docs/docs-for-cli-tools/NetDiscover-CLI-Options.md) | TextFSM (`-P`) |
| Nerva | [SKILL.md](.cursor/skills/nerva/SKILL.md) | [references/SKILLS.md](.cursor/skills/nerva/references/SKILLS.md) | [Nerva-Zero-to-Hero.md](.docs/docs-for-cli-tools/Nerva-Zero-to-Hero.md) | [Nerva-CLI-Options.md](.docs/docs-for-cli-tools/Nerva-CLI-Options.md) | JSON (`--json`) |
| Julius | [SKILL.md](.cursor/skills/julius/SKILL.md) | [references/SKILLS.md](.cursor/skills/julius/references/SKILLS.md) | [Julius-Zero-to-Hero.md](.docs/docs-for-cli-tools/Julius-Zero-to-Hero.md) | [Julius-CLI-Options.md](.docs/docs-for-cli-tools/Julius-CLI-Options.md) | JSON / JSONL (`-o jsonl`) |
| Nuclei | [SKILL.md](.cursor/skills/nuclei/SKILL.md) | [references/SKILLS.md](.cursor/skills/nuclei/references/SKILLS.md) | [Nuclei-Zero-to-Hero.md](.docs/docs-for-cli-tools/Nuclei-Zero-to-Hero.md) | [Nuclei-CLI-Options.md](.docs/docs-for-cli-tools/Nuclei-CLI-Options.md) | JSONL (`-jsonl`) |
| Aircrack-ng | [SKILL.md](.cursor/skills/aircrack-ng/SKILL.md) | [references/SKILLS.md](.cursor/skills/aircrack-ng/references/SKILLS.md) | [Aircrack-Ng-Zero-to-Hero.md](.docs/docs-for-cli-tools/Aircrack-Ng-Zero-to-Hero.md) | [Aircrack-Ng-CLI-Options.md](.docs/docs-for-cli-tools/Aircrack-Ng-CLI-Options.md) | TextFSM (airodump CSV) |
| CMSeeK | [SKILL.md](.cursor/skills/cmseek/SKILL.md) | [references/SKILLS.md](.cursor/skills/cmseek/references/SKILLS.md) | [CMSeeK-Zero-to-Hero.md](.docs/docs-for-cli-tools/CMSeeK-Zero-to-Hero.md) | [CMSeeK-CLI-Options.md](.docs/docs-for-cli-tools/CMSeeK-CLI-Options.md) | JSON (`cms.json`) |
| WAFWOOF | [SKILL.md](.cursor/skills/wafwoof/SKILL.md) | [references/SKILLS.md](.cursor/skills/wafwoof/references/SKILLS.md) | [WAFWOOF-Zero-to-Hero.md](.docs/docs-for-cli-tools/WAFWOOF-Zero-to-Hero.md) | [WAFWOOF-CLI-Options.md](.docs/docs-for-cli-tools/WAFWOOF-CLI-Options.md) | JSON (`-f json`) |
| Pius | [SKILL.md](.cursor/skills/pius/SKILL.md) | [references/SKILLS.md](.cursor/skills/pius/references/SKILLS.md) | [PIUS-Zero-to-Hero.md](.docs/docs-for-cli-tools/PIUS-Zero-to-Hero.md) | [PIUS-CLI-Options.md](.docs/docs-for-cli-tools/PIUS-CLI-Options.md) | NDJSON (`--output ndjson`) |
| Nosey Parker | [SKILL.md](.cursor/skills/nosey_parker/SKILL.md) | [references/SKILLS.md](.cursor/skills/nosey_parker/references/SKILLS.md) | [Nosey-Parker-Zero-to-Hero.md](.docs/docs-for-cli-tools/Nosey-Parker-Zero-to-Hero.md) | [Nosey-Parker-CLI-Options.md](.docs/docs-for-cli-tools/Nosey-Parker-CLI-Options.md) | JSONL / findings DB |
| NTLMRecon | [SKILL.md](.cursor/skills/NTLMRecon/SKILL.md) | [references/SKILLS.md](.cursor/skills/NTLMRecon/references/SKILLS.md) | [NTLMRecon-Zero-to-Hero.md](.docs/docs-for-cli-tools/NTLMRecon-Zero-to-Hero.md) | [NTLMRecon-CLI-Options.md](.docs/docs-for-cli-tools/NTLMRecon-CLI-Options.md) | Text / optional JSON |
| Titus | [SKILL.md](.cursor/skills/Titus/SKILL.md) | [references/SKILLS.md](.cursor/skills/Titus/references/SKILLS.md) | [Titus-Zero-to-Hero.md](.docs/docs-for-cli-tools/Titus-Zero-to-Hero.md) | [Titus-CLI-Options.md](.docs/docs-for-cli-tools/Titus-CLI-Options.md) | JSON / SARIF / text |
| Trajan | [SKILL.md](.cursor/skills/trajan/SKILL.md) | [references/SKILLS.md](.cursor/skills/trajan/references/SKILLS.md) | [Trajan-Zero-to-Hero.md](.docs/docs-for-cli-tools/Trajan-Zero-to-Hero.md) | [Trajan-CLI-Options.md](.docs/docs-for-cli-tools/Trajan-CLI-Options.md) | JSON / SARIF |
| Vespasian | [SKILL.md](.cursor/skills/vespian/SKILL.md) | [references/SKILLS.md](.cursor/skills/vespian/references/SKILLS.md) | [Vespasian-Zero-to-Hero.md](.docs/docs-for-cli-tools/Vespasian-Zero-to-Hero.md) | [Vespasian-CLI-Options.md](.docs/docs-for-cli-tools/Vespasian-CLI-Options.md) | JSON / graph data |
| Aurelian | [SKILL.md](.cursor/skills/Aurelian/SKILL.md) | [references/SKILLS.md](.cursor/skills/Aurelian/references/SKILLS.md) | [Aurelian-Zero-to-Hero.md](.docs/docs-for-cli-tools/Aurelian-Zero-to-Hero.md) | [Aurelian-CLI-Options.md](.docs/docs-for-cli-tools/Aurelian-CLI-Options.md) | JSON / findings |
| Augustus | [SKILL.md](.cursor/skills/Augustus/SKILL.md) | [references/SKILLS.md](.cursor/skills/Augustus/references/SKILLS.md) | [Augustus-Zero-to-Hero.md](.docs/docs-for-cli-tools/Augustus-Zero-to-Hero.md) | [Augustus-CLI-Options.md](.docs/docs-for-cli-tools/Augustus-CLI-Options.md) | JSON / report text |
| dnsx | [SKILL.md](.cursor/skills/dnsx/SKILL.md) | [references/SKILLS.md](.cursor/skills/dnsx/references/SKILLS.md) | [dnsx-Zero-to-Hero.md](.docs/docs-for-cli-tools/dnsx-Zero-to-Hero.md) | [dnsx-CLI-Options.md](.docs/docs-for-cli-tools/dnsx-CLI-Options.md) | JSON / line output |
| webanalyze | [SKILL.md](.cursor/skills/webanalyze/SKILL.md) | [references/SKILLS.md](.cursor/skills/webanalyze/references/SKILLS.md) | [webanalyze-Zero-to-Hero.md](.docs/docs-for-cli-tools/webanalyze-Zero-to-Hero.md) | [webanalyze-CLI-Options.md](.docs/docs-for-cli-tools/webanalyze-CLI-Options.md) | JSON |
| tldfinder | [SKILL.md](.cursor/skills/tldfinder/SKILL.md) | [references/SKILLS.md](.cursor/skills/tldfinder/references/SKILLS.md) | [tldfinder-Zero-to-Hero.md](.docs/docs-for-cli-tools/tldfinder-Zero-to-Hero.md) | [tldfinder-CLI-Options.md](.docs/docs-for-cli-tools/tldfinder-CLI-Options.md) | JSON / text |
| katana | [SKILL.md](.cursor/skills/katana/SKILL.md) | [references/SKILLS.md](.cursor/skills/katana/references/SKILLS.md) | [katana-Zero-to-Hero.md](.docs/docs-for-cli-tools/katana-Zero-to-Hero.md) | [katana-CLI-Options.md](.docs/docs-for-cli-tools/katana-CLI-Options.md) | JSONL / crawl output |
| mapcidr | [SKILL.md](.cursor/skills/mapcidr/SKILL.md) | [references/SKILLS.md](.cursor/skills/mapcidr/references/SKILLS.md) | [mapcidr-Zero-to-Hero.md](.docs/docs-for-cli-tools/mapcidr-Zero-to-Hero.md) | [mapcidr-CLI-Options.md](.docs/docs-for-cli-tools/mapcidr-CLI-Options.md) | Text / expanded CIDRs |
| uncover | [SKILL.md](.cursor/skills/uncover/SKILL.md) | [references/SKILLS.md](.cursor/skills/uncover/references/SKILLS.md) | [uncover-Zero-to-Hero.md](.docs/docs-for-cli-tools/uncover-Zero-to-Hero.md) | [uncover-CLI-Options.md](.docs/docs-for-cli-tools/uncover-CLI-Options.md) | JSONL / provider output |
| recon-ng | [SKILL.md](.cursor/skills/recon_ng/SKILL.md) | [references/SKILLS.md](.cursor/skills/recon_ng/references/SKILLS.md) | [recon-ng-Zero-to-Hero.md](.docs/docs-for-cli-tools/recon-ng-Zero-to-Hero.md) | [recon-ng-CLI-Options.md](.docs/docs-for-cli-tools/recon-ng-CLI-Options.md) | SQLite workspace + exports |
| Metasploit Framework | [SKILL.md](.cursor/skills/metasploit_framework/SKILL.md) | [references/SKILLS.md](.cursor/skills/metasploit_framework/references/SKILLS.md) | [Metasploit-Framework-Zero-to-Hero.md](.docs/docs-for-cli-tools/Metasploit-Framework-Zero-to-Hero.md) | [Metasploit-Framework-CLI-Options.md](.docs/docs-for-cli-tools/Metasploit-Framework-CLI-Options.md) | DB tables + console/export parsing |

## Graph structure documents (CLI profiling corpus)

Approved semantic graph shapes for the widget **CLI Profiling** tab. Combined cross-tool view: [_Current_Ontology.md](_Current_Ontology.md).

| Tool | Structure doc | Generator |
|------|---------------|-----------|
| Nmap | [nmap_nugget_graph_structure.md](nugget_structure/nmap_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/nmap_xml_to_graph.py` |
| Netdiscover | [netdiscover_nugget_graph_structure.md](nugget_structure/netdiscover_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/netdiscover_json_to_graph.py` |
| Nerva | [nerva_nugget_graph_structure.md](nugget_structure/nerva_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/cli_tool_to_graph.py` (`nerva_to_graph`) |
| Pius | [pius_nugget_graph_structure.md](nugget_structure/pius_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/cli_tool_to_graph.py` (`pius_to_graph`) |

**Nmap service nuggets (2026-06):** `SERVICE_VERSION`, `SERVICE_FINGERPRINT`, `SERVICE_EXTRAINFO`; `listens-to` for every port with a reported service name (including filtered ports).

## Reference files by tool

### TextFSM NTC Templates — `.cursor/skills/textfsm_templates/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/textfsm_templates/references/SKILLS.md) |
| Parse API | [parse-api.md](.cursor/skills/textfsm_templates/references/parse-api.md) |
| Platform index | [platform-index.md](.cursor/skills/textfsm_templates/references/platform-index.md) |
| Extending templates | [extending-templates.md](.cursor/skills/textfsm_templates/references/extending-templates.md) |
| Nugget conversion | [nugget-conversion.md](.cursor/skills/textfsm_templates/references/nugget-conversion.md) |
| Use cases & workflow | [use-cases-and-workflow.md](.cursor/skills/textfsm_templates/references/use-cases-and-workflow.md) |
| TextFSM syntax primer | [textfsm-syntax-primer.md](.cursor/skills/textfsm_templates/references/textfsm-syntax-primer.md) |
| Sources | [sources.md](.cursor/skills/textfsm_templates/references/sources.md) |

**Sibling skill:** [textfsm/SKILL.md](.cursor/skills/textfsm/SKILL.md) (raw TextFSM authoring)

### TextFSM — `.cursor/skills/textfsm/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/textfsm/references/SKILLS.md) |
| Template syntax | [template-syntax.md](.cursor/skills/textfsm/references/template-syntax.md) |
| Python API | [python-api.md](.cursor/skills/textfsm/references/python-api.md) |
| CliTable | [clitable.md](.cursor/skills/textfsm/references/clitable.md) |
| Nugget mapping | [nugget-conversion.md](.cursor/skills/textfsm/references/nugget-conversion.md) |
| Pitfalls & examples | [pitfalls-and-examples.md](.cursor/skills/textfsm/references/pitfalls-and-examples.md) |
| Sources | [sources.md](.cursor/skills/textfsm/references/sources.md) |

### Nmap — `.cursor/skills/nmap/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/nmap/references/SKILLS.md) |
| XML output schema | [xml-output-schema.md](.cursor/skills/nmap/references/xml-output-schema.md) |
| Workflows & phases | [workflows-and-phases.md](.cursor/skills/nmap/references/workflows-and-phases.md) |
| Evasion & tactics | [evasion-and-tactics.md](.cursor/skills/nmap/references/evasion-and-tactics.md) |
| CLI flags | [cli-flags.md](.cursor/skills/nmap/references/cli-flags.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/nmap/references/nugget-mapping.md) |
| Sources | [sources.md](.cursor/skills/nmap/references/sources.md) |

### Naabu — `.cursor/skills/naabu/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/naabu/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/naabu/references/cli-options.md) |
| JSON output schema | [json-output-schema.md](.cursor/skills/naabu/references/json-output-schema.md) |
| Workflows & phases | [workflows-and-phases.md](.cursor/skills/naabu/references/workflows-and-phases.md) |
| Nmap integration | [nmap-integration.md](.cursor/skills/naabu/references/nmap-integration.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/naabu/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/naabu/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/naabu/references/sources.md) |

### Julius — `.cursor/skills/julius/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/julius/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/julius/references/cli-options.md) |
| JSON output schema | [json-output-schema.md](.cursor/skills/julius/references/json-output-schema.md) |
| Probes & services | [probes-and-services.md](.cursor/skills/julius/references/probes-and-services.md) |
| Workflows & phases | [workflows-and-phases.md](.cursor/skills/julius/references/workflows-and-phases.md) |
| Match rules & probes | [match-rules-and-probes.md](.cursor/skills/julius/references/match-rules-and-probes.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/julius/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/julius/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/julius/references/sources.md) |

### NetDiscover — `.cursor/skills/netdiscover/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/netdiscover/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/netdiscover/references/cli-options.md) |
| Output & parsing | [output-and-parsing.md](.cursor/skills/netdiscover/references/output-and-parsing.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/netdiscover/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/netdiscover/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/netdiscover/references/sources.md) |

### Nerva — `.cursor/skills/nerva/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/nerva/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/nerva/references/cli-options.md) |
| JSON output schema | [json-output-schema.md](.cursor/skills/nerva/references/json-output-schema.md) |
| Protocol list | [protocol-list.md](.cursor/skills/nerva/references/protocol-list.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/nerva/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/nerva/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/nerva/references/sources.md) |

### Nuclei — `.cursor/skills/nuclei/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/nuclei/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/nuclei/references/cli-options.md) |
| JSONL output schema | [jsonl-output-schema.md](.cursor/skills/nuclei/references/jsonl-output-schema.md) |
| Templates & workflows | [templates-and-workflows.md](.cursor/skills/nuclei/references/templates-and-workflows.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/nuclei/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/nuclei/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/nuclei/references/sources.md) |

### Aircrack-ng — `.cursor/skills/aircrack-ng/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/aircrack-ng/references/SKILLS.md) |
| CLI options by module | [cli-options-by-module.md](.cursor/skills/aircrack-ng/references/cli-options-by-module.md) |
| Workflows | [workflows.md](.cursor/skills/aircrack-ng/references/workflows.md) |
| Output & parsing | [output-and-parsing.md](.cursor/skills/aircrack-ng/references/output-and-parsing.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/aircrack-ng/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/aircrack-ng/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/aircrack-ng/references/sources.md) |

### CMSeeK — `.cursor/skills/cmseek/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/cmseek/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/cmseek/references/cli-options.md) |
| Output schema | [output-schema.md](.cursor/skills/cmseek/references/output-schema.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/cmseek/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/cmseek/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/cmseek/references/sources.md) |

### WAFWOOF — `.cursor/skills/wafwoof/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/wafwoof/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/wafwoof/references/cli-options.md) |
| JSON output schema | [json-output-schema.md](.cursor/skills/wafwoof/references/json-output-schema.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/wafwoof/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/wafwoof/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/wafwoof/references/sources.md) |

### Pius — `.cursor/skills/pius/references/`

| File | Link |
|------|------|
| Index | [SKILLS.md](.cursor/skills/pius/references/SKILLS.md) |
| CLI options | [cli-options.md](.cursor/skills/pius/references/cli-options.md) |
| NDJSON output schema | [ndjson-output-schema.md](.cursor/skills/pius/references/ndjson-output-schema.md) |
| Plugins & phases | [plugins-and-phases.md](.cursor/skills/pius/references/plugins-and-phases.md) |
| Nugget mapping | [nugget-mapping.md](.cursor/skills/pius/references/nugget-mapping.md) |
| Tactics | [tactics.md](.cursor/skills/pius/references/tactics.md) |
| Sources | [sources.md](.cursor/skills/pius/references/sources.md) |

### Additional tools (03J–03V) — references index links

| Tool | References index |
|------|------------------|
| Nosey Parker | [SKILLS.md](.cursor/skills/nosey_parker/references/SKILLS.md) |
| NTLMRecon | [SKILLS.md](.cursor/skills/NTLMRecon/references/SKILLS.md) |
| Titus | [SKILLS.md](.cursor/skills/Titus/references/SKILLS.md) |
| Trajan | [SKILLS.md](.cursor/skills/trajan/references/SKILLS.md) |
| Vespasian | [SKILLS.md](.cursor/skills/vespian/references/SKILLS.md) |
| Aurelian | [SKILLS.md](.cursor/skills/Aurelian/references/SKILLS.md) |
| Augustus | [SKILLS.md](.cursor/skills/Augustus/references/SKILLS.md) |
| dnsx | [SKILLS.md](.cursor/skills/dnsx/references/SKILLS.md) |
| webanalyze | [SKILLS.md](.cursor/skills/webanalyze/references/SKILLS.md) |
| tldfinder | [SKILLS.md](.cursor/skills/tldfinder/references/SKILLS.md) |
| katana | [SKILLS.md](.cursor/skills/katana/references/SKILLS.md) |
| mapcidr | [SKILLS.md](.cursor/skills/mapcidr/references/SKILLS.md) |
| uncover | [SKILLS.md](.cursor/skills/uncover/references/SKILLS.md) |
| recon-ng | [SKILLS.md](.cursor/skills/recon_ng/references/SKILLS.md) |
| Metasploit Framework | [SKILLS.md](.cursor/skills/metasploit_framework/references/SKILLS.md) |

## Prompt sources (instructions used)

| Tool | Prompt file |
|------|-------------|
| TextFSM | [.seed/03A_Prompt_Making_for_TextFSM.md](.seed/03A_Prompt_Making_for_TextFSM.md) |
| TextFSM NTC Templates | [.seed/03A2_Prompt_Making_for_TextFSM_NTC_Templates.md](.seed/03A2_Prompt_Making_for_TextFSM_NTC_Templates.md) |
| Nmap | [.seed/03B_Prompt_Making_for_NMAP.md](.seed/03B_Prompt_Making_for_NMAP.md) |
| NetDiscover | [.seed/03C_Prompt_Making_for_NetDiscover.md](.seed/03C_Prompt_Making_for_NetDiscover.md) |
| Nerva | [.seed/03D_Prompt_Making_for_Nerva.md](.seed/03D_Prompt_Making_for_Nerva.md) |
| Nuclei | [.seed/03E_Prompt_Making_for_Nuclei.md](.seed/03E_Prompt_Making_for_Nuclei.md) |
| Aircrack-ng | [.seed/03F_Prompt_Making_for_Aircrack_ng.md](.seed/03F_Prompt_Making_for_Aircrack_ng.md) |
| CMSeeK | [.seed/03G_Prompt_Making_for_CMSeeK.md](.seed/03G_Prompt_Making_for_CMSeeK.md) |
| WAFWOOF | [.seed/03H_Prompt_Making_for_WAFWOOF.md](.seed/03H_Prompt_Making_for_WAFWOOF.md) |
| Pius | [.seed/03I_Prompt_Making_for_Pius.md](.seed/03I_Prompt_Making_for_Pius.md) |
| Nosey Parker | [.seed/03J_Prompt_Making_for_Nosey_Parker.md](.seed/03J_Prompt_Making_for_Nosey_Parker.md) |
| NTLMRecon | [.seed/03K_Prompt_Making_for_NTLMRecon.md](.seed/03K_Prompt_Making_for_NTLMRecon.md) |
| Titus | [.seed/03L_Prompt_Making_for_Titus.md](.seed/03L_Prompt_Making_for_Titus.md) |
| Trajan | [.seed/03M_Prompt_Making_for_trajan.md](.seed/03M_Prompt_Making_for_trajan.md) |
| Vespasian | [.seed/03N_Prompt_Making_for_vespian.md](.seed/03N_Prompt_Making_for_vespian.md) |
| Aurelian | [.seed/03O_Prompt_Making_for_Aurelian.md](.seed/03O_Prompt_Making_for_Aurelian.md) |
| Augustus | [.seed/03P_Prompt_Making_for_Augustus.md](.seed/03P_Prompt_Making_for_Augustus.md) |
| dnsx | [.seed/03Q_Prompt_Making_for_dnsx.md](.seed/03Q_Prompt_Making_for_dnsx.md) |
| webanalyze | [.seed/03R_Prompt_Making_for_webanalyze.md](.seed/03R_Prompt_Making_for_webanalyze.md) |
| tldfinder | [.seed/03S_Prompt_Making_for_tldfinder.md](.seed/03S_Prompt_Making_for_tldfinder.md) |
| katana | [.seed/03T_Prompt_Making_for_katana.md](.seed/03T_Prompt_Making_for_katana.md) |
| mapcidr | [.seed/03U_Prompt_Making_for_mapcidr.md](.seed/03U_Prompt_Making_for_mapcidr.md) |
| uncover | [.seed/03V_Prompt_Making_for_uncover.md](.seed/03V_Prompt_Making_for_uncover.md) |
| recon-ng | [.seed/03W_Prompt_Making_for_recon-ng.md](.seed/03W_Prompt_Making_for_recon-ng.md) |
| Metasploit Framework | [.seed/03X_Prompt_Making_for_Metasploit_Framework.md](.seed/03X_Prompt_Making_for_Metasploit_Framework.md) |
| Julius | [.seed/03Y_Prompt_Making_for_Julius.md](.seed/03Y_Prompt_Making_for_Julius.md) |
| Naabu | [.seed/03Z_Prompt_Making_for_Naabu.md](.seed/03Z_Prompt_Making_for_Naabu.md) |

## Related SpiderFeet context

| Resource | Link |
|----------|------|
| **Current ontology (Nmap + Netdiscover)** | [_Current_Ontology.md](_Current_Ontology.md) |
| Nugget vocabulary | [.docs/analysis/nuggets.json](.docs/analysis/nuggets.json) |
| Nugget extensions (CLI profiling) | [.docs/analysis/nuggets_extension.json](.docs/analysis/nuggets_extension.json) |
| Parsing primitives | [.docs/analysis/conversion_to_types/03-parsing-primitives.md](.docs/analysis/conversion_to_types/03-parsing-primitives.md) |
| All Zero-to-Hero docs | [.docs/docs-for-cli-tools/](.docs/docs-for-cli-tools/) |