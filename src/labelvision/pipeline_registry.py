"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines.data_science import pipeline as data_science_pipe
from .pipelines.data_prediction import pipeline as data_prediction_pipe
from .pipelines.data_evaluation import pipeline as data_evaluation_pipe

def register_pipelines() -> dict[str, Pipeline]:
    data_science = data_science_pipe.create_pipeline()
    data_prediction = data_prediction_pipe.create_pipeline()
    data_evaluation = data_evaluation_pipe.create_pipeline()
    return {
        "ds": data_science,
        "pred": data_prediction,
        "eval": data_evaluation,
        "__default__": data_science,
    }