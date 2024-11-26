import streamlit as st
from app.constants import UI_AVAILABLE_LANGUAGES, UI_EXAMPLES
from pathlib import Path

st.set_page_config(page_title="Notebook LM", page_icon="➕", layout="centered", initial_sidebar_state="expanded")

st.title("Notebook LM")
st.sidebar.title('Settings')

# 定义一个函数来填充示例数据
def fill_example_data(example_data):
    st.session_state["example_file"] = example_data[0][0] if example_data[0] else None
    st.session_state["url"] = example_data[1]
    st.session_state["question"] = example_data[2]
    st.session_state["tone"] = example_data[3]
    st.session_state["length"] = example_data[4]
    st.session_state["language"] = example_data[5]
    st.session_state["use_advanced"] = example_data[6]

# 创建按钮来填充示例数据
if st.sidebar.button("Fill Example Data 1"):
    fill_example_data(UI_EXAMPLES[0])

if st.sidebar.button("Fill Example Data 2"):
    fill_example_data(UI_EXAMPLES[1])

if st.sidebar.button("Fill Example Data 3"):
    fill_example_data(UI_EXAMPLES[2])

# 创建输入组件
file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"], accept_multiple_files=True)
url = st.sidebar.text_input("URL (Optional)", key="url")
question = st.sidebar.text_input("Question (Optional)", key="question")
tone = st.sidebar.radio("Tone", ["Formal", "Fun"], key="tone", horizontal=True)
length = st.sidebar.radio("Length", ["Short (1-2 min)", "Medium (3-5 min)"], key="length", horizontal=True)
language = st.sidebar.selectbox("Language", UI_AVAILABLE_LANGUAGES, index=11, key="language")
use_advanced = st.sidebar.checkbox("Use advanced", value=True, key="use_advanced")

# 显示示例文件或上传的文件
if "example_file" in st.session_state and st.session_state["example_file"]:
    st.write("Example File:", st.session_state["example_file"])
else:
    st.write("Uploaded File:", file)

# 显示输入的数据
st.write("URL:", url)
st.write("Question:", question)
st.write("Tone:", tone)
st.write("Length:", length)
st.write("Language:", language)
st.write("Use advanced:", use_advanced)

# 处理生成播客的逻辑
if st.button("Generate Podcast"):
    st.write("Generating podcast with the following data:")
    if "example_file" in st.session_state and st.session_state["example_file"]:
        st.write("File:", st.session_state["example_file"])
    else:
        st.write("File:", file)
    st.write("URL:", url)
    st.write("Question:", question)
    st.write("Tone:", tone)
    st.write("Length:", length)
    st.write("Language:", language)
    st.write("Use advanced:", use_advanced)
    # 在这里添加生成播客的逻辑