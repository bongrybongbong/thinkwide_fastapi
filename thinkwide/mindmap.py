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


def extract_last_response(output):
    # output이 튜플 형식인 경우 첫 번째 요소를 사용합니다.
    # output은 (문자열, 리스트) 형식으로 되어 있을 수 있습니다.
    if isinstance(output, tuple):
        output = output[0]

    # JSON 데이터를 파싱합니다.
    data = json.loads(output)

    # 대화 목록을 가져옵니다.
    messages = data[1]  # 첫 번째 요소가 대화 목록을 포함하고 있습니다.

    # 마지막 메시지를 찾습니다. 이 메시지는 'assistant' 역할의 것이어야 합니다.
    last_message = None
    for message in messages:
        if message['role'] == 'assistant':
            last_message = message['content']

    return last_message


def extract_last_response(output):
    # JSON 데이터를 파싱합니다.
    data = json.loads(output)

    # 대화 목록을 가져옵니다.
    messages = data[1]  # 첫 번째 요소가 대화 목록을 포함하고 있습니다.

    # 마지막 메시지를 찾습니다. 이 메시지는 'assistant' 역할의 것이어야 합니다.
    last_message = None
    for message in messages:
        if message['role'] == 'assistant':
            last_message = message['content']

    return last_message


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
        You are excellent at organizing and creating mind map based on input words
    """, role="system"),
    Message("""
            I'm going to give you a cluster of words from a brainstorming session. From these, please identify the most central theme keyword and then organize the rest of the words into a mind map in markdown format. (please code format)
            for example ,
            # ThinkWide
            ## Technology Development
            ### Hardware Compatibility
            #### VR Headset Support
            #### Controller Options
            ### Software Interaction
            #### Hand Gesture Recognition
            #### Voice Commands
            ### Development Tools Integration
            #### Unity, Unreal Engine Plugins
            ### Networking and Stability
            #### Multiplayer Support
            #### Data Synchronization
            
        Please answer in Korean
        The words are as follows:      
        ['사용자 참여', '가상 이벤트', '사용자 경험','인터페이스 디자인','가상 커뮤니티','협업 도구','실시간 상호작용','맞춤화','프로토타이핑','크로스 플랫폼','확장성','통합된 생태계','가상 상거래','데이터 분석','개인 정보 보호','지속 가능성','멀티미디어 콘텐츠','접근성','파트너십','인프라 개발','사용자 피드백','모니터링 및 관리','기술 통합','글로벌 도달','가상 학습','API 개발','브랜딩 전략','콘텐츠 모더레이션','네트워크 보안','지적 재산권']    
                
    """, role="user"), 
    Message("""
           # 가상 혁신
            ## 사용자 참여
            ### 가상 이벤트
            ### 사용자 경험
            ### 인터페이스 디자인
            ### 가상 커뮤니티
            ## 협업 도구
            ### 실시간 상호작용
            ### 맞춤화
            ## 기술 및 플랫폼
            ### 프로토타이핑
            ### 크로스 플랫폼
            ### 확장성
            ### 통합된 생태계
            ## 가상 상거래
            ### 데이터 분석
            ### 개인 정보 보호
            ## 지속 가능성
            ### 멀티미디어 콘텐츠
            ### 접근성
            ### 파트너십
            ## 인프라 개발
            ### 사용자 피드백
            ### 모니터링 및 관리
            ### 기술 통합
            ## 글로벌 도달
            ### 가상 학습
            ### API 개발
            ### 브랜딩 전략
            ### 콘텐츠 모더레이션
            ### 네트워크 보안
            ### 지적 재산권
        """, role="assistant")

]
def ask_chatgpt(conversation: List[Message]) -> Tuple[str, List[Message]]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[asdict(c) for c in conversation]
    )

    msg = Message(**response["choices"][0]["message"])
    return msg.content, conversation + [msg]

def make_mindmap(connected_nodes: List[str]):
    conversation = START_CONVERSATION + [
        Message(f"The words are as follows: {str(connected_nodes)}", role="user")
    ]

    output = ask_chatgpt(conversation)
    last_response = extract_last_response(output)
    return last_response

def get_mindmap(connected_nodes: List[str]):
    if openai.api_key is None:
        print("Please set the OPENAI_API_KEY environment variable.")
        return None

    mindmap_data = make_mindmap(connected_nodes)
    return mindmap_data