import streamlit as st

st.title("💬 Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []


def clear_chat():
    st.session_state.messages = []


st.button("Clear", on_click=clear_chat)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

client = st.session_state.get("openai_client")

if client is None:
    st.info("사이드바에서 OpenAI API Key를 입력하세요.")
    st.stop()

prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    messages = st.session_state.messages + [
        {"role": "user", "content": prompt}
    ]

    try:
        with st.chat_message("assistant"):
            stream = client.responses.create(
                model="gpt-6-luna",
                input=messages,
                stream=True,
            )

            # Responses API 이벤트에서 답변 텍스트만 전달
            def text_stream():
                with stream:
                    for event in stream:
                        if event.type == "response.output_text.delta":
                            yield event.delta
                        elif event.type == "response.failed":
                            raise RuntimeError("응답 생성 실패")
                        elif event.type == "error":
                            raise RuntimeError("스트리밍 오류")

            response = st.write_stream(text_stream())

        st.session_state.messages = messages + [
            {"role": "assistant", "content": response}
        ]

    except Exception:
        st.error("응답 생성에 실패했습니다. API 키와 잔액을 확인하세요.")