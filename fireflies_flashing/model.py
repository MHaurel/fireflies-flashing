import mesa
from fireflies_flashing.random_walk import RandomWalker
from fireflies_flashing.scheduler import RandomActivationByTypeFiltered

import random

class Firefly(mesa.Agent):  # noqa
    """
    An firefly that walks randomly, flashing at the end of its cycle.
    """

    def __init__(self, unique_id, pos, model, moore, cycle_length):
        """
        Customize the agent
        """
        self.unique_id = unique_id
        self.cycle_length = cycle_length
        self.current_value_cycle = random.randrange(self.cycle_length)
        self.is_flashing = False
        if self.current_value_cycle == self.cycle_length:
            self.is_flashing = True
        super().__init__(unique_id, model)

    def step(self):
        """
        Modify this method to change what an individual agent will do during each step.
        Can include logic based on neighbors states.
        """
        self.current_value_cycle += 1 # Incrementing the clock
        if self.current_value_cycle == self.cycle_length: # If the clock reaches the maximum
            self.is_flashing = True # The firefly flashes
            self.current_value_cycle = 0 # Reseting the clock
        else:
            self.is_flashing = False # Else, doesn't flash


        neighbors = self.model.space.get_neighbors(self.pos, radius=100, include_center=True)
        for agent in neighbors:
            if agent.is_flashing: 
                self.current_value_cycle = 0

        # self.random_move() # Random move
        self.move()

    def move(self):
        #neighbors = self.model.space.get_neighbors(self.pos, 2, False)
        self.velocity = 2
        self.speed = 2
        new_pos_x = self.pos[0] + self.velocity * self.speed
        new_pos_y = self.pos[1] + self.velocity * self.speed
        self.model.space.move_agent(self, (new_pos_x, new_pos_y))


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
        # self.schedule = mesa.time.RandomActivation(self)
        self.schedule = RandomActivationByTypeFiltered(self)
        # self.grid = mesa.space.MultiGrid(width=width, height=height, torus=True)
        self.space = mesa.space.ContinuousSpace(width, height, True)

        for i in range(self.num_agents):
            # x = self.random.randrange(self.grid.width) 
            # y = self.random.randrange(self.grid.height)
            # x = self.random.randrange(0, self.space.width)
            # y = self.random.randrange(0, self.space.height)
            x = round(self.random.uniform(0, self.space.width), 1)
            y = round(self.random.uniform(0, self.space.height), 1)
            agent = Firefly(unique_id=i, pos=(x, y), model=self, moore=True, cycle_length=cycle_length)
            # self.grid.place_agent(agent, (x, y))
            self.space.place_agent(agent, (x, y))
            self.schedule.add(agent)

        # example data collector
        self.datacollector = mesa.DataCollector({
            'Fireflies-Flashing' : lambda m: m.schedule.get_type_count(
                Firefly, lambda x: x.is_flashing
            ) 
        })
        

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.datacollector.collect(self)
        self.schedule.step()




    
