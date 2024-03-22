"""Search Flow implementation in LangChain."""
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name
from langchain.agents import AgentExecutor
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults

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
    bing_wrapper = BingSearchAPIWrapper()
    bing_search_tool = BingSearchResults(
        name="bing_search_results",
        api_wrapper=bing_wrapper
    )
    agent_executor = AgentExecutor(
        agent=llm,
        tools=[bing_search_tool],  # Pass Azure Bing search tool to agent executor
        handle_parsing_errors=True
    )
    result = llm.invoke([message])
    print(f"answer:", result)
    return {"answer": result}
