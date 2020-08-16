# Let's start by creating a function that just extracts candidate DNEs
# and define our skeleton ranking function as just throwing runifs at
# candidates at returning the top_k requested, with the associated score 
# and rank

import networkx as nx
import random

# Should probably import this from somewhere general purpose
def load_ontology(fpath='knowledge_graph/Climate_Mind_DiGraph.gpickle'):
    return nx.read_gpickle(fpath)

class NodeRecommender:
    def __init__(self, 
                 g: nx.DiGraph):
        self.g = g
    @property
    def candidates(self):
        if not hasattribute(self, '_candidates'):
            self._candidates = self.get_scoring_candidates(self.g)
        return self._candidates
    @staticmethod
    def get_node_scoring_candidates(g):
        candidates = []
        for node_id, node_data in g.nodes(data=True):
            if 'downstream negative effect' in node_data['classes']:
                candidates.append(node_id)
        return candidates
    @staticmethod
    def get_node_scoring_features(g, node_id):
        pass
    @staticmethod
    def get_user_scoring_features(g, user_id):
        pass
    
    def topk_nodes(self, user_id, top_k=None):
        candidates = self.get_node_scoring_candidates(self.g)
        
        # dummy random scoring
        random.seed(hash(user_id)) # eliminate stochasticity for now
        scored = [[c, random.random()] for c in candidates]
        scored.sort(key = lambda x: x[1], reverse=True)
        
        if top_k:
            return scored[:top_k]
        return scored
    
    def topk_paths(self, user_id, node_id, top_k=None):
        pass
    
    
if __name__ == '__main__':
    g = load_ontology()
    scorer = NodeRecommender(g)

    # scorer.topk_nodes('foo')
    # scorer.topk_nodes('bar')
