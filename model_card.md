# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**  

---

## 2. Intended Use  

This recommender model is designed to suggest 5 relevant songs from a small predefined catalog based on a user's defined "taste profile". It assumes the user explicitly knows and states their desired genre, mood, and energy level. This model is purely for educational classroom exploration, and is not equipped or scaled for real users or live production environments.

---

## 3. How the Model Works  

VibeFinder ranks tracks sequentially via a simple content-based point system.
- It considers the track's **genre**, **mood**, and numerical **energy level**.
- The `UserProfile` contains the user's specific ideal targets for these same features.
- The scoring logic acts like a checklist: +2.0 points for a matching genre, +1.0 for a matching mood, and up to +1.0 points based on the mathematical proximity of the song's energy rating to the user's desired energy rating.
- The output ranks the total sums from highest to lowest and returns an explanation. 

---

## 4. Data  

VibeFinder operates on a microscopic dataset.
- There are **18 total songs** currently in `data/songs.csv`.
- I added 8 tracks to provide additional variety (e.g., adding Classical, Country, R&B, and EDM).
- The dataset leans heavily toward popular mainstream niches (Pop, LoFi, Rock), and leaves out vast majorities of world music, spoken text, classical subdivisions, and avant-garde catalogs.

---

## 5. Strengths  

- Complete transparency: Because the scoring logic is simple addition, developers and users can see exactly *why* a track is suggested.
- Excels at clearly partitioned musical domains (e.g., Chill lofi vs Intense rock).
- Numerical weighting successfully penalizes tracks that deviate far from desired energy thresholds.

---

## 6. Limitations and Bias 

- **Overpowering weights:** By giving genre +2.0 points, the model risks locking users into "filter bubbles", over-prioritizing genre matching rather than capturing the actual 'feel' of the music in other cross-genres.
- **Categorical rigidness:** Moods and genres are hard-coded strings. A song labeled "indie folk" will not match a profile wanting "folk", even if they acoustically sound identical. This leads to rigid, occasionally unfair exclusions.
- **No collaborative signals:** It ignores completely what other users with similar tastes are listening to.

---

## 7. Evaluation  

I conducted tests passing in different hypothetical user profiles defined manually in `src/main.py`.
- Tested profiles included `High-Energy Pop`, `Chill Lofi Study`, `Intense Workout Rock`, and an `Adversarial` profile.
- I checked if the absolute nearest matches appeared at the top. The results were generally accurate.
- I was surprised to find that for the adversarial profile (classical genre + maximum energy), the classical song was still placed first despite being very low energy. This clearly visualized how genre heavily dominated the scoring metric.

---

## 8. Future Work  

If I were to continue developing this model, I would:
- Integrate a partial-matching string comparison for genres (e.g. mapping subgenres to broader parents).
- Blend this content-based approach with simple collaborative filtering (incorporating other users' skip/play histories) to add unpredictability.
- Introduce continuous values for mood instead of static labels (e.g., a sadness vs happiness scale) to yield more fluid matches.

---

## 9. Personal Reflection  

Building this simulation demystified the 'magic' of suggestion engines; I saw firsthand that 'bias' in AI often originates from simple arithmetic decisions made by a developer, such as deciding that genre is inherently twice as important as mood. This radically transformed the way I think about platforms like Spotify and YouTube. Even in algorithms that utilize deep learning or vector dimensions, human judgment continues to matter when defining which metrics truly quantify "success" or "similarity". In the future, I will view all suggestions with a critical lens, recognizing they are the mathematically weighted constraints of a larger design vision.
