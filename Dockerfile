#syntax=docker/dockerfile:1.5

# ====================================================================================================
# Builder
FROM python:3.11-slim@sha256:4b2e5faf103be72abb65046501a89f8feaef28c1148fc2f9b3326e31694ee735 as builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /app
COPY pyproject.toml pdm.lock ./
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable
COPY src/ src/
RUN pdm install --prod --no-lock --no-editable

FROM builder as test

RUN pdm install -d

COPY tests/ tests/

# ====================================================================================================
# Prod
FROM python:3.11-slim@sha256:4b2e5faf103be72abb65046501a89f8feaef28c1148fc2f9b3326e31694ee735 as prod

ENV PYTHONPATH=/app/pkgs
WORKDIR /app
COPY --from=builder /app/__pypackages__/3.11/lib pkgs/

COPY src/ src/

CMD ["python", "src/vent/__main__.py"]
