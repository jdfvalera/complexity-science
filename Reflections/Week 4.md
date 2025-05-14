### Week 4 Reflection: Cellular Automata and Agent-Based Models

## Intro

Week 4 was a bit of a wild card for me since I had to join the class online, thanks to some routine lab tests eating up my morning. No 9am Aboitiz Tech Space vibes this time, just me and my laptop at the halls of Makati MEdical Center. Haha. After the chaos theory and information theory highs of the past weeks, I was intrigued by new concepts on cellular automata (CA) and agent-based models (ABM).

## Takeaways

This week was all about modeling complex systems with CA and ABM, and it felt like we were handed the keys to create mini-worlds. Cellular automata are these grid-based systems where cells follow simple rules based on their neighbors, which leads to crazy emergent patterns. Think Conway’s Game of Life, where cells live, die, or multiply based on neighbor counts, creating still lifes, oscillators, or even “spaceships” gliding across the grid. It’s wild how simple rules can spawn such intricate behavior on a pixel grid. But as a gamer who loved grid-based games, it was not all new to me. It just got more academic, I guess.

ABM, on the other hand, is like CA’s cooler, more flexible cousin. Instead of rigid grids, you’ve got individual agents that make decisions based on their own rules and interactions. The ant foraging model was so fun to watch! One ant finds food, leaves a pheromone trail, and suddenly you’ve got a whole colony organizing into a food-hauling superhighway.
The lecture also compared CA and ABM. CA is great for spatial stuff and easy to code, but it’s limited when you need complex individual behaviors. ABM can handle that complexity but gets computationally heavy. It’s like choosing between a quick sketch (CA) or a full-on 3D render (ABM) for your system.

## Highlight

Hands-down, my favorite moment was when we discussed lattice structures for CA, and I got to chime in about hexagonal lattices. Gamer nerd activated! I argued they’re better for games because they allow smoother character movement compared to clunky square grids. In a square lattice, you’re stuck with 4 (or 8 if you count the clunky diagonals) directions, but hexagons give you 6, making paths feel more natural—like how characters dodge or chase in strategy games. Hexagonal lattices also popped up in the notes for their use in 2D models, and I’m obsessed with how they balance simplicity and flexibility. I’m already thinking about coding a hex-based CA for a game or simulation, but maybe when I have the time!

Another gem was the slide on ABM challenges: “The best thing about agent-based modeling is that you can make anything you want happen. The worst thing is you can make anything you want happen.” I laughed out loud because it’s so true. We’re basically playing god with these models! It’s thrilling to design agents and watch patterns emerge, but it’s also a trap. If you’re not careful, you’re just forcing the system to do what you want, not what it naturally would. That “Garbage In, Garbage Out” warning hit hard, and it’s got me thinking about how to keep my models honest.

## Other Thoughts

As usual, my brain’s buzzing with connections to road safety and the kink community (I really feel like I really wanna do this as a final project). For road safety, I’m picturing a CA model with a hexagonal lattice to simulate traffic flow at an intersection or any other bottlenecks on the road. Each cell could represent a vehicle or pedestrian, with rules for speed, braking, or yielding. A hex grid would make movements more realistic, capturing diagonal swerves or merges that square grids miss. I’m curious if I could tweak the rules to spot crash-prone patterns and suggest safer road designs.

The kink community angle is trickier but so juicy. ABM feels perfect here: each person’s an agent with rules about consent, roles, or safety, interacting in a social “environment.” The emergent behavior could be a subculture, like a new scene forming from a few pioneers. The “playing god” problem resonates too—if I model this wrong, I might accidentally bake in my biases about how these communities work. I’d need real-world data, maybe from forums or events, to keep it legit, but thankfully a simulation is enought for the final project here. Haha.


## Conclusion
Week 4 was alright. CA and ABM are like cheat codes for understanding complexity, turning simple rules into mind-bending patterns. The hexagonal lattice love and the “playing god” warning with ABM got my gamer nerd heart racing to experiment with simulations. Week 5 will most probably be a continuation of this topic becasue we ahve yet to work on a Jupyter notebook!