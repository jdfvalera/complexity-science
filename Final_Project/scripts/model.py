import networkx as nx
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import Network
import numpy as np
import matplotlib.pyplot as plt
from agent import Practitioner

class SceneModel(Model):
    """A model with some number of agents."""

    def __init__(self, n=30, num_nodes=40, seed=None, learning_rate=0.2, skill_decay=0.05, rep_delta=0.2, bias_rate=0.02):
        super().__init__(seed=seed)

        self.num_agents = n
        self.num_nodes = num_nodes if num_nodes >= self.num_agents else self.num_agents
        # self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=0.5)
        self.G = nx.watts_strogatz_graph(n=self.num_nodes, k=4, p=0.1)
        self.grid = Network(self.G, capacity=1, random=self.random)

        # Set up data collection
        self.datacollector = DataCollector(
            agent_reporters={
                "TopSkill": lambda a: a.top_skill,
                "BottomSkill": lambda a: a.bottom_skill,
                "Reputation": lambda a: a.reputation,
                "RoleBias": lambda a: a.role_bias,
                "RoleCategory": lambda a: ("Bottom" if a.role_bias < 0.33 else "Switch" if a.role_bias <= 0.67 else "Top")
            },
            model_reporters={
                "AvgTopSkill": lambda m: np.mean([a.top_skill for a in m.agents]),
                "AvgBottomSkill": lambda m: np.mean([a.bottom_skill for a in m.agents]),
                "AvgReputation": lambda m: np.mean([a.reputation for a in m.agents]),
                "AvgTopSkillBottoms": lambda m: np.mean([a.top_skill for a in m.agents if a.role_bias < 0.33]) if any(a.role_bias < 0.33 for a in m.agents) else 0,
                "AvgTopSkillSwitches": lambda m: np.mean([a.top_skill for a in m.agents if 0.33 <= a.role_bias <= 0.67]) if any(0.33 <= a.role_bias <= 0.67 for a in m.agents) else 0,
                "AvgTopSkillTops": lambda m: np.mean([a.top_skill for a in m.agents if a.role_bias > 0.67]) if any(a.role_bias > 0.67 for a in m.agents) else 0,
                "AvgBottomSkillBottoms": lambda m: np.mean([a.bottom_skill for a in m.agents if a.role_bias < 0.33]) if any(a.role_bias < 0.33 for a in m.agents) else 0,
                "AvgBottomSkillSwitches": lambda m: np.mean([a.bottom_skill for a in m.agents if 0.33 <= a.role_bias <= 0.67]) if any(0.33 <= a.role_bias <= 0.67 for a in m.agents) else 0,
                "AvgBottomSkillTops": lambda m: np.mean([a.bottom_skill for a in m.agents if a.role_bias > 0.67]) if any(a.role_bias > 0.67 for a in m.agents) else 0,
                "AvgReputationBottoms": lambda m: np.mean([a.reputation for a in m.agents if a.role_bias < 0.33]) if any(a.role_bias < 0.33 for a in m.agents) else 0,
                "AvgReputationSwitches": lambda m: np.mean([a.reputation for a in m.agents if 0.33 <= a.role_bias <= 0.67]) if any(0.33 <= a.role_bias <= 0.67 for a in m.agents) else 0,
                "AvgReputationTops": lambda m: np.mean([a.reputation for a in m.agents if a.role_bias > 0.67]) if any(a.role_bias > 0.67 for a in m.agents) else 0,
                "NumBottoms": lambda m: sum(1 for a in m.agents if a.role_bias < 0.33),
                "NumSwitches": lambda m: sum(1 for a in m.agents if 0.33 <= a.role_bias <= 0.67),
                "NumTops": lambda m: sum(1 for a in m.agents if a.role_bias > 0.67),
            }
        )

        # Create agents; add the agent to a random node
        # TODO: change to MoneyAgent.create_agents(...)
        list_of_random_nodes = self.random.sample(list(self.G), self.num_agents)
        for position in list_of_random_nodes:
            agent = Practitioner(self, learning_rate, skill_decay, rep_delta, bias_rate)
            agent.move_to(self.grid[position])

        self.running = True
        self.datacollector.collect(self)
        

    def step(self):
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.datacollector.collect(self)  # collect data