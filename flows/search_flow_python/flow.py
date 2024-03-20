"""Search Flow implementation."""
from openai import AzureOpenAI
from mlops.common.config_utils import MLOpsConfig


def process(input: dict):
    """Implement search flow using Python SDK."""
    config = MLOpsConfig()

    # Generate a completion
    client = AzureOpenAI(
        api_key=config.gpt35_turbo_config["aoai_api_key"],
        api_version=config.gpt35_turbo_config["aoai_api_version"],
        azure_endpoint=config.gpt35_turbo_config["aoai_api_base"]
    )
    chat_completion = client.chat.completions.create(
        model=config.gpt35_turbo_config["aoai_deployment_name"],
        messages=[{"role": "user", "content": input["question"]}]
    )

    return {"answer": chat_completion}
