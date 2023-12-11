from __future__ import annotations
from dotenv import load_dotenv
from typing import Optional, Tuple, List, Literal, Dict
import re
import openai
import os
import json
from dataclasses import dataclass, asdict
from textwrap import dedent
from collections import defaultdict

load_dotenv()
openai.api_key = os.getenv("openai.api_key")


def dict_shape(d, parent_index=""):
    shapes = {}
    for i, (key, value) in enumerate(d.items()):
        index = f"{parent_index}.{i}" if parent_index else str(i)
        shapes[key] = index
        if isinstance(value, dict):
            shapes.update(dict_shape(value, index))
    return shapes

def print_structure_with_shape(d, shapes, indent=0):
    for key, value in d.items():
        print(" " * indent + f"Key: {key}, Shape: {shapes[key]}")
        if isinstance(value, dict):
            print_structure_with_shape(value, shapes, indent + 4)
        elif isinstance(value, str):
            print(" " * (indent + 4) + f"Value: {value} (Type: str)")

@dataclass
class Message:
    content: str
    role: Literal["user", "system", "assistant"]

    def __post_init__(self):
        self.content = dedent(self.content).strip()

# 초기 대화 
START_CONVERSATION = [
    Message("""
        You are a useful AI that can generate mind maps based on any input or instructions.
    """, role="system"),
    Message("""
        You have the ability to perform the following actions given a request
        to create or recommend words for a mind map:
        1. create(subject) - create a mindmap about a given subject
        2. recommend(nodes) - recommend 5 words for the next sub node to extend given nodes
        
        Answer in the same language you are asked. 
        recommend 5 words for the next sub node. ['AI 공부하기' , '수학', '선형 대수학']
        
    """, role="user"), 
    Message("""
           ["벡터", "행렬", "연립방정식", "고유값과 고유벡터", "차원 축소"]
        """, role="assistant")

]
def ask_chatgpt(conversation: List[Message]) -> Tuple[str, List[Message]]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[asdict(c) for c in conversation]
    )

    msg = Message(**response["choices"][0]["message"])
    return msg.content, conversation + [msg]

def recommend_next_nodes(connected_nodes: List[str]) -> List[str]:
    conversation = START_CONVERSATION + [
        Message(f"recommend 5 words for next node from {str(connected_nodes)}", role="user")
    ]

    output, _ = ask_chatgpt(conversation)
    recommended_words = json.loads(output)

    return recommended_words

def get_recommendations(connected_nodes: List[str]):
    if openai.api_key is None:
        print("Please set the OPENAI_API_KEY environment variable.")
        return None

    recommended_nodes = recommend_next_nodes(connected_nodes)
    return recommended_nodes