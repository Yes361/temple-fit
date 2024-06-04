from pgzero.builtins import Actor
from typing import List, Any, Tuple
            
def list_actor_attributes(actor: Actor, field_name: List[str]) -> dict[str, Any]:
    """
    @param actor
    @param field_name The desired fields
    @return: A dictionary containing the values of the desired fields
    """
    field = {}
    for name in field_name:
        field[name] = getattr(actor, name)
    return field

def require_kwargs(fields, kwargs):
    """
    END ME
    """
    for field in fields:
        if field not in kwargs:
            raise Exception(f'{field} is required.')