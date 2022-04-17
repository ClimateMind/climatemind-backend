from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentFeed
from flask import current_app
from random import sample, shuffle


def create_alignment_feed(conversation_uuid, quiz_uuid, alignment_feed_uuid):
    """
    Calculate aligned feed based on user a and b quiz results and add to the alignment feed table.

    This is currently a dummy function.

    Parameters
    ==============
    conversation_uuid (UUID)
    quiz_uuid (UUID) - user b quiz uuid to compare scores with user a scores
    alignment_feed_uuid (UUID) - uuid created when post alignment endpoint is used
    """
    # TODO: Add logic to create aligned feed. Currently working with hard-coded dummy values.

    try:
        alignment_feed = AlignmentFeed()
        alignment_feed.alignment_feed_uuid = alignment_feed_uuid
        alignment_feed.aligned_effect_1_iri = "R9JAWzfiZ9haeNhHiCpTWkr"
        alignment_feed.aligned_effect_2_iri = "R8JoXNnKTYqERwU7fblKTWB"
        alignment_feed.aligned_effect_3_iri = "RB7k7p2iQQgKdQrkRP2MZWM"
        assign_alignment_solution_iris(alignment_feed, find_alignment_solution_iris())
        db.session.add(alignment_feed)
        db.session.commit
    except:
        raise DatabaseError(
            message="An error occurred while adding the alignment feed to the database."
        )

def assign_alignment_solution_iris(alignment_feed, solution_iris):
    """Set the solution iri fields of the alignment feed."""
    solution_iris = find_alignment_solution_iris()
    for (index, iri) in enumerate(solution_iris, start=1):
        setattr(alignment_feed, 'aligned_solution_{}_iri'.format(index), iri)

def find_alignment_solution_iris():
    """Choose solutions for the alignment."""  # TODO: expand docstring
    talk_solution_iri = ''  # TODO: hardcode this?
    popular_solution_iris = {}  # TODO: will hardcode this?
    popular_count = 4
    unpopular_count = 2
    solution_map = {'talk':None, 'popular':set(), 'unpopular':set()}
    solution_nodes = get_solution_nodes()
    for node in solution_nodes:
        iri = node['iri']
        if (iri == talk_solution_iri):
            solution_map['talk'] = iri
        elif (iri in popular_solution_iris):
            solution_map['popular'].append(iri)
        else:
            solution_map['unpopular'].append(iri)
    sample_solutions = sample(solution_map['popular'], popular_count) + sample(solution_map['unpopular'], unpopular_count)
    shuffle(sample_solutions)
    return [solution_map['talk']] + sample_solutions

def get_solution_nodes():
    """Find the solution nodes in the ontoloy."""
    G = current_app.config["G"].copy()
    return [node for node in G.nodes if 'risk solution' in node.keys()]  # TODO: is this the right condition?
