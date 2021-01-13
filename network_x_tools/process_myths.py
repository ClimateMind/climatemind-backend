from knowledge_graph import app
from network_x_tools.network_x_utils import network_x_utils
import networkx as nx


class process_myths:

    """

    Class used for Myth related functions. Uses a fresh copy of the NetworkX graph to
    return relevant information about myths including claims, rebuttals, sources, URLs,
    general myths and user specific myths.

    Any additional functions related to myths should be added here.

    Important to note that score_nodes cannot share the pickle file as score_nodes removes
    many of the myth nodes from the NetworkX object.
    """

    def __init__(self):
        self.G = None
        self.NX_UTILS = network_x_utils()
        self.node = None  # Current Node

    def get_node_id(self, node):
        """Node IDs are the unique identifier in the IRI. This is provided to the
        front-end as a reference for the feed, but is never shown to the user.

        Example http://webprotege.stanford.edu/R8znJBKduM7l8XDXMalSWSl
        """
        offset = 4  # .edu <- to skip these characters and get the unique IRI
        full_iri = node["iri"]
        pos = full_iri.find("edu") + offset
        return full_iri[pos:]

    def set_current_node(self, node):
        """We usually pull multiple myth related items about a particular node. Rather
        than pass these in individually for each function, this let's us use the same
        node for all of the functions in this class.
        """
        self.node = node

    def get_myth_claim(self):
        """Myth claims are used by the front-end to display a description of a
        phrase or claim the user might hear when someone says the myth.
        """
        try:
            return self.node["properties"]["schema_mythClaim"][0]
        except:
            return "No myth claim available at present"

    def get_myth_rebuttal(self):
        """Myth rebuttals are used by the front-end to display a description of a reason
        or rebuttal the user could say in response to someone saying the myth. The
        rebuttals are the reason(s) why the myth is not true and what the science
        says is true.
        """
        try:
            return self.node["properties"]["schema_mythRebuttal"][0]
        except:
            return "No myth rebuttal available at present"

    def get_myth_sources(self):
        """Myth sources are used by the frontend to display the source of the myth."""
        try:
            # return list(set(node["properties"]["schema_organizationSource"]))
            return list(set(self.node["myth sources"]))
        except:
            return []

    def get_myth_video_urls(self):
        """Myth video are used by the frontend to display the video url of the myth."""
        if self.node["properties"]["schema_video"]:
            try:
                return list(set(self.node["properties"]["schema_video"]))
            except:
                return "No videos available at present"
        else:
            return None

    def get_myth_fallacy(self):
        """Myth fallacy (also called 'faulty logic description') are used by the front-end
        to display a description of why a myth is logically wrong."""
        if self.node["properties"]["schema_mythFallacy"]:
            try:
                return self.node["properties"]["schema_mythFallacy"][0]
            except:
                return "No faulty logic description available at present"
        else:
            return None

    def get_effect_specific_myths(self):
        """Climate change impacts sometimes have myths about them.
        This function takes a node and returns the IRIs of any myths about the impact.
        """
        try:
            if "impact myths" in self.node.keys() and self.node["impact myths"]:
                if not self.G:
                    self.G = nx.read_gpickle("./Climate_Mind_DiGraph.gpickle")
                IRIs = []
                for myth_name in self.node["impact myths"]:
                    myth = self.G.nodes[myth_name]
                    IRIs.append(self.get_node_id(self.G.nodes[myth_name]))
            return IRIs
        except:
            return []

    def get_solution_specific_myths(self):
        """Climate change solutions sometimes have myths about them.
        This function takes a node and returns the IRIs of any myths about the solution.
        """
        try:
            if "solution myths" in self.node.keys() and self.node["solution myths"]:
                if not self.G:
                    self.G = nx.read_gpickle("./Climate_Mind_DiGraph.gpickle")
                IRIs = []
                for myth_name in self.node["solution myths"]:
                    myth = self.G.nodes[myth_name]
                    IRIs.append(self.get_node_id(self.G.nodes[myth_name]))
            return IRIs
        except:
            return []

    def get_specific_myth_info(self, iri):
        """
        Returns infomation for a specific myth.
        """
        if not self.G:
            self.G = nx.read_gpickle("./Climate_Mind_DiGraph.gpickle")
        all_myths = nx.get_node_attributes(self.G, "myth")

        specific_myth = None

        for myth in all_myths:
            self.NX_UTILS.set_current_node(self.G.nodes[myth])
            if self.NX_UTILS.get_node_id() == iri:
                specific_myth = myth

        if specific_myth:
            self.NX_UTILS.set_current_node(self.G.nodes[specific_myth])
            self.node = self.G.nodes[specific_myth]
            myth = {
                "iri": self.NX_UTILS.get_node_id(),
                "mythTitle": self.node["label"],
                "mythClaim": self.get_myth_claim(),
                "mythRebuttal": self.get_myth_rebuttal(),
                "mythSources": self.get_myth_sources(),
                "mythVideos": self.get_myth_video_urls(),
                "faultyLogicDescription": self.get_myth_fallacy(),
            }
            return myth
        else:
            return False

    def get_user_general_myth_nodes(self):
        """Returns a list of general myths and some information about those general myths.
        The myths will later be ranked based on user's personal values (although not being
        done in the current implementation).
        """
        if not self.G:
            self.G = nx.read_gpickle("./Climate_Mind_DiGraph.gpickle")
        general_myths = self.G.nodes["increase in greenhouse effect"]["general myths"]
        general_myths_details = []
        for myth in general_myths:
            self.NX_UTILS.set_current_node(self.G.nodes[myth])
            self.node = self.G.nodes[myth]
            d = {
                "iri": self.NX_UTILS.get_node_id(),
                "mythTitle": self.node["label"],
                "mythClaim": self.get_myth_claim(),
                "mythRebuttal": self.get_myth_rebuttal(),
                "mythSources": self.get_myth_sources(),
                "mythVideos": self.get_myth_video_urls(),
                "faultyLogicDescription": self.get_myth_fallacy(),
            }

            general_myths_details.append(d)

        return general_myths_details
