# Improve Scan UI

We need to reorganise how we represent the CLI App Options as controls and text in the Scan UI because there are many, many options and flags per CLI App and the current layout exacerbates this with multiple lines per option.

We need a new layout, one that enables us to show many options as possible in a compact way.

## 1. Reorganise the Current

Currently, the options are presented vertically, and the labels used to represent the fields are written without their dash or double dash. So in an eefort to simplify it, an agent has changed the actual option string. This is fatal and cannot be allowed. Finally, far too much space is pent on each option and the layout is poor

## 2. New Layout

Instead of 3 columns, we will make the portion on the right with the command buttons and the command preview into 2 columns, we can call the command palette. Instead of 9 columns, the options container on the left can have 10 columns, but we want to split that into two columns of 5 columns each, we can call it the cli options palette.

### 2.1 The Command Palette

At the bottom of the Command palette we want to add a `Scan Now` button. This button submits the command line string as selected, and sends it to the CLI App for execution. Later on, when reading through the results, that button will be shown as pressed and unselectable (i.e. read-only).

### 2.2 The CLI Options Palette

A CLI Options Palette is a series of lists of options broken into sections, each section with a section title and a list of options in that section.

#### 2.2.1 A Single CLI Option

Most CLI Options are not mutually exclusive, some are, but we need to handle both cases. If the option is not mutually exclusive then it should be represented by a single check box. Next to the checkbox should be the option string as it appears in the command line string. Then provide a dash and a name of the option,if you mous over the checkbox, a tooltip should appear with the full option description. If they are mutually exclusive, do the same but with radio buttons

Many CLI options require the entering of a value, string, int, bool, list etc. If the option requires a value, then selecting the check box or radio buttoin opens an input box to the right of the CLI option string.

#### 2.2.2 A Single CLI Option Section

When there is a CLI options section it will have options that ere either mutually exclusive or not. Place a heading in the column and then line up the options underneath it to complete a section.


#### 2.2.3 2 vc 3 columns

At present it is not clear wihther we shoulduse two columns only for the otions or whether we can use 3 columns. Work out the total number of options in each section and try to make the columns as equal as possible.

## 3. Pull key Contetn from the API

Finally, recall that rather than store all of the CLI App UI's we want to dynamically produce them based on the options document for each tool. The options document is a JSON object that contains the options for the tool. It is stored in the `./tools/` directory and is named after the tool. The file is named after the tool and has the extension `.json`. The file contains the options for the tool. The API should serve the document so the UI can be defined dynamically.

We need to pull the key content from the FastAPI and use it to populate the CLI Options Palette.