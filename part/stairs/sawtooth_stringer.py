

import cadquery as cq
from utils.math import inch_to_mm


from part.part import Part
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams


class SawtoothStringer(Part):
    def __init__(self, stringer_params: SawtoothStringerParams):
        print(f"Creating SawtoothStringer with params: {stringer_params}")
        self.stringer_params = stringer_params
        # _build is run by parent class Part and it uses self.stringer_params
        # to create the part, so we call super().__init__ here
        super().__init__(stringer_params)


    def _build(self) -> cq.Workplane:
        # Create a simple sawtooth stringer part

        points = []

        first_x = inch_to_mm(self.stringer_params.bottom_stringer_depth)
        first_y = 0


        current_x = first_x
        current_y = first_y
        points.append((current_x, current_y))

        if self.stringer_params.kicker_height > 0 and self.stringer_params.kicker_depth > 0:
            current_x+= -(inch_to_mm(self.stringer_params.bottom_stringer_depth)-inch_to_mm(self.stringer_params.kicker_depth))
            points.append((current_x, current_y))
            current_y += inch_to_mm(self.stringer_params.kicker_height)
            points.append((current_x, current_y))

            current_x += -inch_to_mm(self.stringer_params.kicker_depth)
            points.append((current_x, current_y))
            current_y += (inch_to_mm(self.stringer_params.first_step_rise_height)-inch_to_mm(self.stringer_params.kicker_height))
            points.append((current_x, current_y))

        else:
            current_x += -inch_to_mm(self.stringer_params.bottom_stringer_depth)
            points.append((current_x, current_y))
            current_y += inch_to_mm(self.stringer_params.first_step_rise_height)
            points.append((current_x, current_y))
        
        for i in range(self.stringer_params.number_of_stringer_run):
            current_x += inch_to_mm(self.stringer_params.step_run_depth)
            points.append((current_x, current_y))
            current_y += inch_to_mm(self.stringer_params.step_rise_height)
            points.append((current_x, current_y))

        current_x += inch_to_mm(self.stringer_params.last_step_run_depth)
        points.append((current_x, current_y))

        current_y -= inch_to_mm(self.stringer_params.back_stringer_reverse_height)
        points.append((current_x, current_y))

        stringer_part=(
            cq.Workplane("XZ").polyline(points).close().extrude(inch_to_mm(self.stringer_params.stringer_thickness))
        )
        return stringer_part
    