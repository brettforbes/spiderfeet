# Spiderfeet v2 - Integrating TypeDB FastAPI iFrame

## 1. Background

### 1.1. The old version of the Spiderfeet engine

The old version of the Spiderfeet engine in the `spiderfeet` directory was built based on the idea of having Events that were listened to or produced by the various modules in the `modules` directory (e.g. `modules\sfp_abstractapi.py`), where each module represented a service. The semantic limit of throttling down the feedback to a single type of data in an atomic form (e.g. the Event) is that it cannot suit all situations, since some will require more complex semantic descriptions than simply a single Event name and then one has to concatenate names, which collapses meaning (e.g. `AFFILIATE_DOMAIN_UNREGISTERED`, `AFFILIATE_INTERNET_NAME_UNRESOLVED` etc.), so it becomes hard to add to other data.

Further it means that when interacting with sophisticated data sources, like CLI Apps, the old version of the Spiderfeet engine throttled down the output to just one or two of the most important Event names, which is not enough to capture the full context of the data.


### 1.2. Exploration of a New Workflow for Services that Produce Semantic Subgraphs

We explored and examined a variety of scenarios for 8 different CLI Apps, and developed significant temporary softwareinfrastructure to explore what was involved in implementing the v2 of the Spiderfeet engine, including:

- centralised machinery for converting structured data forms (i.e. xml, json etc.) from scans to be [converted into a subgraph](.seed\scripts\cli_corpus\core\rule_engine.py) from a common ontology and centralised machinery for [converting the semantic graph into a narrative report](.seed\scripts\cli_corpus\core\narrative_engine.py)
- per CLI App infrastructrure to run the scan and produce the four output forms, leveraging the common machinery where possible to convert into the four output forms
- a simple CLI App User Interface that includes five tabs, the scan tab that shows the scan settings, and then tabs for the four output forms, the text form, the structured form, the semantic graph form, and the narrative report form
- Semantic Graph Ontology comprised by adding together the current 8 Graph proposed Nugget Graph Structure Documents (`Nmap — proposed nugget graph structure`, `Netdiscover — proposed nugget graph structure`, `Nerva — proposed nugget graph structure`, `Nuclei — proposed nugget graph structure`, `Pius — proposed nugget graph structure`, `Subfinder — proposed nugget graph structure`, `httpx — proposed nugget graph structure`, and `Katana — proposed nugget graph structure`)
- a YAML DSL workflow model, based on a [Split Branch WorkflowExample](.seed\12A_Workflow_YAML_Example.yaml), a [DSL Description](.seed\12B_Workflow_DSL_Description.md) and a [Graph Selection Language](.seed\12C_Graph_Selection_Language.md) for defining the scanning steps and the output forms, and the ability to chain steps together
- a [separate repo](C:\projects\yaml-workflow-widget) that enables [embedding](.seed\YAML_Workflow_EMBED_GUIDE.md) of a YAML Workflow Editor including an iFrame (`http://localhost:4009/`) that takes the YAML in as grammar and produces a valid workflow diagram top act as a workflow-overview schematic

In short, we have many of the capabilities needed for a v2 SpiderFeet, and are ready to start building the v2 of the Spiderfeet engine.


## 2. Aim

The simple proposition of the v2 of the Spiderfeet engine is that one wants a user interface and engine that can:

1. take in a list of nuggets of data (e.g. target) and produce 4 types of results from a scan: Text Form, Structured Form, Semantic Graph Form, and Narrative Report Form, based on an underlying common ontology.
2. have a workflow of one or more scanning steps, including creating output variables from the semantic graph output, and chaining steps together.
3. have the ability to combine together the semantic subgraphs of multiple services into a single semantic graph, with the ability to query the combined semantic graph for specific nuggets of data.


Specifically, we need to:

- create v2 modules for each of the 8 CLI Apps in the `modules_v2` directory. All CLI App code needs to be in that directory, and/or subdirectories. Assume we will be deleting where ever the current code is located, so everything for the modules, including the common code, needs to be in the `modules_v2` directory. Everything module-specific needed to run the CLI App, and produce the 4 output forms, needs to be in the module file and directory.
- create a new engine in `spiderfeet_v2` directory that uses the new modules and the updated `.seed\spiderfeet_v2_semantic.tql` TypeDB schema in a new `spiderfeet-actual` database.
- make the new engine based on FastAPI
- update the iFrame to connect to the new engine and add two new pages, the Composer page and the Enrichments page (Note we are going to change the name of the "Enrichments" page to "Projects")

You will need to use the [TypeDB skill](.cursor\skills\typedb\SKILL.md) and the [Python type-bridge skill](.cursor\skills\typedb-bridge\SKILL.md) to create the new engine and modules.

## 3. Semantic Graph Ontology

The [original nuggets](.docs\analysis\nuggets.json) produced by the existing machinery and modules, were found to be limiting and to have errors (e.g. no independent `PORT` nugget, collapsed meanings etc.). So we developed [a completely new set of nuggets capable of containing the full semantic output of all 8 CLI Apps](.docs\analysis\nuggets_extension.json), derived from the results of each CLI App.

There is a considerable, subtle hierarchy within the nugget structure that only becomes obvious when you look through the structure of the `.seed\spiderfeet_v2_semantic.tql` TypeDB schema.

### 3.1 Rules on Nuggets

All of the rules for nuggets described in `.seed\05_Onotology_for_Nuggets.md` apply to the v2 of the Spiderfeet engine.

### 3.2 The Meta-Concept Key Rules

In order to add subgraphs together, we need some rules create a consistent structure. The most important rules are:

1. Some concepts`contains`other concepts, and how this can be used to create a directed, acyclic, transitive hierarchical structure of concepts that is consistent regardless of how sparse or dense the data is (i.e. if `A |contains|-> B |contains|-> C`, then `A |contains|-> C`).
2. Some key concepts, known as `meta-concepts`, are used to group together the data and behaviour other nuggets describe (e.g. person, host, CDN, mobile, device, trace, etc.). An issue is the unambiguous selection of the unique value the agent likes to use as a key for this concept. At the moment the key value for a host is its IP address
3. Scan results by themselves are insufficient, and that `meta-concepts` will need to `contains` a number of `category` concepts, such as `networks`, `environment`, `applications`, etc. These do not hold data values that are useful as grouping the nuggets that contain the actual data for that type of `meta-concept` (i.e. `category`  are different between the different types of `meta-concept`), but have the useful nuggets contained within their category.
4. Any `ENTITY` may have zero or more `DESCRIPTOR`s, attached by `had` relations (`has` is a reserved word in TypeQL) and these are used to describe the `ENTITY` in more detail.
5. Every scan is focused on one or more `meta-concepts`,
6. The aim is to limit the number of other edge types, at present there is only `listens-to` and `had` relations.

### 3.2 The Transitive Hierarchy of Containment

Normally, we would need to use a NetworkX function to find all of the weakly-connected components of a `meta-concept` subgraph, but we can use the power of TypeDB to query out the subgraphs using the `contains_recursive` function.

For example, to find all of the nuggets that are contained within a `HOST` nugget's subgraph, we can use the following TypeQL query on any scan result graph, with the `meta-concept` parent entity, and extract all of the contained nuggets and edges through the `contains_recursive` function:

```typeql
fun contains_recursive($container_A: node) -> { node }:
match
  { # base-case
     $_ isa contains, 
       links (container: $container_A, contained: $contained_C);
  } or { # recursive-case
    let $intermediate_B in contains_recursive($container_A);
    $_ isa contains, 
      links (container: $intermediate_B, contained: $contained_C);
  };
return { $contained_C };
```
This function can be modified to also return the `had` and `listens-to` edges within the subgraph of the `meta-concept` parent entity.

### 3.3 Storing a Scan and its Subgraph

When a scan is run, it includes:

- a scan string
- a Text form,
- a Structured form,
- a Semantic Graph Form, which is an array of nuggets and an array of edges,
- a Narrative Report Form, which is a string of markdown text,

Semantic Subgraphs are stored in the database in two forms:

1. **json-string** format, which is a string of JSON that contains the nuggets and edges in a single attribute,
2. **In-Graph** format, which is a set of TypeDB entities and relations that represent the subgraph, as shown below.

```typeql
define
...

	relation subgraph @abstract,
		relates nuggets @card(0..), # array of nugget entities
		relates edges @card(0..), # array of edge relations
		relates owner @card(0..1), # entity that owns the subgraph

	relation scan_result_graph, sub subgraph,
		owns scan_result_id @key, # e.g. "scan-result--0b778a9a-ae9c-4253-883d-32208b75d441"
		relates scan_step as owner;

	relation project_context, sub subgraph,
		owns project_context_id @key, # e.g. "project-context--0b778a9a-ae9c-4253-883d-32208b75d441"
		relates project as owner;

	relation temporary_subgraph, sub subgraph,
		owns temporary_subgraph_id @key, # e.g. "temporary-subgraph--0b778a9a-ae9c-4253-883d-32208b75d441"
		relates project as owner;
```

## 4. Scan Records

When a scan is made, we want to store a scan-record, like was used in the original spiderfeet engine, but also include the details of the workflow step that was run to produce the scan-record.

As can be shown in the `scan-step` shown below, it includes:

- the attributes from the original scan-record, plus 
- the 5 strings which enable the iFrame to display the scan-record in the UI
- a copy of the instance nuggets that were consumeed, as well as the subgraph that was produced by the step
- a reference to the workflow that was run to produce the scan
- a reference to the service that was used to produce the scan
- at the moment routes are not implemented, so we will not include a reference to the route for the future.

```typeql

	relation scan_step, # the record generated as a result of a single scan instance, including ui data and scan results
		owns scan_instance_id @key, # e.g. "scan_step--1c51e712-b5b5-4ef2-9967-e11debbcc607"
		owns step_module_id, # name of the step's module, e.g. "sfp_cli_subfinder" (avoid bare attribute label `id`)
		owns scan_status, # success, error, etc.
		owns scan_nugget_count, # number of nuggets generated by this scan instance,
		owns scan_results_by_type, # object map event_type → count (e.g. IP_ADDRESS: 2)
		owns scan_results, # bundled summary object { status, nugget_count, by_type }
		owns scan_duration, # time scan took to complete
		owns scan_timestamp, # time scan started (API / UI parity)
		owns scan_notes,
		owns scan_ui_cli_command, # the command run to execute the scan step, e.g. "subfinder -d example.com -o json"
		owns scan_ui_text_form, # text description of the scan step,
		owns scan_ui_structured_form, # structured form of the scan step as a string, e.g. { json, csv, xml, etc. }
		owns scan_ui_structured_form_type, # type of the structured form, e.g. "json", "csv", "xml", etc.
		owns scan_ui_graph_form, # json string form of the nodes and edges arrays of the semantic scan subgraph
		owns scan_ui_markdown_narrative_form, # markdown string form of the narrative description of the scan step
		owns scan_yaml, # description in yaml workflow DSL, e.g. "subfinder_enum"
		plays workflow:prior_step, # step can be a prior step in a sequence of steps
		plays workflow:first_step, # step can be the first step in a sequence of steps
		plays workflow:next_step, # step can be a next step in a sequence of steps
		relates consumed @card(0..), # nugget inputs consumed by this scan step
		plays scan_result_graph:scan_step,  # contains actual nodes and edges arrays for the scan result
		relates service, # native osint-service: module_id, name (e.g. sfp_cli_nmap)
		relates route @card(0..1); # route under test when this step ran
```

So in short, each scan step captures a similar record to the old engine, plus all of the data for the user interface to display scan results, as well as details of its particular scan step and connection to the workflow and service that produced it. 

Finally, the actual data nuggets used as input and the semantic nuggets and edges produced are also stored Everything produced through the scan step, and shown on the ui is stored on this single relation. It seems pretty clear that this entiore structre could easily be converted to/from a json object and used for the user interface to display the scan results, and the scan step details, and the workflow and target details.

## 5. Workflow

You will see that the workflow steps from above and the workflow and target details below, are an identical shadow of the YAML Workflow DSL described in [12B_Workflow_DSL_Description.md](.seed\12B_Workflow_DSL_Description.md), but in TypeDB entities and relations. So, once a YAML DSL workflow is exchanged between the FastAPI server and the YAML Workflow Editor iFrame described above, it can be converted between the two formats and created, retrieved, updated or deleted in the TypeDB database as required

```typeql
define
...
	relation workflow,
		owns workflow_id @key, # e.g. "workflow--1c51e712-b5b5-4ef2-9967-e11debbcc607"
		owns name, # name of the workflow, e.g. "recon_attack_surface"
		owns description, # description of the workflow, e.g. "Enumerate domains, map ports/services, and map live web surface + vulns. Ports/services chain and web/vuln chain share sfp_cli_subfinder, then fan out."
		owns author, # author of the workflow, e.g. "Modeller"
		owns created, # time workflow was created
		owns workflow_yaml, # string description in yaml workflow DSL, to feed to the workflow iFrame widget
		relates first_step,
		relates prior_step,
		relates next_step,
		relates target,
		plays project:workflow;

	entity target,
		owns target_id @key, # e.g. "target--1c51e712-b5b5-4ef2-9967-e11debbcc607"
		owns target_value, # value of the target, e.g. "example.com"
		owns target_description, # description of the target, e.g. "The target domain to scan"
		owns target_created, # time target was created
		owns target_yaml, # string description in yaml target DSL, to feed to the target iFrame widget
		plays target_context:target;
```

It seems pretty clear that this entire structure could easily be converted to/from a json object and used for the user interface to edit/display the workflow YAML DSL. It is useful for typeDB to maintain both native and string versions of the same data, in order to provide advantage for both the user interface, and enable reasoning over content in the knowledge graph (i.e. using function `fun` driven queries to not only extract data for the user interface, but also be able to deduce new values from the data in the knowledge graph)

## 6. Projects

Finally, the concept of a Project then includes one or more workflows, that collect subgraphs nodes and edges arrays into a temporary context, from where they are then added together to create the final project context using a rule system to combine the subgraphs together.

```typeql
define
...
	relation project,
		owns project_id @key, # e.g. "project--1c51e712-b5b5-4ef2-9967-e11debbcc607"
		owns stix_incident_id @card(0..1), # e.g. "incident--1c51e712-b5b5-4ef2-9967-e11debbcc607"
		owns created,
		relates workflow @card(0..),
		plays project_context:project, # contains actual nodes and edges arrays for the context for the project
		plays temporary_subgraph:project; # contains actual nodes and edges arrays as the temporary subgraph for the project
```

It seems pretty clear that this entire structure could easily be converted to/from a json object and used for the user interface to edit/display the project details, including the workflows, targets, and the temporary subgraph.

Further, it is obvious that one can query for a project, say through a function `fun` driven query, to extract the project details, including the workflows, targets, and the project context/temporary subgraphs. It is also obvious that one can query for a workflow, say through a function `fun` driven query, to extract the workflow details, including the first step, prior step, next step, and the target.

## 7. The Projects Page Replacing the Enrichments Page

Currently, in the mena bar, there is an "Enrichments" page, which is a placeholder for the new "Projects" page. The new "Projects" page will be a page that allows the user to create, edit, and delete projects, and to view a table of the projects and their details.

By clicking on a row in the Projects table, the full Project json is pulled and the user is sent to the Composer page, described below, where the user can edit the project details, including the workflows, targets, and the temporary and project context subgraphs.

## 8. The Composer Page

The Composer page is comprised of four visual elements. The central pane is split horizontally into two panes and comprises the first two of the four visual elements:

1. The Project Context Viewer, which is a visual viewer for the project context subgraph, and is the upper half of the spilt central pane in the Composer page. This element will be left without content in this project and will be the subject of a future project, so for the moment model it as an empty set of nodes and edges. Both upper pane and lower panes will include an icon on the top right of each pane to expand to full screen for that pane, and an icon so once you are full screen you can revert back to the original size. Both upper and lower pane use the Canvas force graph visualiser developed for the Graph tab in the Simple CLI App Profiling user interface.
2. The Temporary Subgraph Viewer, which is a visual viewer for the temporary subgraph, and is the lower half of the spilt pane in the Composer pane. The behaviour of this element will be fleshed out below. Both upper pane and lower panes will include an icon on the top right of the pane to expand to full screen for that pane, and an icon so once you are full screen you can revert back to the original size.
3. The YAML DSL Workflow Editor, which is a visual editor for the YAML DSL workflow, and slides in from the left on demand either partially to show only the workflow viz, or full screen to show the YAML DSL code windows as well as the workflow viz. The default position of the Workflow editor is for the pane to be partially open to show only the workflow viz. From there, the user is able to click on an icon to collapse it, or click on the icon to expand it to full screen.
4. Simple CLI App Visualiser, which is the simple visualiser component used in the CLI APP Profiling user interface once you press a scan scenario in the table. The simple CLI APP Visualiser Component has 5 tabs ("scan", "text", "structured", "graph", "narrative"), and enables a user to define and start a scan and review the results, or review the results of a scan previously done in a read-only mode. The behaviour of this component will be detailed out below.

### 8.1 Behaviour of the Temporary Subgraph Viewer

When a scan step is processed by the SpiderFeet v2 engine, a semantic graph of the scan is produced. Every workflow step has a context attribute that can be set to `scan_graph` to export the semantic graph of the scan, or `none` to not export the semantic graph of the scan.

```yaml
    context:
      export: scan_graph
```

If the context attribute is set to `scan_graph`, then the semantic graph of the scan is exported and sent to the Temporary Subgraph Viewer. Now since multiple scans will be taken through the workflow many of these scan grapsh will have overlapping id's, so we need a special setup in the Temporary Subgraph Viewer to handle this.

Every time a scan graph is imported into the nodes and edges array that is displayed in the Temporary Subgraph Viewer, we need to add a new `temporary_id` to the nodes that are imported and then map the edges to the new nodes. To do this, we need to:

1. Add a new `temporary_id` to each node that is imported, based on `temporary--<UUIDv4>`, using the common method used for other id's in the TypeDB schema.
2. Map the edges to the new nodes using the `temporary_id`
3. Append the new nodes and edges onto the nodes and edges arrays of the Temporary Subgraph Viewer, and then display the resultant nodes and edges as a series of discrete subgraphs on the force graph canvas.
4. Provide a toggle to Remove 

Make it so that when the temporary graph is sent to the FastAPI server, the temporary id's are removed and the edges arrays are mapped back to the original `nugget_instance_id` values. Only when it is brought into the Temporary subgraph Viewer are the temporary id's added on so each subgraph is essentially independent of the other subgraphs.

### 8.2 Behaviour of the YAML DSL Workflow Editor

The YAML DSL Worflow Editor, is another repo open in Cursor (`C:\projects\yaml-workflow-widget`), so the agent can access it and make changes to it. It is available on `http://localhost:4009/`, and the embedding guide is here `.seed\YAML_Workflow_EMBED_GUIDE.md`. 

The YAML DSL Worflow Editor has different modes of operation, either showing both YAML code window and the workflow viz, or just the workflow viz. The default mode is to show just the workflow viz. The workflow viz has an Edit mode, which allows the user to edit the workflow YAML code, and a View mode, which allows the user to view the workflow YAML code. The default mode is to show the workflow in View mode. 

This iFrame is meant to be embedded and messages are sent between the the surrounding iFrame (`C:\projects\spiderfeet-widget`) and the YAML DSL Workflow Editor iFrame. So that behaviour between the two can be coordinated.

In the host iFrame Composer page, we want to have a collpsing container, to the left of the horizontally split panes, which then embeds the YAML DSL Workflow Editor iFrame. The container and iFrame should be initially partially collapsed to show only the workflow viz (i.e. 3-columns wide), and from there the user is able to click on an icon to fully collapse it onto the left hand border of the Composer page (i.e. 0-columns wide), or click on the icon to expand it to full screen (i.e. 12-columns wide).

We note that both iFrames need to synchronise on light/dark theme, so that the user experience is consistent.

Further, we want a message sent from the YAML DSL Worflow diagram to the surrounding iFrame (`C:\projects\spiderfeet-widget`) that when a workflow step is selected in the workflow viz, the corresponding Simple CLI App 5-tab UI slides in from the right edge of the Composer page, so it covers columns 4-12.

If the scan step has not been run yet, then only the scan tab is able to be accessed, with its scan now button disabled, but the rest of the CLI App option controls enabled. This enables the user to select the CLI App options in the Simple CLI App UI. When the user makes changes in that Simple CLI App UI, the changes are sent to the YAML DSL Workflow Editor iFrame, so that the workflow YAML code, and resulting workflow viz is updated to reflect the changes in the scan options.

The user needs to have selected valid options in the Input, Config, Output and Context sub tasks of the workflow step before that scan step can be run. Once thos options are set in the YAML DSL Workflow Editor iFrame, then the Scan Now button should be enabled on the Simple CLI App UI.

### 8.3 Behaviour of the Simple CLI App Visualiser

The simple CLI App Visualiser acts like described above, there is a viewer for every CLI App and API onboarded into the Spiderfeet v2 engine, and the correct CLI App viewer is displayed in the Simple CLI App Visualiser when a workflow step is selected in the workflow viz.

When the scan has not been run, then the scan now button is not enabled unless each of the 4 sub tasks in any workflow step have been completed correctly (ie. the Langium Grammar is correctly validated and the YAML DSL Workflow Editor iFrame is able to generate a valid workflow YAML code for that workflow step). At that point a message should be sent to the surrounding API to enable the Scan now button on the simple cli app ui.

Once the scan has been run and the results produced, then the four forms of results, text, structured, graph and narrative are displayed in tabs in the Simple CLI App UI. These results are displayed in the Simple CLI App UI, and are also stored in the TypeDB database as part of the scan step record.

## 9. The 4 Example Targets used to Develop the Engine and Capabilities

The aim is to transfer all of the existing code from the CLI App Profiling engine, used to run a scan, produce the outputs, and convert the structured from into graph from, and from there into narrative form. All of that functionality needs to be then transferred into the new Spiderfeet v2 engine directory (`spiderfeet_v2`), and 8 new modules for the CLI Apps (e.g. `modules_v2\sfp_cli_nmap.py`, `modules_v2\sfp_cli_subfinder.py`, etc.).

While modelling everything on the original spiderfeet engine, we need some changes to support the new semantic subgraph structure, and the new scan step record structure.

As described above are that we want to synchronise the development of a series of things, so that all of these new structures and components can coherently work together:

- the 8 new modules for the 8 CLI Apps, following  the pattern of the existing stub `modules_v2\sfp_cli_nmap.py`. Place all of the other modules specific or common code in subdirectories of the `modules_v2` directory. It is the module that is responsible for creating the four forms of output from the scan results. So converting the structured form into graph form, and from there into narrative form, using as much centralised code as possible in the `.modules_v2` directory.
- the Spiderfeet v2 semantic schema, loaded into TypeDB as `spiderfeet-actual` database, intiailised with the 8 new sfp_cli_services in the `modules_v2` directory.
- the function `fun` that you write in TypeQL to enable projects, workflows, steps, subgraphs, project and temporary contexts to be easily quried and extracted in JSON form
- the engine that runs the workflow and calls the 8 new sfp_cli_services to run the scan, it is 
- the FastAPI server, with its routes and endpoints, that are used to create, retrieve, update and delete the projects, workflows, steps, subgraphs, project and temporary contexts in the TypeDB database, in the `spiderfeet_v2` directory.
- the SpiderFeet Widget, which is the parent iFrame that contains the other iFrames, and is used to navigate between the different pages and components.
- the YAML DSL Workflow Editor, which is the iFrame that contains the YAML DSL Workflow Editor, and is used to edit the YAML DSL workflow

In order to develop all of the above in a sybcghronised way, we need 4 simple examples of workflows to run live scans and check all of the capabilities. So the plan is to run the existing [YAML Workflow DSL](.seed\12A_Workflow_YAML_Example.yaml) on 4 different targets instead of "example.com", but keeping the same workflow steps and structure:

- https://www.sbs.com.au
- https://www.k2am.com.au/
- https://www.venturecapitalopportunitiesfund.com.au
- https://www.squarepeg.vc/


The above run and check process is part of the entire project, because we want to build a tightly integrated kernal of capability described above that can then be elaborated on in future projects.