import streamlit as st


def fill_example_data(example_data):
    st.session_state["file"] = example_data[0][0] if example_data[0] else None
    st.session_state["url"] = example_data[1]
    st.session_state["question"] = example_data[2]
    st.session_state["tone"] = example_data[3]
    st.session_state["length"] = example_data[4]
    st.session_state["language"] = example_data[5]
    st.session_state["use_advanced"] = example_data[6]
    st.session_state['random_voice_number'] = example_data[7]


def init_session_state():
    if "file" not in st.session_state:
        st.session_state["file"] = None
    if "url" not in st.session_state:
        st.session_state["url"] = None
    if "question" not in st.session_state:
        st.session_state["question"] = ""
    if "tone" not in st.session_state:
        st.session_state["tone"] = "Formal"
    if "length" not in st.session_state:
        st.session_state["length"] = "Short (1-2 min)"
    if "language" not in st.session_state:
        st.session_state["language"] = "English"
    if "use_advanced" not in st.session_state:
        st.session_state["use_advanced"] = True
    if "random_voice_number" not in st.session_state:
        st.session_state["random_voice_number"] = 4

    if "got_transcripts" not in st.session_state:
        st.session_state["got_transcripts"] = False
    if "text" not in st.session_state:
        st.session_state["text"] = ""
    if "disable_user_input" not in st.session_state:
        st.session_state["disable_user_input"] = True
    if "history_dialogues" not in st.session_state:
        st.session_state["history_dialogues"] = []