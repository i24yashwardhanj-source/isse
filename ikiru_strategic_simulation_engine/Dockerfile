# ===== Base image =====
FROM python:3.10-slim-bookworm

# ===== OS deps (lean) =====
# - build-essential: compile any light native deps if needed
# - git: optional, but handy for pip installs from VCS
# - libspatialindex-dev: needed by rtree (optional dep often used with osmnx)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libspatialindex-dev \
 && rm -rf /var/lib/apt/lists/*

# ===== Pip behavior: no cache, faster installs, no version check =====
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120

WORKDIR /app

# ===== Copy requirements and bypass any hash enforcement =====
# If your requirements have --hash entries, strip them to avoid hash mismatch failures.
COPY requirements.txt /app/requirements.txt
RUN sed -i -E 's/ --hash=[^ ]+//g' /app/requirements.txt \
 && python -m pip install --upgrade pip setuptools wheel \
 && pip config unset global.require-hashes || true

# ===== Install Python dependencies =====
RUN pip install -r requirements.txt

# ===== (Optional) Copy your application code =====
# COPY . /app

# ===== (Optional) JupyterLab default CMD =====
# If you plan to use JupyterLab inside the container, uncomment below.
# EXPOSE 8888
# CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--NotebookApp.token="]

# ===== (Optional) Quick sanity check (remove if not needed) =====
# Verifies a few critical libs import successfully at build time.
# RUN python - <<'PY'
# import pandas, seaborn, ortools, lifetimes, pymc, sklearn, matplotlib
# print("OK:",
#       "pandas", pandas.__version__,
#       "seaborn", seaborn.__version__,
#       "ortools", ortools.__version__)
# PY