

from models.assembly.assembly_params import AssemblyParams


class Assembly:
    def __init__(self, assembly_params: AssemblyParams):
        self.assembly_params = assembly_params