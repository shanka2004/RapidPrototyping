from build123d import *
set_defaults(helper_scale=1, transparent=True)

with BuildPart() as bp:
    with PolarLocations(3,8) as locs:
        Box(1,1,1)

show_all()