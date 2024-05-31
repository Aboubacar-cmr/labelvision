"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import train_yolo


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=train_yolo,
            inputs=dict(data_yaml="params:data_yaml", img_size="params:img_size", epochs="params:epochs"),
            outputs=None,
            name="train_yolo_node"
        )
    ])
