from utils import make_registry
from utils import Calculator
from utils import call_llm
from utils import make_tools
from utils import execute_tool
import pprint

question = "what is 15 times 8?"

tools = make_tools([Calculator])
registry = make_registry([Calculator])

messages = [
    {
        "role": "user",
        "content": question,
    }
]

CALL = call_llm(messages, tools=tools)


def extract_message(response):
    return response['choices'][0]['message']


extracted_CALL = extract_message(CALL)
msg_tool_calls = extracted_CALL['tool_calls']

msg_exec_tool = execute_tool(msg_tool_calls[0], registry)
print("Resultat d'execution :")
pprint.pprint(msg_exec_tool)

messages.append(extracted_CALL)

messages.append({
    "role": "tool",
    "tool_call_id": msg_tool_calls[0]['id'],
    "content": msg_exec_tool,
})

print("Contenu renvoye au LLM :")
pprint.pprint(messages)

CALL_2 = call_llm(messages, tools=tools)
reponse_question = extract_message(CALL_2)
print("Reponse a la question :")
pprint.pprint(reponse_question)
