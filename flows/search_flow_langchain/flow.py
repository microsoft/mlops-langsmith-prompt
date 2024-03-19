"""Search Flow implementation in LangChain."""
import os
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_community.callbacks import get_openai_callback

from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name


PROJECT_NAME = "Search Flow LangChain"


def main():
    # It loads env variables as well behind the scene.
    config = MLOpsConfig()

    os.environ["LANGCHAIN_PROJECT"] = PROJECT_NAME

    llm = (AzureChatOpenAI(
        openai_api_version=config.gpt35_turbo_config["aoai_api_version"],
        azure_deployment=config.gpt35_turbo_config["aoai_deployment_name"]
    )).with_config({"run_name": generate_run_name()})

    message = HumanMessage(
        content="Translate this sentence from English to French. I love programming."
    )

    with get_openai_callback() as cb:
        llm.invoke([message])
        print(
            f"Total Cost (USD): ${format(cb.total_cost, '.6f')}"
        )


if __name__ == "__main__":
    main()
