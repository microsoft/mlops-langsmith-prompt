"""This script does initial data upload. Existing datasets will be replaced."""
from langsmith import Client
from mlops.common.config_utils import MLOpsConfig
import pandas as pd


def main():
    """Enumerate datasets from config and recreate them."""
    config = MLOpsConfig()
    datasets = config.datasets

    client = Client()

    for dataset in datasets:
        existing_ds = client.list_datasets(dataset_name=dataset)
        for ex_ds in existing_ds:
            print(f"Deleting existing {dataset}")
            client.delete_dataset(dataset_id=ex_ds.id)

        data = pd.read_csv(datasets[dataset]["location"])

        input_keys = datasets[dataset]["input_keys"]
        output_keys = datasets[dataset]["output_keys"]
        print(f"Uploading data into {dataset}")
        client.upload_dataframe(
            df=data,
            input_keys=input_keys,
            output_keys=output_keys,
            name=dataset,
            description=datasets[dataset]["description"],
            data_type="kv"
        )
        print(f"{dataset} has been uploaded")


if __name__ == "__main__":
    main()
