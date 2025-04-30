# Zeta_Question-4 : Rate-limitter

**FastAPI** service for rate limiter functionality.

## Structure
- `src/main.py`        — Load artifacts, expose `GET /api/request`

## Quickstart

```bash
# 1. Clone & cd
git clone https://github.com/diyaverma1967/Zeta_Question-4.git
cd Zeta_Question-4

# 2. Set up Conda env
conda create -n Zeta_Question-4 python=3.11 -y
conda activate Zeta_Question-4

# 3. Start API
uvicorn src.main:app --reload
