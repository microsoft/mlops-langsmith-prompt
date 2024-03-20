"""Search Flow implementation."""
# To run the example below, ensure the environment variable OPENAI_API_KEY is set
from langsmith.run_trees import RunTree
from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name
from flows.search_flow_python.flow import process


PROJECT_NAME = "Search Flow Python"


def main():
    """Implement search flow using Python SDK."""
    # Initialize all the variables
    MLOpsConfig()

    question = "Translate this sentence from English to French. I love programming."

    # Create a top-level run
    pipeline = RunTree(
        name=generate_run_name(),
        run_type="chain",
        inputs={"question": question},
        project_name=PROJECT_NAME
    )

    message = {
        "question": question
    }

    # Create a child run
    child_llm_run = pipeline.create_child(
        name="OpenAI Call",
        run_type="llm",
        inputs={"message": message},
    )

    chat_completion = process(message)

    # End the runs and log them
    child_llm_run.end(outputs=chat_completion)
    child_llm_run.post()

    pipeline.end(outputs=chat_completion)
    pipeline.post()


if __name__ == "__main__":
    main()
