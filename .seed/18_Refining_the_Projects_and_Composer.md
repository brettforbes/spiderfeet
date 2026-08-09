# Refining the Projects and Composer

There is far too much vertical padding in the user interface at the moment and we need to reduce it, so the content is more closely aligned with the edges of the screen.

Firstly, we want to make the current Navbar on the top, only show for a limited time, before sliding into the top of the window. Going close to the top of the screen makes the Navbar slide back down. This makes the entire ui much larger for every page in the navbar, but one can still call it down when needed to switch pages.

## 1. Refining the Projects Page

What is meant to show on the Projects page? -> A table of projects, with each row representing a project and the columns representing the project details. The project details must correspopnd with the `project` relation in the spiderfeet_v2_semantic.tql file.
Now when i double-click on a row in the Projects table, i want to open that project in the Composer page, so the YAML DSL is loaded into the composer and the user can edit it and run it. The YAML DSL is stored in the `project` relation as the `project_yaml` attribute, and there should be fastapi routes already setup to get a project, a workflow, a step, and a complete project record in json, everything needed for the user interface to work.


```typeql
define
	relation project,
		owns project_id @key, # e.g. "project--1c51e712-b5b5-4ef2-9967-e11debbcc607"
		owns stix_incident_id @card(0..1), # e.g. "incident--1c51e712-b5b5-4ef2-9967-e11debbcc607"
		owns project_name, # name of the project, e.g. "Project 1"
		owns project_description, # description of the project, e.g. "A project to scan the target domain"
		owns project_created, # datetime project was created
		relates workflow @card(0..),
		plays project_context:project, # contains actual nodes and edges arrays for the context for the project
		plays temporary_subgraph:project; # contains actual nodes and edges arrays as the temporary subgraph for the project

```

### 1.1. Fixing the New Project Modal

These same details must be requested in the modal for creating a new project if the New Project button is pressed. Currently it only has the stix incident id field, does not include the name, description or created time of the project. The project id with the UUIDv4 should be dynamically generated and shown on the modal as read only, same as created time

When a user fills in these details and clicks the Create Project button, the project should be created in the TypeDB database and the user should be redirected to the Composer page with this data loaded into the composer.

### 1.2. Fixing the Error Message

At the moment, the messages on the project screen are an error red, saying
Could not load projects.
NetworkError when attempting to fetch resource.
Load failed: NetworkError when attempting to fetch resource.

### 1.3. Initialising the Project Table with 5 real projects, that have not been run yet

We want to create seed projects, around real examples, based on using the two seed YAML DSL workflow descriptions that already exist, the [simple -> no input wireless scan](.seed\12A2_Workflow_YAML_Example.yaml), and the [complex -> twin fork attack surface recon workflow based on an input of example.com](.seed\12A_Workflow_YAML_Example.yaml) as templates.

A table defining the four seed projects and their data. MAke sure you set up the project id, project name, project description and project created time for each project, ignore the stix incident id for now. The first project is a simple local are scan, the rest are just clones of the multi-pronged attack surface scanning workflow (i.e. the input variable changes). All of the pojects should be fully setup in the spiderfeet-actual TypeDB database, but their YAML DSL has not yet been run, so the project has a setup workflow, but nothing has been scanned or run yet. All we need is the YAML DSL to be stored in the project, but not yet run. Then we can run it later and check for errors, for the moment lets just get everything setup correctly and then we can run the workflows later, so being able to reuse these two workflows to make multiple useful examples is really useful.

A table describing how to make the 4 seed projects, based on the two seed YAML DSL workflow descriptions.

| Project | Input | Template | Project Name | Project Description |
|---------|-------|----------|--------------|---------------------|
| 1 | None | 12A2_Workflow_YAML_Example.yaml | Simple Wireless Scan | A simple wireless scan of the target domain |
| 2 | www.sbs.com.au | 12A_Workflow_YAML_Example.yaml | Complex Twin Fork Attack Surface Recon | A complex twin fork attack surface recon of the target domain |
| 3 | www.k2am.com.au | 12A_Workflow_YAML_Example.yaml | Complex Twin Fork Attack Surface Recon | A complex twin fork attack surface recon of the target domain |
| 4 | www.venturecapitalopportunitiesfund.com.au | 12A_Workflow_YAML_Example.yaml | Complex Twin Fork Attack Surface Recon | A complex twin fork attack surface recon of the target domain |
| 5 | www.squarepeg.vc | 12A_Workflow_YAML_Example.yaml | Complex Twin Fork Attack Surface Recon | A complex twin fork attack surface recon of the target domain |


## 2. Refining the Composer Page

The Composer page is largely good, and the only issues fall into two categories:

1. Small refinements to the surrounding SpiderFeet iFrame and the CSS styles
2. Significant changes to the way the YAML DSL Workflow Editor embeds inside the Composer page on the host iFrame, so that it integrates better with the host iFrame when it is at Partial Width.

### 2.1 Refining the surrounding SpiderFeet iFrame and CSS styles

When the Composer Page is selected, without a Project being selected the current layout is pretty good, although i have not yet tested it with project data loaded. The small refinements are:

#### 2.1.1. Creating a drop down to select the Project to load into the Composer page.

At the very top of the page, where the words `Composer No project selected` are on the left hand side, and the Run Workflow button is on the right hand side, we want to add a drop down to select the Project to load into the Composer page. In the dropdown list, at its top place a checkbox item to add a new project. If the add new project checkbox is checked,, then bring up the new project modal from the Projects page, and allow the user to create a new project. If the add new project checkbox is not checked, then the dropdown list should be populated with the list of projects that are already in the database. When a project is selected from the dropdown list, the project data should be loaded into the Composer page.

#### 2.1.2. Adding some new icon buttons to the Workflow Bar at the top of the container holding the YAML DSL Workflow iFrame

In the Workflow Title Bar, right above where the YAML DSL Workflow Editor is embedded, we want to add some new icon buttons to the Workflow Bar. These buttons will be used to control the YAML DSL Workflow Editor. The buttons will be:

- a pencil icon to shift the YAML DSL Workflow Editor to edit mode, and it turns into a pair of spectacles icon to shift the YAML DSL Workflow Editor to read only mode.
- a gear icon to open the settings menu for the YAML DSL Workflow Editor.

### 2.2 Refining the YAML DSL Workflow iFrame

The fundamental YAML DSL Workflow iFrame is working well, but we need to refine it to be more responsive and to integrate better with the host iFrame when it is at Partial Width. Perhaps make the github tickets in its direct repo, although you also have access to the repo as it is open in cursor `C:\projects\yaml-workflow-widget`

#### 2.2.1. Remove the CLI Workflow DAG Title bar completely, and instead use the buttons from the Workflow Bar in the host iFrame to trigger  the necessary actions.

Completely remove the CLI Workflow DAG Title bar completely, and instead:

1. When the user clicks the Pencil icon in the Workflow Bar, the YAML DSL Workflow iFrame should be switched to edit mode, and change to a Spec.
2. When the user clicks the Spectacles icon in the Workflow Bar, the YAML DSL Workflow iFrame should be switched back to read only mode.
3. When the user clicks the Gear icon in the Workflow Bar, the YAML DSL Workflow iFrame current settings modal should be opened. We need to add some more options to the settings modal, which currently only switches between coloured lines or black only lines. We need to add the option to show/hide the viz legend

When the viz is in Edit mode, there are already buttons on the canvas to enable a new workflow to be built, so nothing needs to change there.

Regardless of whether it is in embed mode or not, the iFrame should not show the "CLI Workflow DAG" title bar in the target iFrame.

#### 2.2.2. Change the Zoom and Pan controls

Change the Zoom Controls from the mouse wheel to `CTRL +` or `CTRL -` to zoom in and out.

Change the Mouse Wheel so it pans the canvas up and down using the scorllbar on the far right hand side of the canvas.

By pressing and dragging the mouse, the canvas should pan left and right

#### 2.2.3. Always Know the Dimensions/Location of the DAG Workflow Viz

In the iFrame you need to always keep track of the:

- vertical centre line of the DAG Workflow Viz
- full left wdith from centre line to the left edge of the visualisation (shapes, text, etc)
- full right width from centre line to the right edge of the visualisation (shapes, text, etc)
- top and bottom of the DAG Workflow Viz

If you always know the size, locations and centre line of the DAG Workflow, based on a 100% zoom ratio, then you can always calculate how to show it in the host iFrame, regardless of the width/height of the host iFrame.

#### 2.2.4. Instant Calculation on How to Show the DAG Workflow Viz in the Host iFrame

Based on the width of the host iFrame, and the dimensions/location of the DAG Workflow Viz, you can instantly calculate how to show the DAG Workflow Viz in the host iFrame.

Rule 1: Start with a zoom of 50%, show the DAG Workflow Viz at the centre of the host iFrame, with the Start shape at the top of the screen. then  a user can scroll down to see more of the diagram

Rule 2: If the DAG Workflow Viz is to wide for the host iFrame, then zoom out further until the left edge of the DAG Workflow Viz is 5px in from the left edge of the host iFrame, and the right edge of the DAG Workflow Viz is 5px in from the right edge of the host iFrame.

Rule 3: Enable the User to use CTRL + and CTRL - to zoom in and out, but provide an option to reset back to default view of rule 1/2 above.

#### 2.2.5. Embed mode removes current overlays, that it tries to ue to reduce the viewing port, instead we focus on displaying well in the host iFrame, with the DAG Workflow Viz at the centre of the canvas, and the Start shape at the top of the screen, and the width scaled to the width of the host iFrame

If I put the CLI Workflow DAG iFrame in Embed mode, as can be seen currently at this address `http://localhost:4009/?embed=1` then one can see the folloing errors in the layout:

1. There is an overlay from the right edge covering approxiamtely the right 1/3rd of the canvas. this partially obscures the existing viz diagram, why?
2. The vertical scrollbar is at the left hand edge of the above covering, and the scrollbar partially obscures the actual visualisation image, why?
3. The legend occurs to the left hand edge of this right third overlying covering, why?
4. there is an overlying covering from the left edge covering the left 1/3rd why?
5. Viewing this from the host iFrame means that one can never see the entire diagram, it is always cut off on the left and right edges, and the top and bottom edges are not visible, why?

Get rid of these ideas and use the functions and rules above to make sure the viz displays well when you are on the Partial width setting in the host iFrame.

