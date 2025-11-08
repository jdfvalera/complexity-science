# Shibari Skill Diffusion Simulation Model

This project simulates how practitioners in a social network develop and exchange skills, reputation, and role preferences through repeated interactions. It uses an **agent-based model (ABM)** built on the [Mesa](https://mesa.readthedocs.io/) framework and visualized with [Solara](https://solara.dev/).

Each agent represents a practitioner who learns, practices, and adapts their style (top, bottom, or switch) through scenes with others. Over time, the population evolves in terms of skill distribution, reputation, and role bias.

---

## Project Structure

```
Final_Project/
└── scripts/
    ├── agent.py         # Defines Practitioner agents and their behavioral logic
    ├── model.py         # Defines the Mesa model and handles simulation steps and data collection
    ├── model_viz.py     # Builds the Solara-based visualization interface for simulation results
    └── app.py           # Launches the visualization dashboard
```

---

## Core Components

### **1. agent.py**
Defines the `Practitioner` class, extending Mesa’s `CellAgent`.
Agents have attributes such as:
- `top_skill`, `bottom_skill`: proficiency levels for each role
- `reputation`: social standing within the network
- `role_bias`: preference for topping or bottoming (0 = bottom, 1 = top)

Agents:
- Check compatibility with partners
- Assign roles probabilistically based on bias
- Determine success probability for a scene
- Update skills, reputation, and bias dynamically after each scene

### **2. model.py**
Implements the `SceneModel` class, a subclass of `mesa.Model`.
It initializes a small-world network (Watts-Strogatz) where agents interact.

Tracks metrics using a `DataCollector`:
- Average skills and reputation across all agents and by role category
- Counts of Bottoms, Switches, and Tops

Simulation steps involve agents moving, practicing with partners, and updating state variables.

### **3. model_viz.py**
Defines the Solara visualization interface:
- **Network Graph:** shows agent connections by role category (color-coded)
- **Histograms:** display skill and reputation distributions by role
- **Time Series:** tracks how average skills evolve over time
- **Role Counters:** shows current counts of Bottoms, Switches, and Tops

Includes adjustable parameters:
- Number of agents / nodes
- Learning rate, skill decay, reputation delta, and bias adjustment rate

### **4. app.py**
A minimal launcher that imports and runs the visualization app defined in `model_viz.py`.

---

## ▶Running the Simulation

### **1. Install dependencies**
```bash
pip install mesa solara matplotlib networkx numpy
```

### **2. Launch the app**
From the `Final_Project/scripts` directory:
```bash
solara run app.py
```

The dashboard will open in your browser, allowing you to:
- Adjust parameters
- Step through the simulation
- Observe how roles, skills, and reputations evolve over time

---

## Key Insights
- The simulation explores how **social learning and bias reinforcement** shape role specialization in a skill-sharing community.
- Switches (versatile agents) often facilitate cross-role learning and improve network adaptability.
- Over time, the balance between learning rate and bias rate determines whether the population polarizes into specialized roles.

