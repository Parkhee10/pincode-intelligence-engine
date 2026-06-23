# Contributing

This project is being built for Myntra WeForShe HackerRamp 2026 by a 2-person team. While external contributions aren't the primary focus during the hackathon window, the project follows standard open-source practices for clarity and maintainability.

## Branching Strategy

- `main` — always demo-stable
- `dev` — integration branch for in-progress work
- `feature/<name>` — individual feature branches (e.g. `feature/risk-model`, `feature/api-confidence-score`)

Pull requests merge into `dev`. Merges to `main` happen at milestone checkpoints.

## Commit Message Convention

We follow a lightweight conventional-commits style:
- `feat: ...` — new feature
- `fix: ...` — bug fix
- `docs: ...` — documentation changes
- `data: ...` — data sourcing/generation changes
- `test: ...` — test additions/changes
- `chore: ...` — tooling, structure, maintenance

## Code Style

- Python: PEP8, type hints where practical
- Keep functions small and explainable — this project prioritizes interpretability over model complexity, given its explainability requirements

## Issues

Check the [Issues](../../issues) tab for current tasks, labeled by area (`data`, `model`, `api`, `frontend`, `docs`).
