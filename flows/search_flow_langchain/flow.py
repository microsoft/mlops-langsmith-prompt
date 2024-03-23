"""Search Flow implementation in LangChain."""
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from mlops.common.config_utils import MLOpsConfig
from mlops.common.naming_utils import generate_run_name
from langchain.agents import AgentExecutor
from langchain import agents, tools
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from langchain import chat_models, prompts, callbacks, schema, agents, tools


def process(input: dict):
    """Implement search flow using LangChain."""
    config = MLOpsConfig()

    agent_executor = agents.initialize_agent(
        llm=AzureChatOpenAI(openai_api_version=config.gpt35_turbo_config["aoai_api_version"], azure_deployment=config.gpt35_turbo_config["aoai_deployment_name"]),
        tools=[tools.ReadFileTool(), tools.WriteFileTool(), tools.ListDirectoryTool()],
        agent=agents.AgentType.OPENAI_FUNCTIONS, handle_parsing_errors=True, verbose=True,
    )
    message = HumanMessage(
        content=input["question"]
    )
    list_dir_tool_invocation = {"list_directory": {"dir_path": "."}}

    with callbacks.collect_runs() as cb:
        result = agent_executor.with_config({"run_name": generate_run_name()}).invoke([message, list_dir_tool_invocation]) # {"list_directory": {"dir_path": "."}}
        run = cb.traced_runs[0]
        print("Output:", result["output"])
        print(f"Saved name: {run.name}")

    return {"answer": result}