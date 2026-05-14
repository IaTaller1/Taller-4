from __future__ import annotations

from planning.pddl import ActionSchema

# ---------------------------------------------------------------------------
# Punto 1a – Complete the preconditions and effects of each action schema.
#
# Each schema uses string variable names as placeholders:
#   "r"         → the robot
#   "from_cell" → source cell       "to_cell" → destination cell
#   "obj"       → any pickable object
#   "s"         → medical supplies  "p" → patient
#   "loc"       → a cell (used as the robot's current location)
#
# Fluent templates are tuples whose elements are either variable names or
# literal constant strings. get_applicable_actions() will substitute
# variable names with real constants during grounding.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Move(r, from_cell, to_cell)
# Move the robot one step to an adjacent, free cell.
# This one is given as an example. You can use it as a template for the other actions.
# ---------------------------------------------------------------------------

MOVE: ActionSchema = ActionSchema(
    name="Move",
    parameters=["r", "from_cell", "to_cell"],
    precond_pos=[
        ("At", "r", "from_cell"),
        ("Adjacent", "from_cell", "to_cell"),
        ("Free", "to_cell"),
    ],
    precond_neg=[],
    add_list=[
        ("At", "r", "to_cell"),
        ("Free", "from_cell"),
    ],
    del_list=[
        ("At", "r", "from_cell"),
        ("Free", "to_cell"),
    ],
)


# ---------------------------------------------------------------------------
# PickUp(r, obj, loc)
# Pick up a pickable object at the robot's current cell.
# After pickup: the object is no longer At loc, and the robot is no longer HandsFree.
# ---------------------------------------------------------------------------

### Your code here ###
# CODIGO PRE-IA:
# PICKUP: ActionSchema = ActionSchema(
#     name="PickUp",
#     parameters=["r", "obj", "loc"],
#     precond_pos=[
#         ("At", "r", "loc"),
#         ("At", "obj", "loc"),
#         ("HandsFree", "r"),
#         ("Pickable", "obj"),
#     ],
#     precond_neg=[],
#     add_list=[
#         ("Holding", "r", "obj"),
#         ("At", "obj", "loc"),   # ERROR: debería estar en del_list
#     ],
#     del_list=[
#         ("HandsFree", "r"),     # Faltaba ("At", "obj", "loc")
#     ],
# )
#
# PROMPT
# Tengo implementados los 4 ActionSchema de domain.py pero cuando corro
# python main.py -p SimpleRescueProblem -f tinyBaseSearch -l tinyBase -q
# el plan falla. creo que los errores están en PickUp donde puse At(obj,loc)
# en el add_list cuando creo que debería estar en del_list, en SetupSupplies
# donde puse At(s,loc) como precondición pero el robot ya lo está cargando,
# en Rescue donde se me olvidó SuppliesReady, y en PutDown donde metí
# At(r,loc) en del_list por error. revisa estos 4 y corrígelos.
#
# --- Código post-IA ---
PICKUP: ActionSchema = ActionSchema(
    name="PickUp",
    parameters=["r", "obj", "loc"],
    precond_pos=[
        ("At", "r", "loc"),
        ("At", "obj", "loc"),
        ("HandsFree", "r"),
        ("Pickable", "obj"),
    ],
    precond_neg=[],
    add_list=[
        ("Holding", "r", "obj"),
    ],
    del_list=[
        ("At", "obj", "loc"),
        ("HandsFree", "r"),
    ],
)
### End of your code ###


# ---------------------------------------------------------------------------
# PutDown(r, obj, loc)
# Place a held object at the robot's current cell.
# After putdown: the object is At loc, and the robot is HandsFree again.
# ---------------------------------------------------------------------------

### Your code here ###
# CODIGO PRE-IA
# PUTDOWN: ActionSchema = ActionSchema(
#     name="PutDown",
#     parameters=["r", "obj", "loc"],
#     precond_pos=[
#         ("At", "r", "loc"),
#         ("Holding", "r", "obj"),
#     ],
#     precond_neg=[],
#     add_list=[
#         ("At", "obj", "loc"),
#         ("HandsFree", "r"),
#     ],
#     del_list=[
#         ("Holding", "r", "obj"),
#         ("At", "r", "loc"),    # ERROR: el robot no se mueve al soltar el objeto
#     ],
# )
#
# CODIGO POST-IA (mismo prompt que PICKUP):
PUTDOWN: ActionSchema = ActionSchema(
    name="PutDown",
    parameters=["r", "obj", "loc"],
    precond_pos=[
        ("At", "r", "loc"),
        ("Holding", "r", "obj"),
    ],
    precond_neg=[],
    add_list=[
        ("At", "obj", "loc"),
        ("HandsFree", "r"),
    ],
    del_list=[
        ("Holding", "r", "obj"),
    ],
)
### End of your code ###


# ---------------------------------------------------------------------------
# Rescue(r, p, loc)
# Rescue a patient who is at a medical post where supplies are ready.
# After rescue: patient is marked as Rescued and no longer At loc.
# ---------------------------------------------------------------------------

### Your code here ###
# CODIGO PRE-IA:
# RESCUE: ActionSchema = ActionSchema(
#     name="Rescue",
#     parameters=["r", "p", "loc"],
#     precond_pos=[
#         ("At", "r", "loc"),
#         ("At", "p", "loc"),
#         ("MedicalPost", "loc"),
#         # ERROR: faltaba ("SuppliesReady", "loc")
#     ],
#     precond_neg=[],
#     add_list=[
#         ("Rescued", "p"),
#     ],
#     del_list=[
#         ("At", "p", "loc"),
#     ],
# )
#
# CODIGO POST-IA (mismo prompt que PICKUP):
RESCUE: ActionSchema = ActionSchema(
    name="Rescue",
    parameters=["r", "p", "loc"],
    precond_pos=[
        ("At", "r", "loc"),
        ("At", "p", "loc"),
        ("MedicalPost", "loc"),
        ("SuppliesReady", "loc"),
    ],
    precond_neg=[],
    add_list=[
        ("Rescued", "p"),
    ],
    del_list=[
        ("At", "p", "loc"),
    ],
)
### End of your code ###


# ---------------------------------------------------------------------------
# SetupSupplies(r, s, loc)
# Set up medical supplies at a medical post.
# The robot must be at loc, holding the supplies, and loc must be a MedicalPost.
# Note: there is no At(s, loc) precondition because the robot is carrying s;
# the fluent At(s, loc) was removed when the robot picked it up.
# ---------------------------------------------------------------------------

### Your code here ###
# CODIGO PRE-IA:
# SETUP_SUPPLIES: ActionSchema = ActionSchema(
#     name="SetupSupplies",
#     parameters=["r", "s", "loc"],
#     precond_pos=[
#         ("At", "r", "loc"),
#         ("At", "s", "loc"),    # ERROR: fluente ya eliminado al hacer PickUp
#         ("MedicalPost", "loc"),
#         ("Holding", "r", "s"),
#     ],
#     precond_neg=[],
#     add_list=[
#         ("SuppliesReady", "loc"),
#         ("HandsFree", "r"),
#     ],
#     del_list=[
#         ("Holding", "r", "s"),
#     ],
# )
#
# CODIGO POST-IA (mismo prompt que PICKUP arriba):
SETUP_SUPPLIES: ActionSchema = ActionSchema(
    name="SetupSupplies",
    parameters=["r", "s", "loc"],
    precond_pos=[
        ("At", "r", "loc"),
        ("MedicalPost", "loc"),
        ("Holding", "r", "s"),
    ],
    precond_neg=[],
    add_list=[
        ("SuppliesReady", "loc"),
        ("HandsFree", "r"),
    ],
    del_list=[
        ("Holding", "r", "s"),
    ],
)
### End of your code ###


DOMAIN: list[ActionSchema] = [MOVE, PICKUP, PUTDOWN, RESCUE, SETUP_SUPPLIES]
