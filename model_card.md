# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0** – A simple CLI-first music recommendation engine that matches user preferences (genre, mood, energy) to song recommendations with transparent scoring explanations.

---

## 2. Intended Use  

VibeFinder 1.0 is designed for **classroom exploration and algorithmic learning**, not production deployment. It generates playlist recommendations based on three user preference dimensions: favorite genre, favorite mood, and target energy level. The system assumes users can articulate these three preferences and prioritizes transparency (showing scoring breakdown) over recommendation accuracy. It is intended for students, instructors, and researchers exploring recommendation systems, bias detection, and algorithmic fairness in music discovery.

---

## 3. How the Model Works  

**The Scoring Algorithm:**

VibeFinder uses a **weighted additive scoring model** that evaluates each song across three dimensions:

1. **Genre Match** (+1.0 points): If a song's genre exactly matches the user's favorite genre, it receives 1.0 points. This ensures genre preference is respected as the primary filter.

2. **Mood Match** (+1.0 points): If a song's mood exactly matches the user's favorite mood, it receives 1.0 points. This brings emotional coherence to recommendations.

3. **Energy Similarity** (×2.0 multiplier): The system calculates how close a song's energy level is to the user's target energy using the formula: `energy_score = 2.0 × (1 - |song_energy - target_energy|)`, clamped to [0.0, 2.0]. This gives energy-based matching double the weight compared to individual genre/mood matches, allowing for nuanced "vibe" alignment.

**Maximum Possible Score: 4.0** (1.0 + 1.0 + 2.0)

The top *k* songs are sorted by total score in descending order and returned with transparent reasoning (which factors contributed to their score). This design prioritizes interpretability: users understand *why* a song is recommended, not just that it is.

---

## 4. Data  

**Dataset Summary:**
- **Total Songs:** 11 songs
- **Genres Represented:** 8 unique genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, disco)
- **Genre Distribution (Bias Alert):**
  - Lofi: 3 songs (27%)
  - Pop: 2 songs (18%)  
  - Others: 6 genres with 1 song each (55% total but fragmented)
- **Mood Coverage:** 6 moods (happy, chill, intense, relaxed, moody, focused)
- **Energy Range:** 0.28 (Spacewalk Thoughts) to 0.93 (Gym Hero)

**Notable Data Characteristics:**
The dataset is intentionally small (11 songs) for classroom exploration and is skewed toward Western popular genres (pop, lofi, indie pop). It lacks representation of non-Western genres (classical, K-pop, Afrobeats, reggae, metal), alternative moods (energetic, dark, romantic), and underrepresents niche communities. This limitation is acknowledged as a teaching tool, not a production-ready system.

---

## 5. Strengths  

- **Transparent Scoring:** Users see exact point breakdowns, building trust and understanding.
- **Balanced Energy Matching:** The 2.0x multiplier on energy allows songs to compete on "vibe fit" even if genre doesn't match, reducing recommendation monotony.
- **Graceful Degradation:** If a song lacks a preference dimension, it scores zero on that component but can still rank if it excels on others.
- **Robust Edge Case Handling:** Handles missing data, case-insensitive matching, and extreme energy values without crashing.
- **Clean CLI Output:** Formatted terminal output with ranked recommendations and reasoning is easy to parse.

**Test Results Confirming Strengths:**
- Users with mainstream preferences (pop + happy + 0.8 energy) receive highly relevant recommendations.
- Energy-focused users benefit from the 2.0x multiplier, receiving suggestions based on workout suitability or mood intensity.
- The system correctly surfaces "Gym Hero" (intense pop song) for high-energy seekers despite having "intense" rather than "happy" mood.

---

## 6. Limitations and Bias 

### 🚨 Critical Biases Identified:

**1. Genre-Dominance Bias (Data + Math)**

The dataset is skewed toward **Pop and Lofi** music (45% of catalog), while classical, world music, metal, and other genres are absent. Combined with the +1.0 genre weight (25% of max score), this creates a **"Popularity Bubble"** where mainstream genres always outrank niche alternatives. A user searching for "classical" music receives zero genre matches and falls back to energy-only scoring—potentially recommending upbeat pop songs instead of orchestral pieces.

*Impact:* Users with non-mainstream tastes receive lower-confidence recommendations or irrelevant "best-of-worst" results.

**2. Linear Energy Penalty (Math Bias)**

The energy similarity formula `1 - |diff|` applies **linear penalties** for energy mismatch. A user targeting 0.5 energy will score a 0.4-energy song at 0.90 (great fit) but a 0.2-energy song at 0.70 (acceptable fit). This **penalizes genuinely good songs** if they fall just outside the target range. For example, a song with 0.35 energy that is 100% mood and genre match scores 2.35, while a 0.51-energy song with zero mood/genre match scores 2.00—despite the former being a far better fit.

*Impact:* Users miss high-quality recommendations because the algorithm treats energy as a primary filter instead of a secondary refinement.

**3. Cold Start Problem (System Limitation)**

If a user specifies a genre or mood not in the dataset (e.g., "metal," "energetic"), the system returns zero points for that dimension. The recommendation falls back to energy matching, potentially surfacing irrelevant songs. A metal lover receives upbeat pop songs instead of no results or an explanatory warning.

*Impact:* Out-of-distribution user preferences result in nonsensical recommendations without warning.

**4. Weighted Bias – Genre Hierarchy (Math Bias)**

Even at reduced +1.0 weight, genre matching still creates an implicit hierarchy where **songs from the target genre always rank higher than equal-scoring songs from other genres**. A song with perfect mood (+1.0) and excellent energy (+2.0) from a non-target genre (3.0 total) is beaten by a genre match with mediocre mood/energy (1.0 + 1.0 + 0.5 = 2.5). This **"Genre Silo"** prevents cross-genre discovery and locks users into echo chambers.

*Impact:* A pop fan will never discover an incredible ambient album that matches their mood perfectly because it's not "pop" enough.

**5. Mood Underrepresentation (Data Bias)**

With only 6 moods and an 11-song dataset, many mood-preference combinations have zero matches (e.g., "sad" mood doesn't exist). Cold start occurs silently—users don't know their mood preference is unsupported, leading to surprising results.

*Impact:* Niche emotional preferences (romantic, dark, aggressive) receive hallucinated recommendations.

### Summary: 
VibeFinder 1.0 optimizes for **simplicity, transparency, and mainstream user satisfaction** at the cost of **diversity, niche taste support, and fairness**. It is fundamentally a teaching tool, not a production recommender. Real-world systems mitigate these biases through collaborative filtering, content-based filtering networks, diversity penalties, and significantly larger, curated datasets representing global musical traditions.

---

## 7. Evaluation  

### **Testing Approach: Three User Profiles**

I tested three realistic user personas to understand when VibeFinder works well and when it fails:

1. **High-Energy Pop Lover** (wants: pop + happy + energetic)
2. **Chill Lofi Enthusiast** (wants: lofi + calm + low energy)
3. **Deep Intense Rock Fan** (wants: rock + intense + aggressive)

---

### **What Worked: The Perfect Matches**

When user preferences *align with the dataset*, VibeFinder produces excellent recommendations:

**Lofi + Chill + Low Energy** → Recommended "Library Rain" (Score: 4.0/4.0) ✅
- Perfect genre match (lofi), perfect mood match (chill), perfect energy match (0.35)
- Result: A flawless recommendation the user would immediately love.

**Rock + Intense + High Energy** → Recommended "Storm Runner" (Score: 4.0/4.0) ✅
- Perfect genre match (rock), perfect mood match (intense), perfect energy match (0.91)
- Result: A high-confidence recommendation that perfectly matches all three preferences.

**Plain English Translation:** When you tell the system what you want and that thing exists in our music library, you get a fantastic recommendation. The system found exactly what you were looking for.

---

### **The "Gym Hero Phenomenon": Mixed Signals**

During adversarial testing, I discovered an interesting quirk: **"Gym Hero" (pop + intense + 0.93 energy) sometimes appeared in "Happy Pop" recommendations**, even though the user wanted "happy" mood, not "intense."

**Why This Happens:**

Imagine you're searching for upbeat pop songs for a summer party. You specify:
- Genre: Pop ✓
- Mood: Happy ✓
- Energy: High (0.9) ✓

The system ranks songs by total score. "Sunrise City" wins because it matches all three dimensions (pop + happy + 0.82 energy = 3.84/4.0). But "Gym Hero" comes close (pop + intense + 0.93 energy = 2.94/4.0) because it nails the energy dimension so perfectly that the mood mismatch doesn't hurt as much.

**Why This Matters:** The system treats energy as equally important as mood + genre combined. For a workout playlist, that's great—you want high-energy songs regardless of their emotional tone. But for a party playlist, you might want happy songs *of any energy level* rather than intense songs *just because they're energetic*. 

**Real-World Impact:** Users sometimes get surprised recommendations that are "technically correct" (high energy + pop) but emotionally wrong (intense instead of happy). This is the algorithm working as designed, not a bug—but it reveals a fundamental design choice: *energy optimization can override mood*.

---

### **What Surprised Me #1: Polar Opposite Energy Preferences Prevent Cross-Recommendation**

The pop lover (0.9 energy target) and lofi fan (0.35 energy target) received *completely different* recommendations, which is correct. But here's the surprise: **the algorithm never gets confused between them**. A song can't score well for both profiles because the energy requirements are so incompatible.

*Reflection:* This is actually a strength. The system won't accidentally recommend "Midnight Coding" (a laidback lofi song at 0.42 energy) to someone training for a workout. Different energy targets create natural "lanes" that protect users from completely wrong recommendations.

---

### **What Surprised Me #2: The "Chill Lofi Sweet Spot" Reveals Data Bias**

Lofi received perfect 4.0 scores because:
- We have 3 lofi songs in our 11-song dataset (27% of catalog)
- One of them ("Library Rain") perfectly matches the lofi + chill preference at exactly the right energy level

*Reflection:* This perfect score is actually a data bias problem masquerading as algorithm success. In a real music catalog with 100,000 songs, there would be ~27,000 lofi songs, and the rankings would have more nuance. The fact that we see "perfect" scores tells me our dataset is too small to properly test ranking discrimination.

**What this means for users:** Lofi fans love this recommender because we happen to have good lofi data. Classical fans would be disappointed because we don't. Users don't blame the algorithm—they think the system "just doesn't like my genre."

---

### **What Surprised Me #3: Cold Start Fails Silently (and Invisibly)**

When I tested a "classical music lover," the system didn't reject the request or warn me. Instead, it silently fell back to scoring by mood + energy only, and recommended "Coffee Shop Stories" (jazz, not classical).

*Reflection:* To a non-programmer, this looks like the system "doesn't know classical music but tried anyway." To a data scientist, it's a "graceful degradation" strategy. To a user, it's confusing—they asked for classical and got jazz.

**The lesson:** Algorithms don't handle unexpected input the way humans do. A human music expert would say "Sorry, we don't have classical—can I suggest jazz instead?" The algorithm just... returns results and hopes you don't notice.

---

### **Evaluation Summary: When VibeFinder Shines and When It Stumbles**

| Scenario | Result | Why |
|----------|--------|-----|
| User wants mainstream genre (pop, lofi, rock) | ⭐⭐⭐⭐⭐ Excellent | Dataset has these genres well-represented |
| User seeks energy-first recommendations | ⭐⭐⭐⭐ Very Good | Energy weight is strong and flexible |
| User wants mood-focused suggestions | ⭐⭐⭐ Good | Mood works well *if* dataset has that mood |
| User specifies niche genre (classical, metal) | ⭐⭐ Poor | Dataset doesn't have it; silent fallback |
| User has conflicting preferences | ⭐⭐ Poor | Algorithm picks energy + genre, ignores mood |
| User discovers new artists accidentally | ⭐⭐ Limited | High genre weight prevents cross-genre serendipity |

---

---

## 8. Future Work  

**Short-term Improvements:**
1. **Add Missing Moods & Genres:** Expand dataset to include "sad," "metal," "dark," "energetic" and non-Western genres.
2. **Mood-Based Filtering:** Implement minimum match thresholds (e.g., "at least one of mood/genre must match").
3. **Cold Start Detection:** Warn users when their preference is out-of-distribution and suggest closest alternatives.
4. **Non-Linear Energy Scoring:** Replace linear distance with a Gaussian kernel to soften penalties for near-misses: `energy_score = exp(-(|diff|/σ)²)`.

**Medium-term Enhancements:**
5. **Content-Based Diversity:** After ranking by score, apply a diversity penalty to diversify top-k by genre/mood.
6. **Collaborative Filtering:** If user ratings are available, surface songs loved by users with similar taste profiles.
7. **Explanation Depth:** Rank songs not just by score but by confidence (how many match dimensions) to surface "4-out-of-4 match" songs first.

**Philosophical Reflection:**
The core tension is **specialization vs. serendipity**. A high genre weight ensures recommendations feel coherent but limits discovery. A low genre weight enables cross-genre exploration but risks confused results. Production systems balance this through hybrid models (60% personalized, 40% exploratory) and **user-controllable exploreability sliders**. For VibeFinder 1.0, the current +1.0 genre / 2.0× energy / +1.0 mood balance reflects a **mild bias toward exploration**, which aligns with a classroom learning system's goal: help students *discover* what AI recommenders can do, and what they cannot.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
