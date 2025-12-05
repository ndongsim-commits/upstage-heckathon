import streamlit as st
from chat_message import ChatMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt

from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOllama
from langchain_teddynote import logging
import os
from retriever import load_existing_retriever

# API KEY 정보로드
load_dotenv()


# 프로젝트 이름을 입력합니다.
logging.langsmith("[RBA] ILJIN GPT")

# 캐시 디렉토리 생성
if not os.path.exists(".cache"):
    os.mkdir(".cache")

# 파일 업로드 전용 폴더
if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")

st.title("[RBA] ILJIN GPT💬")

# 처음 1번만 실행하기 위한 코드
if "RBA_messages" not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state["RBA_messages"] = []

if "chain" not in st.session_state:
    # 아무런 파일을 업로드 하지 않을 경우
    st.session_state["chain"] = None

# 사이드바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("CLEAR")


# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["RBA_messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시리를 추가
def add_message(role, message):
    st.session_state["RBA_messages"].append(ChatMessage(role=role, content=message))


def create_chain(retriever):
    # 단계 6: 프롬프트 생성(Create Prompt)
    prompt = load_prompt("prompts/pdf-rag.yaml", encoding="utf-8")

    # 단계 7: 언어모델(LLM) 생성
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 단계 8: 체인(Chain) 생성
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


retriever = load_existing_retriever("RBA_index")

if retriever:
    chain = create_chain(retriever)
    st.session_state["chain"] = chain
else:
    st.warning("Cannot find existing retriever.")

if clear_btn:
    st.session_state["RBA_messages"] = []

# 이전 대화 기록 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("Ask me about the RBA!")

# 경고 메시지를 띄우기 위한 빈 영역
warning_msg = st.empty()

if user_input:
    # chain을 생성
    chain = st.session_state["chain"]

    if chain is not None:
        # 사용자의 입력
        st.chat_message("user").write(user_input)
        # 스트리밍 호출
        response = chain.stream(user_input)
        with st.chat_message("assistant"):
            # 빈 공간(컨테이너)를 만들어서, 여기에 토큰을 스트리밍 출력한다.
            container = st.empty()

            ai_answer = ""
            for token in response:
                ai_answer += token
                container.markdown(ai_answer)

        # 대화기록을 저장
        add_message("user", user_input)
        add_message("assistant", ai_answer)
    else:
        warning_msg.error("Please upload a file.")
