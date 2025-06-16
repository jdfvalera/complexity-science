## Skill Diffusion and Learning Networks in Shibari: An Agent-Based Model

### Project Summary

This project simulates how technical skill in *shibari* (Japanese rope bondage) spreads through a community of practitioners over time. Using an agent-based model built in using Mesa, the simulation explores how rope tops and bottoms improve their skills through direct practice, social learning, and feedback from partners and peers. The model draws on concepts from complexity science, including diffusion dynamics, learning networks, and reputation-based trust systems.

### Research Question

**How do individual and network-level learning mechanisms affect the diffusion of skill in a shibari community?**

Sub-questions include:

* What role does practice versus peer learning play in skill acquisition?
* How does network structure affect the emergence of expert clusters?
* How does trust (modeled via reputation) influence who learns from whom?

### Model Overview

#### Agents

* **Tops** and **bottoms**: Each agent is assigned one of two roles.
* Attributes:

  * `skill-level` (0–10): Increases through practice or social learning.
  * `learning-rate`: A personal coefficient for how fast the agent learns.
  * `reputation`: Increases with successful scenes; influences peer trust.
  * `connections`: A social network of other agents from whom they can learn.

#### Environment

* No spatial constraints; interactions are driven by random pairing and network links.

#### Time Step Dynamics

Each tick includes:

1. **Scene Simulation**: Random top-bottom pairs attempt a scene. Success depends on skill levels. Both gain a small skill boost from practice.
2. **Feedback Loop**: Scene outcome affects agents’ reputations.
3. **Social Learning**: Agents observe or learn from more skilled, reputable peers in their network and adjust their own skill accordingly.

### Data & Metrics

The model tracks:

* Average and distribution of skill over time
* Reputation vs. skill correlation
* Skill Gini coefficient (inequality of expertise)
* Clustering of high-skill individuals in the network

Optional visual outputs:

* Color-coded agents by skill level
* Skill heatmap over time
* Interactive trust/learning network

### Complexity Concepts

* **Emergence**: Expert clusters and uneven skill distributions arise from simple learning rules.
* **Adaptation**: Agents improve dynamically in response to both direct and social experience.
* **Network Effects**: Structure of learning connections influences the speed and direction of diffusion.
* **Feedback and Nonlinearity**: Scene outcomes recursively shape future learning paths via reputation.

### Why It’s Interesting

Shibari is a rich microcosm of embodied knowledge transmission, consent negotiation, and community trust. This model highlights how informal education, mentorship, and experiential learning scale over time in tightly interconnected communities. The framework is extensible to other domains where skill and trust co-evolve, such as martial arts, performance arts, or even professional training networks.
