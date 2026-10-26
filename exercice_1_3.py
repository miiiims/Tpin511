from dataclasses import dataclass
from utils import make_registry
from utils import call_llm
from utils import make_tools
from utils import execute_tool
import pprint
from typing import Literal



@dataclass
class WordCounter:
    """Count the number of words in a text."""

    text: str
    language: Literal["french", "english"] = "english"
    def __call__(self):
        return len(self.text.split())


question = "How many words are in 'Hello world, this is a test'?"

tools = make_tools([WordCounter])
print("Schema de l'outil :")
pprint.pprint(tools)

registry = make_registry([WordCounter])

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
