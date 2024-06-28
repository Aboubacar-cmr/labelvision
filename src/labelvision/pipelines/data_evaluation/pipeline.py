from kedro.pipeline import Pipeline, node, pipeline
from .nodes import load_results, evaluate_model, save_metrics, print_metrics

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=load_results,
            inputs="params:results_csv",
            outputs="results_df",
            name="load_results_node",
        ),
        node(
            func=evaluate_model,
            inputs="results_df",
            outputs="metrics",
            name="evaluate_model_node",
        ),
        node(
            func=print_metrics,
            inputs="metrics",
            outputs=None,
            name="print_metrics_node",
        ),
        node(
            func=save_metrics,
            inputs=dict(metrics="metrics", output_path="params:metrics_output_path"),
            outputs=None,
            name="save_metrics_node",
        ),
    ])
