from owlready2 import *

class Network:
    """ A class which runs a depth-first-search on the ontology and creates
        a graph network from the data.
        
        Parameters
        ----------
        ontology : OWL2 climate mind ontology file
        edge_type : causes_or_promotes, is_inhibited_or_prevented_or_blocked_by        
        start_point : node, optional
           Specify starting node for depth-first search and return edges in
           the component reachable from source.    
    """

    def __init__(self, ontology, edge_type, start_point):
        self.ontology = ontology
        self.edge_type = edge_type
        self.result = []
        self.visited = set()
        self.node_family = []
        if start_point:
            self.source = start_point
        else:
            self.source = None

        
    def add_child_to_result(self, child, parent):
        """ Adds a node to the results and if needed adds the node's family
        to node_family (a stack of nodes to continue exploring).
        """
        self.result.append((parent.label[0], child.label[0], self.edge_type))
        if child not in self.visited:
            self.visited.add(child)
            self.node_family.append((child, iter(getattr(child, self.edge_type)))) 

    def dfs_for_classes(self, node):
        """ Performs a depth-first-search on parent classes from a node.
        
            Parameters
            ----------
            node: The starting point node in the ontology
        """
        visited_classes = set()
        classes = self.ontology.get_parents_of(node)
        
        if classes:
            class_family = []
            
            for ont_class in classes:
                if ont_class != owl.Thing:
                    try:
                        class_family.append((ont_class, iter(getattr(ont_class, self.edge_type))))
                        class_family.append((ont_class, iter(self.ontology.get_parents_of(ont_class))))
                    except:
                        pass # Restriction objects are causing an error, should investigate more
           
            while class_family:
                parent2, children2 = class_family[-1]
                visited_classes.add(parent2) #how do we know that parent2 is a class? it doesn't matter?
            
                try:
                    child2 = next(children2)
                    if child2 != owl.Thing:
                
                        if child2 in self.ontology.individuals():
                            self.add_child_to_result(child2, node)
                            
                        elif child2 not in visited_classes and child2 in self.ontology.classes():
                            visited_classes.add(child2)
                            class_family.append((child2, iter(getattr(child2, self.edge_type))))
                            class_family.append((child2, iter(self.ontology.get_parents_of(child2))))
                        
                except StopIteration:
                    class_family.pop() 
            
                   
    def dfs_labeled_edges(self):
        
        """ Produce edges in a depth-first-search (DFS) labeled by type.

        Notes
        -----
        Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
        by D. Eppstein, July 2004.
        If a source is not specified then a source is chosen arbitrarily and
        repeatedly until all components in the graph are searched.
        """
    
        if self.source is None:
            nodes = self.ontology.individuals()
        else:
            nodes = [self.source]
    
        for node in nodes:
            if node not in self.visited:
                self.visited.add(node)
                self.node_family.append((node, iter(getattr(node, self.edge_type))))
                while self.node_family:
                    parent, children = self.node_family[-1]
                    try:
                        child = next(children)
                        self.add_child_to_result(child, parent)
                    except StopIteration:
                        self.node_family.pop()
                        self.dfs_for_classes(parent)


    def get_results(self):
        """ Returns
            -------
            result: A list of triples found by the depth-first-search
        """
        return self.result