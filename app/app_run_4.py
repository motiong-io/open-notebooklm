"""

TEST Version on 5733
streamlit run app/app_run_4.py --server.port 5733

"""

import streamlit as st
from app.constants import UI_AVAILABLE_LANGUAGES, UI_EXAMPLES,EMPTY_EXAMPLE_DATA,ST_HIDE_HEADER_HTML
import os

st.set_page_config(page_title="Notebook LM (test)", page_icon="assets/img/faviconV2.png", layout="centered", initial_sidebar_state="expanded")
st.markdown(ST_HIDE_HEADER_HTML, unsafe_allow_html=True)

#### Sidebar

from app.st_page_funcs.sessions_about import fill_example_data,init_session_state

st.sidebar.image("assets/img/companyLogo.png",use_container_width=True)

if not st.session_state:
    fill_example_data(EMPTY_EXAMPLE_DATA)
init_session_state()

st.sidebar.write("Some examples to try:")
sidebar_c1, sidebar_c2,sidebar_c3,sidebar_c4 = st.sidebar.columns([1, 1, 1, 1])
if sidebar_c1.button("1️⃣"):
    fill_example_data(UI_EXAMPLES[0])
if sidebar_c2.button("2️⃣"):
    fill_example_data(UI_EXAMPLES[1])
if sidebar_c3.button("3️⃣"):
    fill_example_data(UI_EXAMPLES[2])
if sidebar_c4.button("↩️"):
    fill_example_data(EMPTY_EXAMPLE_DATA)


if "file" in st.session_state and st.session_state["file"]:
    source_index=0
elif "url" in st.session_state and st.session_state["url"]:
    source_index=1
else:
    source_index=0

source = st.sidebar.radio("Source", ["File", "URL"], key="source", index=source_index,horizontal=True)

if source == "File":
    if "file" in st.session_state and st.session_state["file"]:
        st.sidebar.write("File:", st.session_state["file"])
    else:
        file_like = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"], accept_multiple_files=False, disabled=True if "file" in st.session_state and st.session_state["file"] else False,label_visibility="collapsed")
        if file_like is not None:
            import os
            os.makedirs('app/examples_cached', exist_ok=True)
            save_path = os.path.join('app/examples_cached', 'uploaded_file.pdf')
            with open(save_path, 'wb') as f:
                f.write(file_like.getbuffer())
            st.session_state["url"] = None
            st.session_state["file"] = save_path


if source == "URL":
    if "url" in st.session_state and st.session_state["url"]:
        st.sidebar.write("Example URL:", st.session_state["url"])
    url = st.sidebar.text_input("URL", key="url", disabled=True if "url" in st.session_state and st.session_state["url"] else False)
    st.session_state["file"] = None


question = st.sidebar.text_area("Question (Optional)", key="question")
tone = st.sidebar.radio("Tone", ["Formal", "Fun"], key="tone", horizontal=True)
length = st.sidebar.radio("Length", ["Short (1-2 min)", "Medium (3-5 min)"], key="length", horizontal=True)
language = st.sidebar.selectbox("Language", UI_AVAILABLE_LANGUAGES, index=0)
# use_advanced = st.sidebar.checkbox("Use advanced", value=True, key="use_advanced")
use_advanced = True
random_voice_number = st.sidebar.select_slider("Random Voice Number",options=[i for i in range(9)],key="random_voice_number")

##### Main Page
from app.services.process_source import process_pdf,parse_url
from app.services.generate_script import generate_init_script,generate_modified_script
from app.services.generate_audios import generate_podcast_audio
from app.services.transcript_audio import AudioTranscriptionService

from app.schema import DialogueItem, MediumDialogue, ShortDialogue
from app.constants import (
    CHARACTER_LIMIT,
    ERROR_MESSAGE_TOO_LONG,
    MELO_TTS_LANGUAGE_MAPPING,
    SUNO_LANGUAGE_MAPPING,
    ST_MAINPAGE_TITLE_HTML,
    ST_MAINPAGE_TITLE_TOP_HTML
)
from typing import List
import asyncio

main_top_space = st.empty()
main_space = st.empty()

main_space.markdown(ST_MAINPAGE_TITLE_HTML, unsafe_allow_html=True)

current_task = None

def clean_unused_files():
    directory='app/examples_cached'
    session_files = [st.session_state["file"]]
    if not os.path.exists(directory):
        return 

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and file_path not in session_files:
            os.remove(file_path) 
            print(f"Deleted unused file: {file_path}")

async def podcast_gen(
    text: str, 
    speaker: str, 
    language: str, 
    use_advanced_audio: bool, 
    random_voice_number: int, 
    index: int = None
) -> str:
    audio_path = await asyncio.to_thread(
        generate_podcast_audio, 
        text, speaker, language, use_advanced_audio, random_voice_number, index
    )
    return audio_path



if "history_dialogues" not in st.session_state:
    st.session_state["history_dialogues"] = []



if st.sidebar.button("Start", key="start",use_container_width=True,disabled=False if st.session_state["file"] or st.session_state["url"] else True):
    main_top_space.markdown(ST_MAINPAGE_TITLE_TOP_HTML, unsafe_allow_html=True)
    main_space.info("Starting the conversation...")
    # st.write(st.session_state)


    if st.session_state["source"] == "File":
        text = process_pdf(st.session_state["file"])
    elif st.session_state["source"] == "URL":
        text = parse_url(st.session_state["url"])
    
    if len(text) > CHARACTER_LIMIT:
        st.error(ERROR_MESSAGE_TOO_LONG)
    else:
        # st.write(text)
        st.session_state["text"] = text
        st.toast("Got Document content",icon="🎉")
        
        with st.spinner("Generating Scripts..."):
            initial_script = generate_init_script(question, tone, length, language, text)
            st.session_state["got_transcripts"] = True
        # st.write(initial_script)
        st.toast("Got Scripts",icon="🎉")

        with main_space.container():
            # display the generated script one by one with audio
            for line in initial_script.dialogue:
                with st.spinner(f"Generating audio for {line.speaker}..."):
                    language_for_tts = SUNO_LANGUAGE_MAPPING[language]
                    if not use_advanced:
                        language_for_tts = MELO_TTS_LANGUAGE_MAPPING[language_for_tts]

                    audio_file_path = generate_podcast_audio(
                    line.text, line.speaker, language_for_tts, use_advanced, random_voice_number,len(st.session_state["history_dialogues"])
                    )

                    st.session_state["history_dialogues"].append(DialogueItem(speaker=line.speaker,text=line.text,audio_file_path=audio_file_path))

                    if line.speaker == "Host (MotionG Host)":
                        with st.chat_message("Host",avatar='🎤'):
                            st.write(line.text)
                            st.audio(audio_file_path, autoplay=True)
                    elif line.speaker == "Guest":
                        with st.chat_message("Guest",avatar='🪑'):
                            st.write(line.text)
                            st.audio(audio_file_path, autoplay=True)
                    else:
                        with st.chat_message("User",avatar='🙋‍♂️'):
                            st.write(line.text)


def show_history_dialogues(history_dialogues:List[DialogueItem]):
    for dialogue in history_dialogues:
        if dialogue.speaker == "Host (MotionG Host)":
            with st.chat_message("Host",avatar='🎤'):
                st.audio(dialogue.audio_file_path, autoplay=False)
                st.write(dialogue.text)

        elif dialogue.speaker == "Guest":
            with st.chat_message("Guest",avatar='🪑'):
                st.audio(dialogue.audio_file_path, autoplay=False)
                st.write(dialogue.text)

        else:
            with st.chat_message("User",avatar='🙋‍♂️'):
                st.write(dialogue.text)





### Input Widget

from streamlit_float import * 
from streamlit_chat_widget import chat_input_widget
float_init()
footer_container = st.container()
with footer_container:
    user_input = chat_input_widget()
footer_container.float(
    "display:flex; align-items:center;justify-content:center; overflow:hidden visible;flex-direction:column; position:fixed;bottom:15px;"
)


if user_input:
    if "text" in user_input:
        user_text =user_input["text"]
        input = user_text
    elif "audioFile" in user_input:
        audio_bytes = bytes(user_input["audioFile"])
        input = AudioTranscriptionService().get_audio_transcription_byte(audio_bytes)

    if input:
        main_space.empty()
        with main_space.container():
            st.session_state["history_dialogues"].append(DialogueItem(speaker="User",text=input, audio_file_path=None))
            main_top_space = st.container(height=150,border=False)
            main_top_space.markdown(ST_MAINPAGE_TITLE_TOP_HTML, unsafe_allow_html=True)

            show_history_dialogues(st.session_state["history_dialogues"])

            new_script = generate_modified_script(input, tone, length, language, st.session_state["text"], st.session_state["history_dialogues"])
            # st.write(new_script)
            for line in new_script.dialogue:
                with st.spinner(f"Generating audio for {line.speaker}..."):        
                    language_for_tts = SUNO_LANGUAGE_MAPPING[language]
                    if not use_advanced:
                        language_for_tts = MELO_TTS_LANGUAGE_MAPPING[language_for_tts]

                    audio_file_path = generate_podcast_audio(
                    line.text, line.speaker, language_for_tts, use_advanced, random_voice_number,len(st.session_state["history_dialogues"])
                    )

                    st.session_state["history_dialogues"].append(DialogueItem(speaker=line.speaker,text=line.text,audio_file_path=audio_file_path))

                    if line.speaker == "Host (MotionG Host)":
                        with st.chat_message("Host",avatar='🎤'):
                            st.audio(audio_file_path, autoplay=True)
                            st.write(line.text)
                    elif line.speaker == "Guest":
                        with st.chat_message("Guest",avatar='🪑'):
                            st.audio(audio_file_path, autoplay=True)
                            st.write(line.text)
                    else:
                        with st.chat_message("User",avatar='🙋‍♂️'):
                            st.write(line.text)


clean_unused_files()



