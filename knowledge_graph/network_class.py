import typing
import owlready2
from owlready2 import *
from knowledge_graph.ontology_processing_utils import give_alias


class Network:
    """A class which runs a depth-first-search on the ontology and creates
    a graph network from the data.

    Parameters
    ----------
    ontology : OWL2 climate mind ontology file

       Completes a depth-first search for the ontology and return edges in
       the component reachable from source.

    Sample Usage
    ------------
        onto = get_ontology(onto_path).load()
        node_network = Network(onto, source)
        node_network.dfs_labeled_edges()
        df = pd.DataFrame(node_network.edge_triplets,
                     columns=["subject", "object", "predcate"])
    """

    def __init__(self, ontology, source=None):
        self.ontology = ontology
        self.edge_triplets = []
        self.visited = set()
        self.node_family = []
        self.class_family = []
        if source:
            self.source = source
        else:
            self.source = None
        # Add labels the ontology object in a way that makes them pythonicly accessible through . invocation method.
        obj_props = list(self.ontology.object_properties())
        annot_props = list(self.ontology.annotation_properties())
        data_props = list(self.ontology.data_properties())
        self.obj_properties = [give_alias(x) for x in obj_props if x.label]
        self.annot_properties = [give_alias(x) for x in annot_props if x.label]
        self.data_properties = [give_alias(x) for x in data_props if x.label]

    def add_child_to_result(self, child, parent, edge_type):
        """Adds a node to the results and if needed adds the node's family
        to node_family (a stack of nodes to continue exploring).

            Parameters
            ----------
            child: A node in the ontology
            parent: A node in the ontology
            edge_type: The relationship between child and parent
                        i.e. causes, inhibits, etc
        """
        self.edge_triplets.append((parent.label[0], child.label[0], edge_type))
        if child not in self.visited:
            self.visited.add(child)
            for obj_prop in self.obj_properties:
                val = getattr(child, obj_prop)
                rec = (child, iter(val), obj_prop)
                self.node_family.append(rec)

    def add_class_to_explore(self, owl_class_obj: owlready2.entity.ThingClass):
        """Adds all nodes related to a particular class. Some of these nodes
        will not actually be a class, but that is irrelevant as they will get ignored.

            Parameters
            ----------
            owl_class_obj: A node in the ontology
        """
        for obj_prop in self.obj_properties:
            if hasattr(owl_class_obj, obj_prop):
                val = getattr(owl_class_obj, obj_prop)
                rec = (owl_class_obj, iter(val), obj_prop)  # why iter()?
                self.class_family.append(rec)

        parents = self.ontology.get_parents_of(owl_class_obj)
        rec = (owl_class_obj, iter(parents), "is_a")
        self.class_family.append(rec)
        # the class(es) of the ont_class. This could pull classes that are just Restriction classes, so really should add code here that checks the class is found in self.ontology.classes() before adding it to the class_family.

    def dfs_for_classes(self, node):
        """Performs a depth-first-search on parent classes from a node.

        Parameters
        ----------
        node: The starting point node in the ontology
        """
        visited_classes = set()
        classes = self.ontology.get_parents_of(node)

        if classes:

            for ont_class in classes:
                # if ont_class != owl.Thing:
                if isinstance(ont_class, owlready2.entity.ThingClass):
                    self.add_class_to_explore(ont_class)

            while self.class_family:
                parent2, children2, edge_type2 = self.class_family.pop()
                visited_classes.add(parent2)
                for child2 in children2:
                    # if child2 != owl.Thing: # ?
                    if child2 == owl.Thing:  # fr though, what is this?
                        continue

                    if child2 in self.ontology.individuals():
                        self.add_child_to_result(child2, node, edge_type2)
                    elif (
                        child2 not in visited_classes
                        and child2 in self.ontology.classes()
                    ):
                        # It's a "visited class" but we're adding it to "classes to explore?"
                        # `visited_classes` is scoped local to this function. Probably
                        # just need to name it something else.
                        visited_classes.add(child2)
                        self.add_class_to_explore(child2)

    def dfs_labeled_edges(self):

        """Produce edges in a depth-first-search (DFS) labeled by type.

        Notes
        -----
        Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
        by D. Eppstein, July 2004.
        If a source is not specified then a source is chosen arbitrarily and
        repeatedly until all components in the graph are searched.

        TODO Find why a couple of duplicates are created
        Example: increase in carbon capture,
                  greenhouse-gas externality,
                  is_inhibited_or_prevented_or_blocked_or_slowed_by

        """
        if self.source:
            nodes = [self.ontology.search_one(label=self.source)]
        else:
            nodes = self.ontology.individuals()

        for node in nodes:
            if node not in self.visited:
                self.visited.add(node)
                for obj_prop in self.obj_properties:
                    val = getattr(node, obj_prop)
                    rec = (node, iter(val), obj_prop)
                    self.node_family.append(rec)

                while self.node_family:
                    parent, children, edge_type = self.node_family.pop()
                    self.visited.add(parent)
                    for child in children:
                        self.add_child_to_result(child, parent, edge_type)
                    self.dfs_for_classes(parent)
