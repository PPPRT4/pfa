from Langgraph_agent.langgraph_agent import build_graph

graph_app = build_graph()


def run_my_agent(inputs):
    result = graph_app.invoke({
        "query": inputs["input"]
    })

    return result.get("answer", "")