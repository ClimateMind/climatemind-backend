from flask import current_app

from app.network_x_tools.network_x_utils import network_x_utils
from app.myths.process_myths import process_myths

import numpy as np
import random
import networkx as nx


class process_solutions:

    """

    Solutions can be divided into two categories, mitigations and adaptations. Both of
    these are shown as potential solutions to climate issues affecting the user.

    Class used for solution related functions. Uses a fresh copy of the NetworkX graph to
    return relevant information about solutions.

    Any additional functions related to solutions should be added here.

    """

    def __init__(self, max_solutions=4, adaptation_to_mitigation_ratio=0.5):
        self.G = current_app.config["G"].copy()
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
        solutions. The solutions are ordered from highest to lowest CO2 Equivalent
        Reduced / Sequestered (2020–2050) in Gigatons from Project Drawdown scenario 2.
        """
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
                    "solutionCo2EqReduced": self.NX_UTILS.get_co2_eq_reduced(),
                }
            except:
                pass

            if d not in general_solutions_details:
                general_solutions_details.append(d)

        return general_solutions_details

    def get_user_actions(self, effect_name):
        """
        Takes the name of a climate effect and returns a list of actions associated
        with that node.
        """
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
