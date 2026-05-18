# Marine Oil Spill Detection for the Gemma 4 Good Hackathon

[![Kaggle](https://img.shields.io/badge/Kaggle-Gemma%204%20Good%20Hackathon-blue)](https://www.kaggle.com/competitions/gemma-4-good-hackathon)

## Overview

This repository contains a submission-oriented oil-spill workflow for the Kaggle Gemma 4 Good Hackathon.

Primary entry point:

- `gemma-oil-detect.ipynb` (classification + scenario + vessel context + executive summary)

Core pipeline:

- classify Sentinel-1 SAR sample chips for oil vs no-oil
- generate a synthetic 2022 spill scenario when oil is detected
- backtrack origin and project +24h drift with HYCOM currents
- evaluate coastline proximity/intersection risk
- rank nearby vessels from AMSA AIS archives and display a local track
- produce a Gemma-generated markdown summary via Ollama and expose a structured `gemma4_prompt`

## Quick Start

From repository root:

```powershell
Push-Location .\gemma-oil-detect
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Pop-Location
```

Then open and run `gemma-oil-detect.ipynb`.

The executive summary step requires Ollama with a Gemma model available locally.

## Environment Configuration

Runtime values can be set in environment variables or a local `.env` file in `gemma-oil-detect/`.

Recommended variables:

- `AUTO_INITIALIZE_EARTH_ENGINE=1`
- `EARTHENGINE_PROJECT=<project-id>`
- `FALLBACK_SAMPLE_LABEL=1`
- `SAMPLE_SELECTION_SEED=42`

## MARPOL-Informed Priority Rules

This project is not a legal compliance engine, but it uses MARPOL Annex I distance thresholds as an operational prioritization heuristic:

- tanker-linked context: high priority when within **50 NM** of coast
- non-tanker context: high priority when within **12 NM** of coast

These thresholds are used for triage and reporting narrative, not formal regulatory determination.

## Demo Behavior

- With Google Earth Engine available: random sample selection, live synthetic scenario attempts.
- Without Google Earth Engine: deterministic demo fallback scenario.
- In fallback mode, `FALLBACK_SAMPLE_LABEL=1` can force a positive sample so the full path remains visible.
- Vessel track display uses adjacent monthly AIS scope around the ranked observation and may show fewer than 21 points when before/after points are unavailable.

## Training From Scratch

Use `model_prepare_kaggle.ipynb` (Kaggle GPU recommended) to reproduce training and distillation.

It will:

- split data into train/validation/test
- train three individual models with weighted sampling and focal loss
- build an uncertainty-weighted ensemble
- distill the ensemble into a lightweight student model
- write `.pth` outputs to `best_models/`

## Repository Layout

- `gemma-oil-detect.ipynb` - main submission notebook
- `model_prepare_kaggle.ipynb` - training and distillation workflow
- `best_models/best_student.pth` - distilled student checkpoint
- `data/amsa_ais/` - AMSA monthly AIS archives
- `data/coastline/` - coastline shapefile for rendering

## Data Sources

- Sentinel-1 SAR sample chips (ESA / Copernicus Sentinel-1 mission)
   https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-1
- AMSA monthly AIS archives (Australian Maritime Safety Authority)
   https://www.amsa.gov.au/safety-navigation/navigation-systems/automatic-identification-system-ais
- HYCOM sea-water velocity (Google Earth Engine)
   https://developers.google.com/earth-engine/datasets/catalog/HYCOM_sea_water_velocity
- NOAA/NGDC ETOPO1 bathymetry (Google Earth Engine)
   https://developers.google.com/earth-engine/datasets/catalog/NOAA_NGDC_ETOPO1
- Natural Earth coastline vectors
   https://www.naturalearthdata.com/

## Notes

- The notebook is a controlled demo and uses synthetic scenario generation for workflow demonstration.
- If classification is no-oil, drift modeling and vessel ranking are intentionally skipped.
- Output is explicit about fallback conditions and data provenance for transparency.
