"""
This is a boilerplate pipeline 'data_prediction'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import prediction


def create_pipeline(**kwargs) -> Pipeline:
     return Pipeline([
        node(
            func=prediction,
            inputs=dict(image_path="params:path_image_test", model_path="params:model_path", path_result="params:path_result_predict"),
            outputs=None,
            name="predict_yolo_node"
        )
    ])
