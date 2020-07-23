from owlready2 import *

class Network:
    """ A class which runs a depth-first-search on the ontology and creates
        a graph network from the data.
        
        Parameters
        ----------
        ontology : OWL2 climate mind ontology file

           Completes a depth-first search for the ontology and return edges in
           the component reachable from source.    
    """

    def __init__(self, ontology):
        self.ontology = ontology
        self.result = []
        self.visited = set()
        self.node_family = []
        self.class_family = []

        
    def add_child_to_result(self, child, parent, edge_type):
        """ Adds a node to the results and if needed adds the node's family
        to node_family (a stack of nodes to continue exploring).
            
            Parameters
            ----------
            child: A node in the ontology
            parent: A node in the ontology
            edge_type: The relationship between child and parent 
                        i.e. causes, inhibits, etc
        """
        self.result.append((parent.label[0], child.label[0], edge_type))
        if child not in self.visited:
            self.visited.add(child)
            self.node_family.append((
                        child,
                        iter(child.causes_or_promotes),
                        "causes_or_promotes"
                        ))
            self.node_family.append((
                        child,
                        iter(child.is_inhibited_or_prevented_or_blocked_or_slowed_by),
                        "is_inhibited_or_prevented_or_blocked_or_slowed_by"
                        ))
            
    
    def add_class_to_explore(self, class_name):
        """ Adds all nodes related to a particular class. Some of these nodes
        will not actually be a class, but that is irrelevant as they will get ignored.
        
            Parameters
            ----------
            class_name: A node in the ontology
        """
        try:
            self.class_family.append((
                    class_name, 
                    iter(class_name.causes_or_promotes),
                    "causes_or_promotes"
                    ))
        except: pass
        try:
            self.class_family.append((
                    class_name, 
                    iter(class_name.is_inhibited_or_prevented_or_blocked_or_slowed_by),
                    "is_inhibited_or_prevented_or_blocked_or_slowed_by"
                    ))
        except: pass
        try:
            self.class_family.append((
                    class_name, 
                    iter(self.ontology.get_parents_of(class_name)),
                    "is_a"
                    )) # the class(es) of the ont_class
        except: pass   
            

    def dfs_for_classes(self, node):
        """ Performs a depth-first-search on parent classes from a node.
        
            Parameters
            ----------
            node: The starting point node in the ontology
        """
        visited_classes = set()
        classes = self.ontology.get_parents_of(node)
        
        if classes:
            
            for ont_class in classes:
                if ont_class != owl.Thing:
                    self.add_class_to_explore(ont_class)
                    
            while self.class_family:
                parent2, children2, edge_type2 = self.class_family[-1]
                visited_classes.add(parent2) #these are not all classses
            
                try:
                    child2 = next(children2)
                    if child2 != owl.Thing:
                        
                        if child2 in self.ontology.individuals():
                            self.add_child_to_result(child2, node, edge_type2)
                        elif child2 not in visited_classes and child2 in self.ontology.classes():
                            visited_classes.add(child2)
                            self.add_class_to_explore(child2)
                        
                except StopIteration:
                    self.class_family.pop() 
            
                   
    def dfs_labeled_edges(self):
        
        """ Produce edges in a depth-first-search (DFS) labeled by type.

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

        nodes = self.ontology.individuals()
    
        for node in nodes:
            if node not in self.visited:
                self.visited.add(node)
                self.node_family.append((
                            node, 
                            iter(node.causes_or_promotes),
                            "causes_or_promotes"
                            ))
                self.node_family.append((
                            node, 
                            iter(node.is_inhibited_or_prevented_or_blocked_or_slowed_by),
                            "is_inhibited_or_prevented_or_blocked_or_slowed_by"
                            ))
                
                while self.node_family:
                    parent, children, edge_type = self.node_family[-1]
                    self.visited.add(parent)
                    
                    try:
                        child = next(children)
                        self.add_child_to_result(child, parent, edge_type)
                        
                    except StopIteration:
                        self.node_family.pop()
                        self.dfs_for_classes(parent)


    def get_results(self):
        """ Returns
            -------
            result: A list of triples found by the depth-first-search
        """
        return self.result
