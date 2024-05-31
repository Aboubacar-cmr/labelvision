"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines.data_science import pipeline as data_science_pipe


def register_pipelines() -> dict[str, Pipeline]:
    data_science = data_science_pipe.create_pipeline()
    return {
        "ds": data_science,
        "__default__": data_science,
    }
