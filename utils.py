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

def create_actor(*args, **kwargs):
    """
    Allows Custom Properties to be passed as parameters to the initialization of Actor
    @return: An Actor
    """
    expected_kwargs = set(Actor.EXPECTED_INIT_KWARGS).union(set(['pos', 'image']))
    
    custom_properties = set(kwargs) - expected_kwargs
    acceptable_kwargs = set(kwargs).intersection(expected_kwargs)
    new_kwargs = {key: kwargs[key] for key in acceptable_kwargs}
    
    actor = Actor(*args, **new_kwargs)
    for property in custom_properties:
        setattr(actor, property, kwargs[property])
        
    return actor    