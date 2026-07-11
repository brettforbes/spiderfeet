# CLI App Sequencing - Workflow DSL Description

A powerful, generic workflow derived based on the data processing that needs to occur between each step in a CLI Application Sequencing workflow. Since the semantic extent of data output by any single CLI app is far greater than the existing SpiderFeet module, we believe by defining the DSL first on the CLI apps, we can easily retrofit the DSL to control the current SpiderFeet module processing. 

## 1. Aim

The aim is to design a DSL that enables us to define the sequence of inputs, commands, output variables and data saved to context, for any single scanning operation, whether it is a single CLI app, or an API connected through a SpiderFeet module. The SpiderFeet Workflow DSL also sets an interface standard for exchanging data between CLI apps, for example a fixed standard on how lists of values are represented and passed between CLI apps, while the module code performs any specific transforms from the global standard as needed to suit the specific needs of the CLI app. This will ensure the design can suit any new CLI apps as they are onboarded, without having to change the DSL.

## 2. Background to a Single CLI App Workflow Step

Most CLI Applications take in a single nugget value (e.g. DOMAIN_NAME, SUBDOMAIN, IP_ADDRESS, etc.), as a single value or a list of values. Some CLI applications require no input (e.g. network topology discovery, etc.), occaisionally a CLI application will require a pair of nuggets, separated by a delimiter (e.g. IP_ADDRESS:PORT) as a single value or a list of values.

All CLI applications output a semantic subgraph as an arrays of nodes and edges, based on the common SpiderFeet ontology (`.docs\docs-for-cli-tools\_Current_Ontology.md`), and as new CLI apps are onboarded, the ontology in this document will be updated and extended as needed to include the new CLI app's output.

### 2.1 Input File Handling

In order to import a list of inputs in a single command line, some Cli apps require this list to be in a file. Ideally we provide the capability for a user to either specify the file name through the user interface, or have an `auto` mode where the file is created automatically by the module as a consequence of the input data prior to handling the CLI app's input, rather than being specified by the user.

### 2.2 CLI App Command Handling

Each CLI app has a single command line, with a number of options, inputs and outputs specified. The DSL needs a means of entering these and handling the tempaltes for variables to handle the input file and output files.

### 2.3 Output Results Selection and Processing

Every CLI App will output a scan graph, with a scan entity nugget that `had` a number of different descriptor nuggets as properties. 

The scan nugget will also have a `contains` relation to any:

- `HOST` type nuggets (`SYSTEM`, `HOST`, `DEVICE`, `MOBILE` or `CDN`), which will then contain category nuggets (`NETWORKS`, `APPLICATIONS`, `ENVIRONMENT`, `SECURITY` etc.). These category nuggets will then contain any of the data like `IP_ADDRESS`, `PORT`, `SERVICE` etc.
- `DOMAIN_NAME` type nuggets, including `SUBDOMAIN` nuggets.

In these cases, the DSL needs to provide output variables that can be used by  sunsequent worklfow steps, and will use the transitive relation `contains` to traverse the graph for example:

- for each `HOST`, `SYSTEM` or `DEVICE`, we want to extract the `IP_ADDRESS` and any `PORT`s it `contains`, and csetup a list of pairs where they are separated by colons
- for each `DOMAIN_NAME` in the scan graph, we want to extract the `SUBDOMAIN`s it `contains`, and setup a list of subdomains, one of domains and one of all domains

### 2.4 Context Handling

In some workflow steps, we want to copy the scan graph to the context, so that we can build it through multiple scans. Other scans are purely interim steps and we will not want to extract conterxt from them


## 3. Description of Workflow YAML Example

### 3.1 Overview of Example Workflow

We have astarted a sketch of the Workflow YAML Example in `12A_Workflow_YAML_Example.yaml`. This is a simple example of a workflow that has a number of scans in steps:

1. **sfp_subfinder**: Scan all subdomains given a domain name, output a list of subdomains -> context
2. **sfp_nmap**: Scan all ports in each of the domains and subdomains in the list, output a list of IP_ADDRESS:PORT pairs -> context
3. **sfp_nerva**: Scan all pairs of IP_ADDRESS:PORT, for services in every one of the pairs, output a list of services 
4. **sfp_httpx**: Scan all domains and subdomains in the list, output a list of webservers and their status codes 
5. **sfp_katana**: Scan and crawl all or the webservers in the list, output a list of every url found 
6. **sfp_nuclei**: Scan all urls in the list, for vulnerabilities in every one of the urls, output a list of vulnerabilities -> context

So there are two separate sequences of workflow steps:

1. **Map all Ports and Services for each Domain and Subdomain**: Steps 1, 2 and 3
2. **Map all Webservers and Vulnerabilities for each Domain and Subdomain**: Steps 1, 4, 5 and 6

Two of the steps are only interim steps (4 and 5) and we will not want to extract conterxt from them. the other 4 steps are the main steps that we will want to extract context from.


### 3.2 Description of the Common Workflow DSL Structure

We have a sketch of the YAML workflow DSL, except probably the output variables are not properly specified. We really need to change the logic to make it more specific so the logic shown below is reflected in the YAML file `.seed\12A_Workflow_YAML_Example.yaml`. This document is the master inn lgoic, and the YAML file is meant to encapsulate everything described below.

#### 3.2.1 Workflow ID

Every workflow has a unique id, based on a label and a UUID4, so:
```yaml
id: workflow--1c51e712-b5b5-4ef2-9967-e11debbcc607
```

#### 3.2.2 Workflow Info

Every workflow has a unique info block, with the following fields, which are used to describe the modules in the workflow and the start module and targets:

```yaml
info:
  name: Recon Attack Surface
  description: This workflow is used to recon the attack surface of a target.
  author: Modeller
  created: Tuesday, 7th July 2026, 21:58:32
  modules: 
    - sfp_subfinder
    - sfp_nmap
    - sfp_nerva
    - sfp_httpx
    - sfp_katana
    - sfp_nuclei
  start: sfp_subfinder
  targets: 
    - https://example.com
```
So there is a clear place to start the workflow, and a variable that contains an input list of targets to scan, which may be empty if the first scan step runs without a target.

### 3.3 Description of the Subfinder Scan Step Logic

The first step is the `sfp_subfinder` step, and we pretend an `sfp_subfinder` module already exists, and this YAML section defines its interaction with the standard workflow interface:

- **input** it uses a list input, based on the values in the target variable
- **config** the input list is automatically copied to an appropriate input file by the `sfp_subfinder`, and templated in, as is the automated temporary output file, created through the `temp_file` config option
- **output** the output is a series of variables that are used by subsequent workflow steps, and are setup as lists of values, based on the output of the `sfp_subfinder` module. So the scan graph is searched for `DOMAIN_NAME` and `SUBDOMAIN` nuggets that the `SCAN_RECORD` nugget `contains`. These are extracted and setup as named variables, which contain lists of values. These are:
  - **domains**: a list of domain names
  - **subdomains**: a list of subdomains
  - **all_domains**: a list of all domains and subdomains
- **context** this is definitely data we want in the context, so the scan graph is copied to the context, so that it can be built through the consolidation of multiple scans.

### 3.4 Description of the Nmap Scan Step Logic

The next step is the `sfp_nmap` step, and we pretend the existing `sfp_nmap` module already supports this workflow approach, and this YAML section then defines its interaction with the standard workflow interface:

- **input** it registers a list input, the values in the `subdomains` variable
- **config** the input list is automatically copied to an appropriate input file by the `sfp_nmap`, and templated in, as is the automated output XML file, created through the `temp_file` config option
- **output** the output is a single variable, that is based on searching the scan graph for `HOST`, `SYSTEM` or `DEVICE` nuggets that `contains` an `IP_ADDRESS` nugget, and then extracting the `IP_ADDRESS` and any `PORT`s it `contains`. These are extracted and setup as pairs, where for each IP_ADDRESS:PORT pair, the IP_ADDRESS and PORT are extracted, concatenated with a colon separator, and setup as named variables, which contain lists of IP_ADDRESS:PORT pairs. These are:
  - **ip_port_list**: a list of paired IP_ADDRESS:PORT values
- **context** this is definitely data we want in the context, so the scan graph is copied to the context, so that it can be added to previous scan graphs.

### 3.5 Description of the Nerva Scan Step Logic

The next step is the `sfp_nerva` step, and we pretend the existing `sfp_nerva` module already supports this workflow approach, and this YAML section then defines its interaction with the standard workflow interface:

- **input** it registers a list input, the values in the `subdomains` variable
- **config** the input list is automatically copied to an appropriate input file by the `sfp_nmap`, and templated in, as is the automated output XML file, created through the `temp_file` config option
- **output** there are no output values that are used by pother steps
- **context** this is definitely data we want in the context, so the scan graph is copied to the context, so that it can be added to previous scan graphs.

### 3.6 Description pf the Httpx Scan Step Logic

The next step is the `sfp_httpx` step, and we pretend there is an existing `sfp_httpx` module that already supports this workflow approach, and this YAML section then defines its interaction with the standard workflow interface:

- **input** it registers a list input, the values in the `all_domains` list variable from the `sfp_subfinder` step
- **config** the input list is automatically copied to an appropriate input file by the `sfp_httpx` module, and templated in, as is the automated output JSON file, created through the `temp_file` config option
- **output** the output is a single variable `web_url_list`, a list of `URL_WEB_FRAMEWORK` nuggets, where the input domain list has been searched, and reduced only to those urls with a website framework, and the variable is setup as a list of these urls. 

### 3.6 Description pf the Katana Scan Step Logic

The next step is the `sfp_katana` step, and we pretend there is an existing `sfp_katana` module that already supports this workflow approach, and this YAML section then defines its interaction with the standard workflow interface:

- **input** it registers a list input, the values in the `web_url_list` list variable from the `sfp_httpx` step
- **config** the input list is automatically copied to an appropriate input file by the `sfp_katana` module, and templated in, as is the automated output JSON file, created through the `temp_file` config option
- **output** the output is a single variable `internal_url_list`, a list of `LINKED_URL_INTERNAL` nuggets, where the input url list has been searched, and reduced only to those urls that are internal to the target domain, and the variable is setup as a list of these urls. 

### 3.5 Description of the Nuclei Scan Step Logic

The next step is the `sfp_nuclei` step, and we pretend the existing `sfp_nuclei` module already supports this workflow approach, and this YAML section then defines its interaction with the standard workflow interface:

- **input** it registers a list input, the values in the `internal_url_list` list variable from the `sfp_katana` step
- **config** the input list is automatically copied to an appropriate input file by the `sfp_nuclei` module, and templated in, as is the automated output JSON file, created through the `temp_file` config option
- **context** this is definitely data we want in the context, so the scan graph is copied to the context, so that it can be added to previous scan graphs.
