
import uuid
import streamlit as st
import pickle
import os
import time
import json
from streamlit import session_state
from chatmarker.constants import CHATMARKER_VERSION

st.set_page_config(
    page_title='问答数据集生成器',
    layout="wide",
    page_icon='🥳',
    initial_sidebar_state="expanded", #“auto”或“expanded”或“collapsed”
         menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': None
     }
)

def build_chat_area(placeholder, form_id: str, messages):
    with placeholder.form(form_id, True):
        for message in messages:
            message_dom = st.text_area(label=f"{message['role']}: ",
                                    value=message['content'],
                            height=100,
                            max_chars=2048,
                            placeholder="支持使用 Markdown 格式书写")
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            btn_previous = st.form_submit_button("上一个对话", use_container_width=True)
        with col2:
            btn_del = st.form_submit_button("删除", use_container_width=True)
        with col3:
            btn_save = st.form_submit_button("保存", use_container_width=True)
        with col4:
            btn_next = st.form_submit_button("下一个对话", use_container_width=True, type="primary")
        
        st.balloons()
        print(btn_next)
        if btn_next:
            placeholder.empty()
            st.session_state.index = st.session_state.index + 1
    return btn_previous, btn_del, btn_save, btn_next

def main():
    with open("dataset.json", "r", encoding="utf-8") as f:
        dataset = json.loads(f.read())
    
    if 'index' not in st.session_state:
        st.session_state.index = 0
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    st.title(f"ChatMarker {CHATMARKER_VERSION}")
    PROMPT=st.sidebar.text_input("提示词", value= "请给出以下问题的答案：")

    md_dom = st.markdown(f"> 对话数据 - {st.session_state.index}")

    data = dataset[st.session_state.index]
    messages = data["messages"]
    placeholder = st.empty()
    btn_previous, btn_del, btn_save, btn_next = build_chat_area(placeholder, str(uuid.uuid4()), messages)

if __name__ == "__main__":
    main()
