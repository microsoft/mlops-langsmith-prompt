"""Search Flow implementation in LangChain."""
import os
from flows.search_flow_langchain.flow import process


PROJECT_NAME = "Search Flow LangChain"


def main():
    """Implement search flow using LangChain."""
    os.environ["LANGCHAIN_PROJECT"] = PROJECT_NAME
    question = "What is Microsoft's mission?"

    message = {"question": question}
    process(message)


if __name__ == "__main__":
    main()
