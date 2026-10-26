from utils import Database
from utils import make_sql_tools
from utils import make_registry
from utils import make_tools
from utils import call_llm
from utils import execute_tool

SYSTEM_PROMPT = """You are a SQL assistant with access to a SQLite database.

Tools:
- ListTables: list all tables
- DescribeTable: get table structure
- SQLQuery: execute any SQL query

Think step by step. Explore the schema first, then query."""


def extract_message(response):
    return response['choices'][0]['message']


def boucle_agent(question, tools, registry, max_iterations=5):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    i = 0
    while i < max_iterations:
        print("Number", i + 1)
        CALL = call_llm(messages, tools=tools)
        message = extract_message(CALL)
        messages.append(message)

        if not message.get('tool_calls'):
            return message['content']

        for tool_call in message['tool_calls']:
            resultat = execute_tool(tool_call, registry)
            print("   ", tool_call['function']['name'], tool_call['function']['arguments'])
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call['id'],
                "content": resultat,
            })

        i = i + 1

    return "Max iterations reached"


if __name__ == "__main__":
    db = Database("library.db")
    sql_tools = make_sql_tools(db)

    tools = make_tools(sql_tools)
    registry = make_registry(sql_tools)

    questions = [
        "What are the books written after 1970?",
        "Who is the author of 'Dune' and when were they born?",
        "How many books are there per genre?",
        "What is the average rating per publisher?",
        "Which author has written the most books?",
    ]

    for question in questions:
        print("Question :", question)
        reponse = boucle_agent(question, tools, registry)
        print("Reponse a la question :", reponse)
        print()
