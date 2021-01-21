class network_x_utils:

    """

    This class provides commonly used utils which are shared between all different types
    of NetworkX nodes (Feed Items, Solutions, Myths). For each of these, we want to be
    able to pull basic information like the IRI, Descriptions, Images, etc.

    Include any generalized NetworkX functions here.

    """

    def __init__(self):
        self.node = None  # Current node

    def set_current_node(self, node):
        """We usually pull multiple node related items simultaneously. Rather
        than pass these in individually for each function, this let's us use the same
        node for all of the functions in this class.
        """
        self.node = node

    def get_node_id(self):
        """Node IDs are the unique identifier in the IRI. This is provided to the
        front-end as a reference for the feed, but is never shown to the user.

        Example http://webprotege.stanford.edu/R8znJBKduM7l8XDXMalSWSl
        """
        offset = 4  # .edu <- to skip these characters and get the unique IRI
        full_iri = self.node["iri"]
        pos = full_iri.find("edu") + offset
        return full_iri[pos:]

    def get_description(self):
        """Long Descriptions are used by the front-end to display explanations of the
        climate effects shown in user feeds.
        """
        try:
            return self.node["properties"]["schema_longDescription"][0]
        except:
            return "No long desc available at present"

    def get_short_description(self):
        """Short Descriptions are used by the front-end to display explanations of the
        climate effects shown in user feeds.
        """
        try:
            return self.node["properties"]["schema_shortDescription"][0]
        except:
            return "No short desc available at present"

    def get_image_url(self):
        """Images are displayed to the user in the climate feed to accompany an explanation
        of the climate effects. The front-end is provided with the URL and then requests
        these images from our server.
        """
        try:
            return self.node["properties"]["schema_image"][0]
        except:
            # Default image url if image is added
            return "https://yaleclimateconnections.org/wp-content/uploads/2018/04/041718_child_factories.jpg"

    def get_image_url_or_none(node):
        """Images are displayed to the user in the climate feed to accompany an explanation
        of the climate effects. The front-end is provided with the URL and then requests
        these images from our server.
        """
        try:
            return node["properties"]["schema_image"][0]
        except:
            # Default image url if image is added
            return None

    def get_causal_sources(self):
        """Sources are displayed to the user in the sources tab of the impacts overlay page.
        This function returns a list of urls of the sources to show on the impact overlay page for an impact/effect.
        Importantly, these sources aren't directly from the networkx node, but all the networkx edges that cause the node.
        Only returns edges that are directly tied to the node (ancestor edge sources are not used)
        """
        if "causal sources" in self.node and len(self.node["causal sources"]) > 0:
            causal_sources = self.node["causal sources"]

        try:
            return causal_sources
        except:
            return (
                []
            )  # Default source if none #should this be the IPCC? or the US National Climate Assessment?

    def get_solution_sources(self):
        """Returns a flattened list of custom solution source values from each node key that matches
        custom_source_types string.
        """
        try:
            return self.node["solution sources"]
        except:
            return []

    def get_is_possibly_local(self, node):
        """Returns whether it's possible that a node effects a particular user based on
        their location. Note that here we need to pass in the node directly, rather than
        using one set by the class as the node comes from the localised_acyclic_graph.py
        rather than a the standard graph.
        """
        if "isPossiblyLocal" in node:
            if node["isPossiblyLocal"]:
                return 1
            else:
                return 0
        else:
            return 0

    def get_co2_eq_reduced(self):
        """
        Returns the solution's CO2 Equivalent Reduced / Sequestered (2020–2050) in Gigatons.
        Values taken from Project Drawdown scenario 2.
        """
        if "CO2_eq_reduced" in self.node["data_properties"]:
            return self.node["data_properties"]["CO2_eq_reduced"]
        else:
            return 0
