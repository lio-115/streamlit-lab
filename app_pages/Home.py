import uuid

import streamlit as st
from openai import OpenAI

st.title("AI 질문·응답")

api_key = st.session_state.get("api_key", "")

@st.cache_data(ttl=3600, show_spinner=False)
def ask(question, cache_id, _client):
    response = _client.responses.create(
        model="gpt-6-luna",
        input=question,
    )
    return response.output_text


question = st.text_area("질문을 입력하세요")

if st.button("질문하기"):
    if not api_key:
        st.warning("OpenAI API Key를 입력하세요.")
    elif not question.strip():
        st.warning("질문을 입력하세요.")
    else:
        try:
            with st.spinner("답변 생성 중..."):
                answer = ask(
                    question.strip(),
                    st.session_state.cache_id,
                    st.session_state.openai_client,
                )
            st.write(answer)
        except Exception:
            st.error("요청에 실패했습니다. API 키, 잔액, 모델 접근 권한을 확인하세요.")
import base64

st.divider()
st.header("AI 이미지 생성")

image_prompt = st.text_area(
    "만들고 싶은 이미지를 설명하세요",
    placeholder="예: 부산 바다를 바라보는 귀여운 고양이",
)

if st.button("이미지 생성"):
    if "openai_client" not in st.session_state:
        st.warning("OpenAI API Key를 입력하세요.")
    elif not image_prompt.strip():
        st.warning("이미지 설명을 입력하세요.")
    else:
        try:
            with st.spinner("이미지 생성 중... 수십 초 걸릴 수 있어요."):
                client = st.session_state.openai_client

                result = client.images.generate(
                    model="gpt-image-2.6-flare",
                    prompt=image_prompt.strip(),
                )

                image_bytes = base64.b64decode(
                    result.data[0].b64_json
                )

            st.image(image_bytes, caption=image_prompt)

        except Exception:
            st.error(
                "이미지 생성에 실패했습니다. "
                "API 잔액과 이미지 모델 접근 권한을 확인하세요."
            )
