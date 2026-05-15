from __future__ import annotations

from planning.pddl import ActionSchema, State, Objects, get_all_groundings


def nullHeuristic(
    state: State,
    goal: State,
    domain: list[ActionSchema],
    objects: Objects,
) -> float:
    """Trivial heuristic — always returns 0 (equivalent to uniform-cost search)."""
    return 0


# ---------------------------------------------------------------------------
# Punto 4a – Ignore-Preconditions Heuristic
# ---------------------------------------------------------------------------


def ignorePreconditionsHeuristic(
    state: State,
    goal: State,
    domain: list[ActionSchema],
    objects: Objects,
) -> float:
    """
    Admissible heuristic based on a greedy set-cover relaxation.

    Ignores all action preconditions so every grounded action is always
    applicable. Counts the minimum number of actions needed to cover all
    unsatisfied goal fluents (lower bound on true plan length).
    """
    unsatisfied = goal - state
    if not unsatisfied:
        return 0

    groundings = get_all_groundings(domain, objects)
    actions_taken = 0

    while unsatisfied:
        best_action = max(groundings, key=lambda a: len(a.add_list & unsatisfied))
        coverage = len(best_action.add_list & unsatisfied)

        if coverage == 0:
            # Goal fluents unreachable — return remaining count as upper bound
            return len(unsatisfied)

        unsatisfied -= best_action.add_list
        actions_taken += 1

    return actions_taken


# ---------------------------------------------------------------------------
# Punto 4b – Ignore-Delete-Lists Heuristic
# ---------------------------------------------------------------------------


def ignoreDeleteListsHeuristic(
    state: State,
    goal: State,
    domain: list[ActionSchema],
    objects: Objects,
) -> float:
    """
    Estimate the plan cost by solving a relaxed problem where no action
    has a delete list (effects never remove fluents from the state).

    In this monotone relaxation, the state only grows over time (fluents are
    never removed), so hill-climbing always makes progress and cannot loop.

    Algorithm (hill-climbing on the relaxed problem):
      1. Start from the current state with a relaxed (monotone) apply function.
      2. At each step, pick the grounded action that adds the most unsatisfied
         goal fluents (greedy hill-climbing).
      3. Count steps until all goal fluents are satisfied (or until no progress).

    Tip: In the relaxed problem, apply_action never removes fluents.
         You can implement this by treating del_list as empty for all actions.
         Use get_applicable_actions to enumerate applicable grounded actions at
         each step (preconditions still apply in the relaxed model).
    """
    ### Your code here ###

    ### End of your code ###
