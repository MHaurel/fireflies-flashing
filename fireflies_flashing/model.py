import mesa
from fireflies_flashing.random_walk import RandomWalker


class Firefly(RandomWalker):  # noqa
    """
    An firefly that walks randomly, flashing at the end of its cycle.
    """

    def __init__(self, unique_id, pos, model, moore):
        """
        Customize the agent
        """
        self.unique_id = unique_id
        self.is_flashing = True # TODO : random ? (change by implementing clock)
        super().__init__(unique_id, pos, model, moore)

    def step(self):
        """
        Modify this method to change what an individual agent will do during each step.
        Can include logic based on neighbors states.
        """
        self.random_move()
        pass


class Fireflies_FlashingModel(mesa.Model):
    """
    The model class holds the model-level attributes, manages the agents, and generally handles
    the global level of our model.

    There is only one model-level parameter: how many agents the model contains. When a new model
    is started, we want it to populate itself with the given number of agents.

    The scheduler is a special model component which controls the order in which agents are activated.
    """

    def __init__(self, num_agents, cycle_length, width, height):
        super().__init__()
        self.num_agents = num_agents
        self.cycle_length = cycle_length
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=True)

        for i in range(self.num_agents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            agent = Firefly(unique_id=i, pos=(x, y), model=self, moore=True)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        # example data collector
        self.datacollector = mesa.datacollection.DataCollector()

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.datacollector.collect(self)
        self.schedule.step()
