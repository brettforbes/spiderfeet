# Documenting and Classifying OSINT Services Modules

Spiderfoot is a module-based system that allows you to collect data from various OSINT servicwes. Each module is responsible for collecting data from a specific source. The data is then stored in the database and can be used for further analysis.

There are 233 modules in the `modules` directory. Each module is a Python file that contains a class that inherits from `SpiderFootPlugin`. Each class has a `meta` dictionary that contains the metadata for the module. Not all modules are external data sources. Some modules are internal to Spiderfoot and are used to perform analysis on the data.

## Summarising the OSINT Service Modules

We are interested in parsing each module, to test if it contains the field `dataSource` in its metadata. If it does, we should extract its metadata, the list of events that each module listens to, and the list of events it prooduces to be collected together in a data object we will call an `OSINT Service`. The aim is to have a maximal, yet consistent data model that can be applied to every OSINT service.

These OSINT data objects will be gathered into a servcices list, and saved in the file `.docs\analysis\osint_services.json`

Can you develop code in `.docs\analysis\analyse_modules.py` to achieve this? Can we then run it once to see what the data looks like to see if it needs refining?
