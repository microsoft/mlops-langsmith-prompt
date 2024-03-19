"""Search Flow implementation."""
# To run the example below, ensure the environment variable OPENAI_API_KEY is set
from openai import AzureOpenAI
from langsmith.run_trees import RunTree
from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name


PROJECT_NAME = "Search Flow Python"


def main():
    """Implement search flow."""
    config = MLOpsConfig()

    # This can be a user input to your app
    question = "Can you summarize this morning's meetings?"

    # Create a top-level run
    pipeline = RunTree(
        name=generate_run_name(),
        run_type="chain",
        inputs={"question": question},
        project_name=PROJECT_NAME
    )

    # This can be retrieved in a retrieval step
    context = "During this morning's meeting, we solved all world conflict."

    messages = [
        {"role": "system", "content": "You are a helpful assistant. \
          Please respond to the user's request only based on the given context."},
        {"role": "user", "content": f"Question: {question}\nContext: {context}"}
    ]

    # Create a child run
    child_llm_run = pipeline.create_child(
        name="OpenAI Call",
        run_type="llm",
        inputs={"messages": messages},
    )
    # Generate a completion
    client = AzureOpenAI(
        api_key=config.gpt35_turbo_config["aoai_api_key"],
        api_version=config.gpt35_turbo_config["aoai_api_version"],
        azure_endpoint=config.gpt35_turbo_config["aoai_api_base"]
    )
    chat_completion = client.chat.completions.create(
        model=config.gpt35_turbo_config["aoai_deployment_name"], messages=messages
    )

    # End the runs and log them
    child_llm_run.end(outputs=chat_completion)
    child_llm_run.post()

    pipeline.end(outputs={"answer": chat_completion.choices[0].message.content})
    pipeline.post()


if __name__ == "__main__":
    main()
