"""Search Flow implementation in LangChain."""
import os
from flows.search_flow_langchain.flow import process


PROJECT_NAME = "Search Flow LangChain"


def main():
    """Implement search flow using LangChain."""
    os.environ["LANGCHAIN_PROJECT"] = PROJECT_NAME

    question = "Summarize the Azure OpenAI tutorials." #"Translate this sentence from English to French. I love programming."

    message = {
        "question": question
    }

    process(message)


if __name__ == "__main__":
    main()
