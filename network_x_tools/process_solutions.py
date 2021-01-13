from knowledge_graph import app

from network_x_tools.network_x_utils import network_x_utils
from network_x_tools.process_myths import process_myths

import numpy as np
import random
import networkx as nx


class process_solutions:
    def __init__(self, max_solutions=4, adaptation_to_mitigation_ratio=0.5):
        self.G = None
        self.NX_UTILS = network_x_utils()
        self.MYTH_PROCESS = process_myths()
        self.MAX_SOLUTIONS = max_solutions
        self.A_TO_M_RATIO = adaptation_to_mitigation_ratio

    def solution_randomizer(self, adaptation_solutions, mitigation_solutions):
        """Takes list of solutions and decides which adaptation solutions to randomly
        show and which mitigation solutions to randomly show.

        Parameters
        ----------
        adaptation_solutions - A list of adaptation solutions
        mititgation_solutions - A list of mitigation solutions
        """
        number_adaptation_max = np.math.floor(self.MAX_SOLUTIONS * self.A_TO_M_RATIO)
        if len(adaptation_solutions) <= number_adaptation_max:
            number_mitigation = self.MAX_SOLUTIONS - len(adaptation_solutions)
            solutions = adaptation_solutions + random.sample(
                mitigation_solutions, number_mitigation
            )
        else:
            solutions = random.sample(
                adaptation_solutions, number_adaptation_max
            ) + random.sample(
                mitigation_solutions, self.MAX_SOLUTIONS - number_adaptation_max
            )
        return solutions

    def get_user_general_solution_nodes(self):
        """Returns a list of general solutions and some information about those general
        solutions. The myths will later be ranked based on user's personal values
        (although not being done in the current implementation).
        """
        if not self.G:
            self.G = nx.read_gpickle("./Climate_Mind_DiGraph.gpickle")
        general_solutions = self.G.nodes["increase in greenhouse effect"][
            "mitigation solutions"
        ]
        general_solutions_details = []

        for solution in general_solutions:
            try:
                self.NX_UTILS.set_current_node(self.G.nodes[solution])
                self.MYTH_PROCESS.set_current_node(self.G.nodes[solution])
                d = {
                    "iri": self.NX_UTILS.get_node_id(),
                    "solutionTitle": self.G.nodes[solution]["label"],
                    "solutionType": "mitigation",
                    "shortDescription": self.NX_UTILS.get_short_description(),
                    "longDescription": self.NX_UTILS.get_description(),
                    "imageUrl": self.NX_UTILS.get_image_url_or_none(),
                    "solutionSpecificMythIRIs": self.MYTH_PROCESS.get_solution_specific_myths(),
                    "solutionSources": self.NX_UTILS.get_solution_sources(),
                }
            except:
                pass

            if d not in general_solutions_details:
                general_solutions_details.append(d)

        return general_solutions_details

    def get_user_actions(self, effect_name):
        """Takes the name of a climate effect and returns a list of actions associated
        with that node.
        """
        if not self.G:
            self.G = nx.read_gpickle("./Climate_Mind_DiGraph.gpickle")
        solution_names = self.G.nodes[effect_name]["adaptation solutions"]
        adaptation_solutions = []
        mitigation_solutions = []
        for solution in solution_names:
            try:
                self.NX_UTILS.set_current_node(self.G.nodes[solution])
                self.MYTH_PROCESS.set_current_node(self.G.nodes[solution])
                s_dict = {
                    "iri": self.NX_UTILS.get_node_id(),
                    "solutionTitle": self.G.nodes[solution]["label"],
                    "solutionType": "adaptation",
                    "shortDescription": self.NX_UTILS.get_short_description(),
                    "longDescription": self.NX_UTILS.get_description(),
                    "imageUrl": self.NX_UTILS.get_image_url_or_none(),
                    "solutionSpecificMythIRIs": self.MYTH_PROCESS.get_solution_specific_myths(),
                    "solutionSources": self.NX_UTILS.get_solution_sources(),
                }

                # only include direct adaptation solutions (ignore adaptation solutions that are upstream for now)
                for neighbor in self.G.neighbors(effect_name):
                    if (
                        self.G[effect_name][neighbor]["type"]
                        == "is_inhibited_or_prevented_or_blocked_or_slowed_by"
                        and neighbor == solution
                    ):
                        adaptation_solutions.append(s_dict)

            except:
                pass
        solution_names = self.G.nodes["increase in greenhouse effect"][
            "mitigation solutions"
        ]
        for solution in solution_names:
            try:
                self.NX_UTILS.set_current_node(self.G.nodes[solution])
                self.MYTH_PROCESS.set_current_node(self.G.nodes[solution])
                s_dict = {
                    "iri": self.NX_UTILS.get_node_id(),
                    "solutionTitle": self.G.nodes[solution]["label"],
                    "solutionType": "mitigation",
                    "shortDescription": self.NX_UTILS.get_short_description(),
                    "longDescription": self.NX_UTILS.get_description(),
                    "imageUrl": self.NX_UTILS.get_image_url_or_none(),
                    "solutionSpecificMythIRIs": self.MYTH_PROCESS.get_solution_specific_myths(),
                    "solutionSources": self.NX_UTILS.get_solution_sources(),
                }
                mitigation_solutions.append(s_dict)
            except:
                pass
        solutions = self.solution_randomizer(
            adaptation_solutions,
            mitigation_solutions,
        )
        return solutions
