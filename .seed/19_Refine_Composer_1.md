# Refine Composer 

## 1. Issues with Nerva Scan Step, possible problem in Graph Select Launguage

### 1.1 Background

The biggest potential weakness in the workflow model - scan step model is the process of defining output variable, because of the complexity of the job. Every scan produces a scan graph, and defining the output variables means selecting values from the scan graph, and sometimes post-processing them (e.g.concatenation, or regex matching), before combining them into a list before making them available for future scan steps to use as inputs

As previously defined each Scan Step has four components, an Input,the Config, definition of Output variables and the whether to export a semantic subgraph to temporary context. The real question is whether the current [Graph Select Language](.seed\12C_Graph_Select_Language.md) is sufficient to collect the output variables from the scan step, although admittedly we only have a small set of examples.

Now consider that we have meta-concepts like Hosts, Systems, Conpany's, People etc. that `contain` other entities, subentities, and sometimes meta-concepts themselves. This means that the output variables of a scan step can be a list of entities, subentities, or meta-concepts, and we need to be able to select specific items out of this scan graph, collect them in a list, publish them using a variable name and use them as inputs in future workflow steps.

Once an output variable has been defined for the scan step, with this Graph Selection Language, then there are two ways to use the GSL to obtain those results, either convert it in a TypeQL query and try to select and export the right data items, or use it in logic to look directly through the nodes and edges array to collect the items that are to be assigned to the output variable.

Up to you how this exchange between the description in the YAML Workflow DSL for an output variable, which uses the Graph Selection Language, is used to retrieve the actual data items from the scan graph. If you want to use the TypeQL query approach, then you can use the TypeDB skill `.cursor\skills\typedb\SKILL.md` and consider the recursive containment query below.

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

If instead the covnersion between Graph Selection Language and retrieving the data items is currently done through code logic, then you can continue to use this, as long as the GSL addequately describes the selections and transformations required, how you extract data items is now up to you.

### 1.2 Does the GSL Map All of the Requirements?

Now lets consider the current workflow, you can see that some steps work, but Nerva fails to find anything, and Nuclei throws an error. The big question is whether the data the steps are receiving as input is correct, and if not, why not. Is it because the descriptio in the Output variable is insufficient??

Lets consider the data flow from the target on through each step, considering specifically the output variables and the input requirements of various steps

| Input Requirements | Step | Output Variable Requirements |
|--------------------|------|-----------------------------|
| Domain Names from User | Target | List of Domain Names (`default=1`) |
| List of Domain Names | SubFinder | List of Subdomains + Domain Names |  # must include the list from the input and the output together here
| List of Subdomains + Domain Names | NMAP | List of IPV4_ADDRESS(concatenate(IPV4_ADDRESS, ":", for Each `PORT` in (contained(PORTS)))) | # Note that the actual nodes and edges logic will be `Host` `contains` `Networks` `contains` `IPV4_ADDRESS` `contains` `Transport` `contains` `Port`, where an IPV4_ADDRESS can have multiple transpoirts and multiple ports associated with each transport
| List of IPV4_ADDRESS(concatenate(IPV4_ADDRESS, ":", for Each `Port` in (contained(PORTS)))) | Nerva | none |
| List of Subdomains + Domain Names | HTTPX | List of website urls |
| List of website urls | Katana | Complete list of urls and internal urls |
| Complete list of urls and internal urls | Nuclei | none |

Consider the current GSL document, and the steps shown in the YAML workflow. Do they express the output variables correctly? IS this the reason that Nerva and Nuclei do not work? Can we be sure about this?



## 2. Refine Visual Utility of YAML DSL Visualisation, when embedded in the Composer

The YAML DSL Visualisation is working really great, but there is an outcome we never considered when embedding it in the Composer, where the view is zoomed out much further, than the viz appears natively in the raw iFrame. The shapes are a good size, but the text is far too small to read in general. Is it possible to look at the current DOM to discover the label sizes in the current YAML DSL Workflow iFrame?

Specifically, we need to address the following issues:

- The labels for the shapes are too small to read in general. Part of the reason for this is because we use the module name, e.g. `sfp_cli_subfinder`, which is too long, if the fiont size is much larger. Hence it would make a lot of sense to clip the prefix from the module name, and just use the last word of the module name, e.g. `subfinder`. The other labels, such as `start` and `target` are both small compared to their shapes, only the final shape with the word `context` is possibly too long a word if the font size is greatly increased.
- The labels on the edges are far too small to read. They can be smaller than the shape labels by a few points, but they still need to be readable
- Should we be using a slightly narrower, but much larger font?
- The tooltips are too small to read in general, the buttons are small too and hard to select. Can you make the tooltips and everything on it 50% larger?

### 2.2 Context Export Lines on Viz only For Steps Which Export Context

Finally, we need to refine the layout algorithm of the YAML DSL Workflow, when embedded in the Composer, to make it more accurate and consistent to the YAML DSL. This needs to be done carefully as we want to refine it, not break the 95% of excellent usability.

The key refinement is that rules for laying out semantic export edges, need to be refined so they are exactly as they are now, but also include:

- Semantic context ports are always on a scan step, but there is only an edge between the step and a context collector, if the context export is enabled for that step

Given that single rule, do you see which edges and context circles need to be updated?

Consider:

- `sfp-cli-subfinder` has no context export, so there should be no edge between it and a context collector, nor should there be a context collector, as that step does not require it
- `sfp-cli-nmap` has context export, so there should be an edge between it and a context collector, and a context collector, as that step requires it
- `sfp-cli-nerva` has context export, so there should be a an edge between it and a context collector, and a context collector, as that step requires it
- `sfp-cli-httpx` has no context export, so there should be no edge between it and a context collector, but it is on the same row as `sfp-cli-nmap` so there is still a context collector for that row, but no edge to it from `sfp-cli-httpx`
- `sfp-cli-katana` has no context export, so there should be no edge between it and a context collector, but it is on the same row as `sfp-cli-nerva` so there is still a context collector for that row, but no edge to it from `sfp-cli-katana`
- `sfp-cli-nuclei` has context export, so there should be an edge between it and a context collector, and a context collector, as that step requires it

Can you change the layout algorithm to make these changes, so it is not hard coded, but laid out as specified by the data in the YAML file? You must make sure this layout is still robust, even if steps are expanded or collapsed, and that the context collectors are always on the same row as the scan step that requires them.


## 3. Temporary Subgraphs Not Shown Immediately After they Are Saved to the Database

We need to get a better visual sequence of events happening so that the user can see what is happening and why. Currently, we save the temporary subgraphs to the database, but they are not shown immediately after they are saved, and we do not have a visual marker to show that the subgraph has been saved and is being processed.

### 3.1 Visual Progress Marker Needed for each Scan Step

Every scan step gets a list of 1 or more inputs, and thereby progress for every scan step can be measured as a progress through the list of inputs. Thus every step needs a progress indicator to show the progress through the list of inputs, e.g. `1 of n` where `n` is the number of inputs for the step.

### 3.2 Sequence of Events and Visual Indicators for Each Scan Step

Ideally, once a scan is complete, the following steps should be taken:

1. The four types of results are produced and properly saved to the database, with a visual marker to show that the subgraph has been saved and is being processed.
2. The temporary subgraph is produced and properly saved to the database, if the context export is enabled for the step
3. Control is transferred to the next steps in sequence, and the viz is updated with the colour of the step going completed state, and the following step in sequence is enabled and goes to the running state with a `1 of n` progress indicator, if there is a split this parallelises the steps, but if there is no split then it is a sequential step.
4. The temporary subgraph is then immediately shown in the Temporary Subgraph Viewer, while the progress indicator on the runningsteps is still on the first stemp
5. The progress indicator on the running steps is updated until scan progess is complete and the progress indicators is set to `n of n` and the cycle repeats from 1. again





## Issues with Nuclei Scan Step

Finally, the nucleai scan step is not working as expected. The error message is:
ERROR: timeout after 900.0s

But we do not even know if the correct inputs are being passed to the step, so we need to investigate this further, as described previously in this document