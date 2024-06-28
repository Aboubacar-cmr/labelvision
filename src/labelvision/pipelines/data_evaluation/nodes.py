import pandas as pd

def load_results(results_csv: str) -> pd.DataFrame:
    df = pd.read_csv(results_csv)
    df.columns = df.columns.str.strip()  # Supprimer les espaces dans les noms de colonnes
    return df

def evaluate_model(results: pd.DataFrame) -> dict:
    metrics = {
        "precision": results['metrics/precision(B)'].mean(),
        "recall": results['metrics/recall(B)'].mean(),
        "mAP": results['metrics/mAP50(B)'].mean(),
    }
    return metrics

def save_metrics(metrics: dict, output_path: str):
    with open(output_path, 'w') as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")

def print_metrics(metrics: dict):
    print("Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
