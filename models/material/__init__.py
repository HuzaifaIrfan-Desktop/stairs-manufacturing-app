

from models.material.lumber import available_lumbers
from models.material.plywood import available_plywoods

available_materials = {**available_lumbers, **available_plywoods}