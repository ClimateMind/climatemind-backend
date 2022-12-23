# Ontology

## Process the Ontology

_**Follow these steps every time you are made aware of an update to the Ontology.**_

1. Download a fresh copy of the Ontology from web protege. Make sure it's the RDF/XML format (check the downloaded item has .owl at the end of it!).
2. Run the `process_owl` flask command by executing the following (replace `<relative/path/filename.owl>`):

```
flask ontology process_owl <relative/path/filename.owl>
```

Use `--no-check` argument to skip comparison with the previous Ontology.

## FAQ

**Q: Which files need to be in the repo for the app to have access to the data?** A: The .gpickle file needs to be in the climatemind-backend/output folder. As long as it has this file, the app will have data to work with. _The OWL File is not needed in the backend-repo_

**Q: How does the production application get access to the climate data?** A: The .gpickle file is included in the commits to the repo. When this is pushed to the main branch, the production application has access to the .gpickle file
