# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version of the music recommender simulates content-based filtering by comparing the user's specific feature preferences (like genre, mood, and energy) with the attributes of songs in our catalog. By scoring each song according to how closely it matches a target "taste profile", we generate tailored song suggestions and transparently explain why each song was chosen.

---

## How The System Works

The recommendation engine functions as a weighted point system. Every track in the `data/songs.csv` catalog is given points based on its similarity to the target `UserProfile`.
- **Features Used:** `genre` (string), `mood` (string), `energy` (float 0.0-1.0).
- **Scoring Recipe:**
  - **Genre Match:** +2.0 points if the song's genre perfectly matches the user profile's target genre.
  - **Mood Match:** +1.0 point if the song's mood matches the user profile's target mood.
  - **Energy Proximity:** Up to +1.0 point based on how close the song's energy is to the user's target energy. The difference is subtracted from 1.0. The closer the energy level, the higher the score.
  
The model assesses every song individually, compiles the scores, and sorts the list in descending order to output the Top N suggestions.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

- **Conflicting Profiles:** I created an adversarial user profile that liked "classical" genre but had an intensely high target "energy" of 0.99. Interestingly, "Symphony No 9 by Beethoven" was ranked first because of the heavy genre score weight (+2.0 points), despite having an energy penalty compared to some electronic/dance songs.
- **Varying Energy Targets:** When lowering target energy, the recommender beautifully shifted towards acoustic, ambient, or chill songs, demonstrating that numerical features are critical to balancing the binary genre/mood matches.

---

## Limitations and Risks

- **Filter Bubbles & Exploration:** Due to the strict weighting system giving heavy importance to genre (+2.0), the model is trapped inside "filter bubbles". It rarely suggests high-quality tracks that match the vibe/mood but are cataloged under a slightly differing genre.
- **Sparse Options:** We are only using a catalog of 18 songs, making it difficult to generate highly diverse recommendations.
- **Subjective Categorization:** The static `mood` field is subjective and cannot adequately capture hybrid feelings that a real user experiences.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Through this project, I realized how data is seamlessly translated into algorithmic predictions with just arithmetic. Designing the weights (+2 for genre vs +1 for mood) forced me to acknowledge that an algorithm's output relies entirely on the human assumptions injected into those parameters.

I also saw firsthand how easily a predictive system can form biases or "filter bubles". By weighting genre heavily, I noticed that certain high-energy pop enthusiasts missed out on intense rock songs or EDM songs that matched their energy target perfectly, all because the exact genre string didn't align. This illustrates that real recommendation algorithms (like those on TikTok or Spotify) must balance historical matching with "unknown exploration" in order to properly build an open, fair, and diverse content ecosystem.
