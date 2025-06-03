from mesa.discrete_space import CellAgent


class Practitioner(CellAgent):

    def __init__(self, model, learning_rate, skill_decay, rep_delta, bias_rate):
        """Create a new agent.

        Args:
            model (Model): The model instance that contains the agent
        """
        super().__init__(model)
        self.top_skill = 1.0  # Initialize with small random skill
        self.bottom_skill = 1.0 # Initialize with small random skill
        # self.role_bias = self.random.uniform(0, 1)
        self.role_bias = 0.5
        self.reputation = 1.0
        self.role_in_scene = None
        self.learning_rate = learning_rate
        self.skill_decay = skill_decay
        self.rep_delta = rep_delta
        self.bias_rate = bias_rate


    def compatibility_check(self, partner):
        """Check if the agent is compatible with a partner based on role bias."""
        # Calculate compatibility probability based on role_bias difference
        bias_diff = abs(self.role_bias - partner.role_bias)
        # Base compatibility: higher for larger bias differences, but Switches (mid-range) are versatile
        compatibility_prob = 0.5 + 0.5 * bias_diff  # Ranges from 0.5 to 1.0
        # Switches (0.33 <= role_bias <= 0.67) have a compatibility bonus
        if 0.33 <= self.role_bias <= 0.67 or 0.33 <= partner.role_bias <= 0.67:
            compatibility_prob = min(1.0, compatibility_prob + 0.2)
        return self.random.random() < compatibility_prob

    def assign_roles(self, partner):
        """Assign roles (top or bottom) probabilistically based on role bias."""
        # Relative preference for topping (higher role_bias prefers top)
        relative_bias = self.role_bias - partner.role_bias
        # Probability that self takes the top role
        top_prob = 0.5 + 0.3 * relative_bias  # Scales from 0.2 to 0.8 based on bias difference
        top_prob = max(0.2, min(0.8, top_prob))  # Ensure some chance of role reversal
        if self.random.random() < top_prob:
            self.role_in_scene = "top"
            partner.role_in_scene = "bottom"
        else:
            self.role_in_scene = "bottom"
            partner.role_in_scene = "top"

    def is_scene_successful(self, partner):
        """Determine scene success based on combined skills, capped at 85%."""
        if self.role_in_scene == 'top':
            total_skill = self.top_skill + partner.bottom_skill
        else:
            total_skill = self.bottom_skill + partner.top_skill
        # Base success probability: 70% to 85% based on skills
        success_prob = min(0.85, 0.7 + 0.2 * (total_skill / 20))
        # Small bonus if roles align with preferences (e.g., high role_bias prefers top)
        role_alignment = 1.0 if (
            (self.role_in_scene == "top" and self.role_bias > 0.67) or
            (self.role_in_scene == "bottom" and self.role_bias < 0.33)
        ) else 0.99
        success_prob *= role_alignment
        return self.random.random() < success_prob

    def practice_skill(self, partner, success):
        """Update skills and reputation based on scene success."""
        neighbors = [agent for agent in self.cell.neighborhood.agents if agent != self]
        learning_rate = self.learning_rate if success else self.learning_rate / 4  # 1/4 for failure
        rep_delta = self.rep_delta if success else -self.rep_delta*2  # negative for failure
        skill_decay = self.skill_decay

        if len(neighbors) > 0:
            if self.role_in_scene == 'top':
                diff = partner.bottom_skill / 20
                growth = (learning_rate * diff + 0.03) * (12 - self.top_skill) / 10
                self.top_skill += growth
                self.top_skill = max(0, min(10, self.top_skill))
                self.bottom_skill = max(0, min(10, self.bottom_skill - skill_decay))  # Decay only bottom_skill
            else:
                diff = partner.top_skill / 20
                growth = (learning_rate * diff + 0.03) * (12 - self.bottom_skill) / 10
                self.bottom_skill += growth
                self.bottom_skill = max(0, min(10, self.bottom_skill))
                self.top_skill = max(0, min(10, self.top_skill - skill_decay))  # Decay only top_skill

            self.reputation = max(0, min(10, self.reputation + rep_delta))
            partner.reputation = max(0, min(10, partner.reputation + rep_delta))
        else:
            self.reputation = max(0, min(10, self.reputation - rep_delta))
            partner.reputation = max(0, min(10, partner.reputation - rep_delta))
            
        if success:
            if self.role_in_scene == "top":
                self.role_bias *= (1+self.bias_rate)    # Move bias toward 1
            elif self.role_in_scene == "bottom":
                self.role_bias *= (1-self.bias_rate)    # Move bias toward 0
        else:
            if self.role_in_scene == "top":
                self.role_bias *= (1-self.bias_rate)
            elif self.role_in_scene == "bottom":
                self.role_bias *= (1+self.bias_rate)

        # Keep it within [0, 1]
        self.role_bias = max(0, min(1, self.role_bias))

    def step(self):
        """Agent's step method: move to an empty neighbor and practice with a partner if available."""
        # Move to a random empty neighbor, if available
        empty_neighbors = [cell for cell in self.cell.neighborhood if cell.is_empty]
        if empty_neighbors:
            self.cell = self.random.choice(empty_neighbors)

        # Find a partner to practice with
        neighbors = [agent for agent in self.cell.neighborhood.agents if agent != self]
        if neighbors:
            # Prefer agents with higher reputation
            weights = [max(agent.reputation, 0.01) for agent in neighbors]  # Avoid zero weight
            partner = self.random.choices(neighbors, weights=weights, k=1)[0]
            if self.compatibility_check(partner):
                self.assign_roles(partner)
                success = self.is_scene_successful(partner)
                self.practice_skill(partner, success)