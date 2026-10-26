from utils import make_registry
from utils import Calculator
from utils import call_llm
from utils import make_tools
from utils import execute_tool


def extract_message(response):
    return response['choices'][0]['message']


def boucle_agent(question, tools, registry, max_iterations=5):
    messages = [
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
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call['id'],
                "content": resultat,
            })

        i = i + 1

    return "Max iterations reached"


tools = make_tools([Calculator])
registry = make_registry([Calculator])

questions = [
    "What is 15 times 8?",
    "What is (15 times 8) plus 20?",
    "What is 100 divided by 4, minus 3?",
]

for question in questions:
    print("Question :", question)
    reponse = boucle_agent(question, tools, registry)
    print("Reponse a la question :", reponse)
    print()
