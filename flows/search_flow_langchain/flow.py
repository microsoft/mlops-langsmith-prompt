"""Search Flow implementation in LangChain."""
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name


def process(input: dict):
    """Implement search flow using LangChain."""
    config = MLOpsConfig()

    llm = (AzureChatOpenAI(
        openai_api_version=config.gpt35_turbo_config["aoai_api_version"],
        azure_deployment=config.gpt35_turbo_config["aoai_deployment_name"]
    )).with_config({"run_name": generate_run_name()})

    message = HumanMessage(
        content=input["question"]
    )

    result = llm.invoke([message])

    return {"answer": result}
