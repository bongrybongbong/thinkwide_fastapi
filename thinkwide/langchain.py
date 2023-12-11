from dotenv import load_dotenv
load_dotenv()

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

#sequential chain

llm = OpenAI(temperature=0.7)

def keywor_and_mindmap(data):
    #chain1 : 레스토랑 이름 지어주기 체인
    making_mindmap = PromptTemplate(
        input_variables=['data'],
        template=""" I'm going to give you a cluster of words from a brainstorming session. From these, please identify the most central theme keyword and then organize the rest of the words into a mind map in markdown format. (please #code format)
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
        The words are as follows: {data}
        """
    )
    mindmap_chain = LLMChain(llm=llm, prompt=making_mindmap, output_key="mindmap_nodes")
    #chain2 : 메뉴 만들어주기 체인
    Prompt_tempate_items = PromptTemplate(
        input_variables=['mindmap_nodes'],
        template="SUGGEST SOME MENU ITEMS FOR {restaurant_name}."
    )
    Food_items_chain = LLMChain(llm=llm, prompt=Prompt_tempate_items, output_key="menu_items")
    # 결과로 나오 메뉴들 menu_item이라는 키로~
    chain = SequentialChain(
        chains=[name_chain, Food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )
    #우리는 이렇게 나온 결과를 응답으로 반환함
    response = chain({'cuisine': cuisine})

    return response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items(("KOREAN")))







---

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

def recommend_mindmap(connected_nodes: List[str]):
    conversation = START_CONVERSATION + [
        Message(f"The words are as follows: {str(connected_nodes)}", role="user")
    ]

    output, _ = ask_chatgpt(conversation)
    mindmap_data1 = json.loads(output)

    return mindmap_data1

def get_mindmap(connected_nodes: List[str]):
    if openai.api_key is None:
        print("Please set the OPENAI_API_KEY environment variable.")
        return None

    mindmap_data = recommend_mindmap(connected_nodes)
    return mindmap_data