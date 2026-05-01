# 🎵 Music Recommender Simulation

## Project Summary

This repository upgrades the original AI110 Module 3 music recommender into a modular agentic workflow. The new system transforms user intent into structured search parameters, retrieves candidate songs using the existing recommendation engine, and evaluates the final playlist with a critic that assigns explicit confidence scores.

## Architecture Overview

The new agentic pipeline is implemented in `src/agentic_engine.py` and follows a clean reasoning loop:

- **Planner Agent**: analyzes natural language intent and determines search parameters for energy, valence, tempo, mood, and genre.
- **Retrieval Tool**: fetches a candidate pool using the current recommendation logic in `src/recommender.py` and enriches it with tempo/valence alignment.
- **Critic Agent**: reviews candidates against the articulated intent, rejects misaligned songs, and computes a normalized confidence score.
- **Human-in-the-loop output**: the system generates recommendations and makes them easy for a human to inspect and approve.

A Mermaid diagram illustrating this flow is available at `assets/agentic_workflow.mmd`.

## Setup Instructions

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the original CLI example:

```bash
python3 -m src.main
```

4. Run the evaluation harness:

```bash
python3 tests/eval_harness.py
```

## Sample Interaction Traces

### Trace 1: Stressed and needing focus

**User input:** "I'm stressed and need to focus on my work"
- Planner infers low energy, moderate valence, and focused mood.
- Retrieval selects candidates that match calm focus and tempo preferences.
- Critic rejects songs that are too high energy.
- Output: a shortlist of mellow, focused tracks with confidence scores.

### Trace 2: Gym workout playlist

**User input:** "I want an upbeat high-energy playlist for the gym"
- Planner infers intense mood, high energy, and strong tempo.
- Retrieval prioritizes energetic songs and evaluates tempo alignment.
- Critic approves high-energy matches and assigns confidence values.
- Output: workout-ready recommendations above the pass threshold.

### Trace 3: Evening wind-down

**User input:** "Something calm and chill for winding down after a long day"
- Planner selects relaxed mood, low energy, low tempo, and moderate valence.
- Retrieval surfaces chill candidates from the catalog.
- Critic filters out songs that are too intense.
- Output: calming recommendations with transparent reasoning.

## Testing Summary

The evaluation harness in `tests/eval_harness.py` runs five predefined user scenarios and prints a pass/fail report:

- Pass if the top recommendation confidence is >= 0.7
- Fail otherwise
- The script also prints the average top confidence across scenarios

This harness demonstrates the reliability feature and helps validate the agentic workflow end-to-end.

## Project Files

- `src/recommender.py` — existing song scoring and CSV loader
- `src/agentic_engine.py` — new planner/retriever/critic agent pipeline
- `tests/eval_harness.py` — confidence-based evaluation harness
- `assets/agentic_workflow.mmd` — Mermaid data-flow diagram
- `model_card.md` — bias, risk, and AI collaboration reflection

## Notes

The design is intentionally modular and explainable. Each agent component is responsible for a single stage of the reasoning loop, making the code easier to discuss in interviews.
