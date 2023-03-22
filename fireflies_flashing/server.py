"""
Configure visualization elements and instantiate a server
"""

from .model import Fireflies_FlashingModel, Firefly  # noqa

import mesa


def circle_portrayal_example(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
        "Color": "Pink",
    }
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    circle_portrayal_example, 20, 20, 500, 500
)
chart_element = mesa.visualization.ChartModule([{"Label": "Fireflies-Flashing", "Color": "Pink"}])

model_kwargs = {"num_agents": 10, "width": 10, "height": 10}

server = mesa.visualization.ModularServer(
    Fireflies_FlashingModel,
    [canvas_element, chart_element],
    "Fireflies-Flashing",
    model_kwargs,
)
