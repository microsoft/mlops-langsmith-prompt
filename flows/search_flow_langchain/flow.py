"""Search Flow implementation in LangChain."""
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name
from langchain.tools import tool
from langchain.callbacks.manager import Callbacks
from langchain.schema.output_parser import StrOutputParser
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults


@tool
def bing_search_tool(url: str, callbacks: Callbacks = None):
    """Search using the Azure Bing Search API."""
    config = MLOpsConfig()
    bing_wrapper = BingSearchAPIWrapper()
    chain = (
        ChatPromptTemplate.from_template("Search for relevant information based on the following URL:\n{{uid}}>"
        ).partial(url=url)
        | AzureChatOpenAI(
            api_version=config.gpt35_turbo_config["aoai_api_version"],
            azure_deployment=config.gpt35_turbo_config["aoai_deployment_name"]
        )
        | StrOutputParser()
        | BingSearchResults(
            name="bing_search_results",
            api_wrapper=bing_wrapper,
            url=url
        )
    ).with_config({"run_name": generate_run_name()})

    return chain.invoke(
        {"url": url},
        {"callbacks": callbacks},
    )


def process(input: dict):
    """Implement search flow using LangChain.

    Args:
        input (dict): Input dictionary containing the question and URL.

    Returns:
        dict: A dictionary containing the search result.
    """
    try:
        search_result = bing_search_tool(input["url"])

        # print("Search Result:", search_result)
        return {"summary": search_result}
    except Exception as e:
        print("Error occurred during search:", e)
        return {"summary": "Search failed due to an error."}
