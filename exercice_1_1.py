from utils import make_registry
from utils import Calculator
from utils import call_llm
from utils import make_tools
import pprint

question = "what is 15 times 8?"

tools = make_tools([Calculator])
print("Schema de l'outil :")
pprint.pprint(tools)

registry = make_registry([Calculator])
print("Registre :")
pprint.pprint(registry)

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
print("Reponse du LLM :")
pprint.pprint(extracted_CALL)

msg_tool_calls = extracted_CALL['tool_calls']
print("tool_calls :")
pprint.pprint(msg_tool_calls)


