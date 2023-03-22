"""
Configure visualization elements and instantiate a server
"""

from .model import Fireflies_FlashingModel, Firefly  # noqa

from .SimpleContinuousModule import SimpleCanvas


import mesa

def firefly_flashing_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {} # remove it ?

    if type(agent) is Firefly:
        portrayal['Shape'] = "circle"
        portrayal["Filled"] = "true",
        portrayal["Layer"] = 0,
        portrayal["r"] = 0.5,
        if agent.is_flashing:
            portrayal = {
                "Shape": "circle",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5,
                "Color": "Yellow",
            }
        else:
            # portrayal["Color"] = "Grey"

            portrayal = {
                "Shape": "circle",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5,
                "Color": "Grey",
            }

        return portrayal
    else:
        raise TypeError

"""
canvas_element = mesa.visualization.CanvasGrid(
    firefly_flashing_portrayal, 20, 20, 500, 500
)
"""
canvas_element = SimpleCanvas(firefly_flashing_portrayal, 500, 500)


chart_element = mesa.visualization.ChartModule([{"Label": "Fireflies-Flashing", "Color": "Yellow"}])

model_kwargs = {
    "title": mesa.visualization.StaticText("Parameters:"),
    "num_agents": mesa.visualization.Slider("Fireflies number", 100, 1, 200),
    "cycle_length": mesa.visualization.Slider("Cycle length", 10, 5, 100),
    "width": 20, 
    "height": 20}

server = mesa.visualization.ModularServer(
    Fireflies_FlashingModel,
    [canvas_element, chart_element],
    "Fireflies-Flashing",
    model_kwargs,
)
