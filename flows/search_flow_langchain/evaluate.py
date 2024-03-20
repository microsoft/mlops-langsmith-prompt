"""Evaluate search flow."""
from langsmith.evaluation import EvaluationResult, run_evaluator
from langchain.smith import RunEvalConfig
from mlops.common.config_utils import MLOpsConfig
from langsmith import Client
from flows.search_flow_langchain.flow import process
from mlops.common.naming_utils import generate_project_name


PROJECT_BASE_NAME = "search_flow_langchain"


@run_evaluator
def must_mention(run, example) -> EvaluationResult:
    """Implement evaluation metric."""
    prediction = run.outputs.get("answer").content
    required = example.outputs.get("output")
    if prediction == required:
        score = 1
    else:
        score = 0
    return EvaluationResult(key="output", score=score)


def main():
    """Implement evaluation setup and run."""
    MLOpsConfig()

    client = Client()

    eval_config = RunEvalConfig(
        custom_evaluators=[must_mention],
    )

    client.run_on_dataset(
        dataset_name="language_translation_toy",
        llm_or_chain_factory=process,
        evaluation=eval_config,
        verbose=True,
        project_name=generate_project_name(PROJECT_BASE_NAME),
        # Any experiment metadata can be specified here
        project_metadata={"version": "1.0.0"},
    )


if __name__ == "__main__":
    main()
