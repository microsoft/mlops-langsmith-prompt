"""Search Flow implementation in LangChain."""
import os
from flows.search_flow_langchain.flow import process


PROJECT_NAME = "Search Flow LangChain"


def main():
    """Implement search flow using LangChain."""
    os.environ["LANGCHAIN_PROJECT"] = PROJECT_NAME
    url = "https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/how-to-integrate-with-langchain?view=azureml-api-2"
    question = "Search for relevant information at {url}"

    message = {
        "question": question,
         "url": url
    }
    print("message:", message)
    process(message)


if __name__ == "__main__":
    main()
