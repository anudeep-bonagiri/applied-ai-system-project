# Recommender System Reflection

## Evaluation Comparisons

When comparing **High-Energy Pop** and the **Chill Lofi Study** profiles:
- The top recommendation for High-Energy Pop is "Sunrise City" (Pop, Happy, High Energy), whereas for Chill Lofi it flips entirely to "Focus Flow" (Lofi, Focused, Low Energy). 
- **Why it makes sense:** This demonstrates the mathematical success of our numerical system. The genre and mood differences trigger completely different base pools, and the massive target energy difference (+0.8 vs +0.3) forces the algorithm to penalize energetic pop songs when looking for chill study tracks. 

When comparing **Intense Workout Rock** and the **Adversarial (Conflicting)** profile:
- The top recommendation for Intense Workout Rock is "Storm Runner" (Rock, Intense, 0.91 Energy). For the adversarial classical-yet-high-energy profile, the top recommendation is "Symphony No 9" (Classical, Intense, 0.70 Energy).
- **Why it makes sense:** The adversarial profile preferred "classical" music with almost maximum energy (0.99). Symphony No 9 was picked first solely because the massive +2.0 and +1.0 rewards for matching its genre ("classical") and mood outmatched the heavy penalty it received for having lower relative energy than a rock or EDM track. This perfectly isolates what a 'filter bubble' looks like; it would rather give the user a slow song of the exact desired genre than a fast song from an adjacent genre.
