import cadquery as cq

from models.part.part_params import PartParams

class Part:
    def __init__(self, part_params: PartParams):
        self.part_params = part_params

        self.cq_part = self._build()

    
    def _build(self)-> cq.Workplane:
        # Create a simple part based on the parameters
        return (
            cq.Workplane("XY")
            .box(self.part_params.length, self.part_params.width, self.part_params.height)
        )

    def get(self)-> cq.Workplane:
        return self.cq_part