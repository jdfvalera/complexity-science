from agent import Practitioner
from model import SceneModel

from mesa.visualization import SolaraViz, make_space_component
from mesa.visualization.utils import update_counter
from matplotlib.figure import Figure
import solara

def agent_portrayal(agent):
    # Assign colors and labels based on role category
    if agent.role_bias < 0.33:
        color = "blue"  # Bottoms
    elif 0.33 <= agent.role_bias <= 0.67:
        color = "green"  # Switches
    else:
        color = "red"    # Tops
    
    # Use a very small node size to emphasize labels
    size = 70 # Small size to make nodes nearly invisible
    
    return {
        "color": color,
        "size": size,
    }


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random seed",
    },
    "n": {
        "type": "SliderInt",
        "value": 30,
        "label": "Number of agents",
        "min": 2,
        "max": 100,
        "step": 1,
        "description": "Choose how many agents to include in the model",
    },
    "num_nodes": {
        "type": "SliderInt",
        "value": 40,
        "label": "Number of nodes",
        "min": 3,
        "max": 200,
        "step": 1,
        "description": "Choose how many nodes to include in the model, with at least the same number of agents",
    },
    "learning_rate": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Learning Rate",
        "min": 0.05,
        "max": 0.5,
        "step": 0.05,
        "description": "Rate at which skills improve during successful scenes",
    },
    "skill_decay": {
        "type": "SliderFloat",
        "value": 0.05,
        "label": "Skill Decay",
        "min": 0.0,
        "max": 0.1,
        "step": 0.01,
        "description": "Rate at which unused skills decay",
    },
    "rep_delta": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Reputation Change",
        "min": 0.05,
        "max": 0.5,
        "step": 0.05,
        "description": "Change in reputation for successful/failed scenes",
    },
    "bias_rate": {
        "type": "SliderFloat",
        "value": 0.01,
        "label": "Bias Change Rate",
        "min": 0.0,
        "max": 0.2,
        "step": 0.01,
        "description": "Rate at which the bias towards a role changes after a successful/failed scene"
    }
}


def post_process(ax):
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color="w", markerfacecolor='blue', markersize=8, label="Bottom"),
        Line2D([0], [0], marker='o', color="w", markerfacecolor='green', markersize=8, label="Switch"),
        Line2D([0], [0], marker='o', color="w", markerfacecolor='red', markersize=8, label="Top"),
    ]
    ax.legend(handles=legend_elements, title="Role Category", loc="upper right")
    # Adjust label font size to ensure readability
    ax.set_xlabel("Network Graph (B=Bottoms, S=Switches, T=Tops)", fontsize=10)
    # Optional: Adjust node label font size
    for text in ax.texts:
        text.set_fontsize(12)


SpaceGraph = make_space_component(
    agent_portrayal, cmap=None, post_process=post_process
)
    
@solara.component
def Histogram(model):
    update_counter.get()  # This is required to update the counter
    fig = Figure(figsize=(12, 12))
    axes = fig.subplots(3, 1)

    # Top Skill Histogram
    bottoms_top = [a.top_skill for a in model.agents if a.role_bias < 0.33]
    switches_top = [a.top_skill for a in model.agents if 0.33 <= a.role_bias <= 0.67]
    tops_top = [a.top_skill for a in model.agents if a.role_bias > 0.67]
    if bottoms_top:
        axes[0].hist(bottoms_top, bins=20, range=(0, 10), alpha=0.5, label="Bottoms", color="blue")
    if switches_top:
        axes[0].hist(switches_top, bins=20, range=(0, 10), alpha=0.5, label="Switches", color="green")
    if tops_top:
        axes[0].hist(tops_top, bins=20, range=(0, 10), alpha=0.5, label="Tops", color="red")
    axes[0].set_xlabel("Top Skill")
    axes[0].set_ylabel("Number of Agents")
    axes[0].set_title("Top Skill Distribution by Role Category")
    axes[0].legend()

    # Bottom Skill Histogram
    bottoms_bottom = [a.bottom_skill for a in model.agents if a.role_bias < 0.33]
    switches_bottom = [a.bottom_skill for a in model.agents if 0.33 <= a.role_bias <= 0.67]
    tops_bottom = [a.bottom_skill for a in model.agents if a.role_bias > 0.67]
    if bottoms_bottom:
        axes[1].hist(bottoms_bottom, bins=20, range=(0, 10), alpha=0.5, label="Bottoms", color="blue")
    if switches_bottom:
        axes[1].hist(switches_bottom, bins=20, range=(0, 10), alpha=0.5, label="Switches", color="green")
    if tops_bottom:
        axes[1].hist(tops_bottom, bins=20, range=(0, 10), alpha=0.5, label="Tops", color="red")
    axes[1].set_xlabel("Bottom Skill")
    axes[1].set_ylabel("Number of Agents")
    axes[1].set_title("Bottom Skill Distribution by Role Category")
    axes[1].legend()
    
    # Reputation Histogram
    bottoms_rep = [a.reputation for a in model.agents if a.role_bias < 0.33]
    switches_rep = [a.reputation for a in model.agents if 0.33 <= a.role_bias <= 0.67]
    tops_rep = [a.reputation for a in model.agents if a.role_bias > 0.67]
    if bottoms_rep:
        axes[2].hist(bottoms_rep, bins=20, range=(0, 10), alpha=0.5, label="Bottoms", color="blue")
    if switches_rep:
        axes[2].hist(switches_rep, bins=20, range=(0, 10), alpha=0.5, label="Switches", color="green")
    if tops_rep:
        axes[2].hist(tops_rep, bins=20, range=(0, 10), alpha=0.5, label="Tops", color="red")
    axes[2].set_xlabel("Reputation")
    axes[2].set_ylabel("Number of Agents")
    axes[2].set_title("Reputation Distribution by Role Category")
    axes[2].legend()
    
    fig.tight_layout()
    solara.FigureMatplotlib(fig)
    
@solara.component
def TimeSeries(model):
    update_counter.get()
    data = model.datacollector.get_model_vars_dataframe()
    
    fig = Figure(figsize=(10, 4))
    ax = fig.subplots()

    ax.plot(data["AvgTopSkill"], label="Avg Top Skill", color="red")
    ax.plot(data["AvgBottomSkill"], label="Avg Bottom Skill", color="blue")
    ax.set_xlabel("Step")
    ax.set_ylabel("Skill")
    ax.set_title("Skill Evolution Over Time")
    ax.legend()
    solara.FigureMatplotlib(fig)

@solara.component
def RoleDistributionNumbers(model):
    update_counter.get()
    model_data = model.datacollector.get_model_vars_dataframe()

    if model_data.empty:
        return solara.Text("No data yet.")

    latest = model_data.iloc[-1]
    bottoms = latest["NumBottoms"]
    switches = latest["NumSwitches"]
    tops = latest["NumTops"]

    with solara.Row(style={"justifyContent": "space-around", "padding": "20px"}):
        with solara.Column(style={"alignItems": "center"}):
            solara.Text("Bottoms", style={"fontSize": "18px", "color":"#0000FF"})
            solara.Text(f"{bottoms}", style={"fontSize": "36px", "fontWeight": "bold"})
        with solara.Column(style={"alignItems": "center"}):
            solara.Text("Switches", style={"fontSize": "18px", "color": "#00FF00"})
            solara.Text(f"{switches}", style={"fontSize": "36px", "fontWeight": "bold"})
        with solara.Column(style={"alignItems": "center"}):
            solara.Text("Tops", style={"fontSize": "18px", "color": "#FF0000"})
            solara.Text(f"{tops}", style={"fontSize": "36px", "fontWeight": "bold"})
    
def create_page():
    model = SceneModel()
    return SolaraViz(
        model=model,
        components=[SpaceGraph, Histogram, TimeSeries, RoleDistributionNumbers],
        model_params=model_params,
        name="Shibari Skill Diffusion Simulation Model: Scene Network",
    )