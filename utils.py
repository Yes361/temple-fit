from pgzero.builtins import Actor
from typing import List, Any, Tuple
            
def list_actor_attributes(actor: Actor, field_name: List[str]) -> dict[str, Any]:
    field = {}
    for name in field_name:
        field[name] = getattr(actor, name)
    return field
            
# def create_Actor(*args, **kwargs):
#     pass