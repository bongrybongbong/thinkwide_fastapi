def generate_mindmap_from_info(Node_text):
    Prompt = f"""
    You are a useful AI that can generate mind maps based on any input or instructions. You have the ability to perform the following actions given a request
        to create or recommend words for a mind map:
        1. create(subject) - create a mindmap about a given subject
        2. recommend(nodes) - recommend 5 words for the next sub node to extend given nodes
        
        Answer in the same language you are asked.
       Create a mind map about {Node_text}.
    """

    messages = [{'role': 'system', 'content': Prompt}]
    print(f"messages here:{messages}")

    chat = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=messages,
        temperature=0.6
    )

    reply = chat.choices[0].message.content
    save_to_database(Node_text, reply)
    # print(reply)
    #print(f'ChatGPT: {reply}', '\n') #gpt결과 출력e

    return reply



["스키", "스노우보드", "독서", "영화 감상", "핫 초코","가족 여행", "크리스마스", "새해 목표", "취미 클래스", "봉사 활동","휴식", "재충전", "친구들과의 만남", "게임", "조리법 시도","운동", "명상", "일기 쓰기", "예술 프로젝트", "온라인 강좌","집 정리", "가족 게임 밤", "실내 암벽 등반", "팟캐스트 듣기", "자기계발","언어 학습", "요가", "스노우맨 만들기", "눈싸움", "겨울 산책"]