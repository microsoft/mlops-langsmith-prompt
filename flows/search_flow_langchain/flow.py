"""Search Flow implementation in LangChain."""
import uuid
import requests
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name
from langchain.tools import tool
from langchain.callbacks.manager import Callbacks
from langchain.schema.output_parser import StrOutputParser
from langchain_community.utilities import BingSearchAPIWrapper
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class SummaryResult:
    """A data class representing the result of a summary.

    Attributes:
        content (str): The summarized content.
    """

    content: str


@tool
def bing_search_tool(question: str, callbacks: Callbacks = None):
    """Search using the Azure Bing Search API."""
    bing_wrapper = BingSearchAPIWrapper()
    # Run query through BingSearch and return snippet, title, and link metadata
    search_results = bing_wrapper.results(question, 5)
    return search_results


@tool
def summarize_tool(url: str, callbacks: Callbacks = None):
    """Summarize a website."""
    config = MLOpsConfig()
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/58.0.3029.110 Safari/537.3')
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all('p')])

        summary_chain = (
            ChatPromptTemplate.from_template(
                "Summarize the following text:\n<TEXT {uid}>\n" "{text}" "\n</TEXT {uid}>"
            ).partial(uid=lambda: uuid.uuid4())
            | AzureChatOpenAI(
                api_version=config.gpt35_turbo_config["aoai_api_version"],
                azure_deployment=config.gpt35_turbo_config["aoai_deployment_name"]
            )
            | StrOutputParser()
        ).with_config({"run_name": generate_run_name()})

        summary_text = summary_chain.invoke(
            {"text": text},
            {"callbacks": callbacks},
        )
        return SummaryResult(content=summary_text)
    else:
        # If request was not successful, return an error message
        return SummaryResult(content="Failed to retrieve content from the URL.")


def process(input: dict):
    """Implement search flow using LangChain.

    Args:
        input (dict): Input dictionary containing the question.

    Returns:
        dict: A dictionary containing the search result.
    """
    try:
        results = bing_search_tool(input["question"])
        top_link = results[0]['link']
        result = summarize_tool(top_link)
        return {"answer": result}
    except Exception as e:
        print("Error occurred during search:", e)
        return {"answer": "Search failed due to an error."}
