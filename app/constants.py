"""
constants.py
"""

import os

from pathlib import Path

# Key constants
APP_TITLE = "Motion G Toolkit Test"
CHARACTER_LIMIT = 100_000

# Gradio-related constants
GRADIO_CACHE_DIR = "app/gradio_cached_examples/tmp/"
GRADIO_CLEAR_CACHE_OLDER_THAN = 1 * 24 * 60 * 60  # 1 day

# Error messages-related constants
ERROR_MESSAGE_NO_INPUT = "Please provide at least one PDF file or a URL."
ERROR_MESSAGE_NOT_PDF = "The provided file is not a PDF. Please upload only PDF files."
ERROR_MESSAGE_NOT_SUPPORTED_IN_MELO_TTS = "The selected language is not supported without advanced audio generation. Please enable advanced audio generation or choose a supported language."
ERROR_MESSAGE_READING_PDF = "Error reading the PDF file"
ERROR_MESSAGE_TOO_LONG = "The total content is too long. Please ensure the combined text from PDFs and URL is fewer than {CHARACTER_LIMIT} characters."

# Fireworks API-related constants
FIREWORKS_API_KEY = "xxxxxxxxxx"#os.getenv("FIREWORKS_API_KEY")
FIREWORKS_MAX_TOKENS = 16_384
FIREWORKS_MODEL_ID = "accounts/fireworks/models/llama-v3p1-405b-instruct"
FIREWORKS_TEMPERATURE = 0.1

# OpenAI API-related constants
OPENAI_API_KEY = ""
OPENAI_BASE_URL = "http://10.4.32.15:5000/api/openai/ve/v1"
OPENAI_MODEL_ID = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.1

# MeloTTS
MELO_API_NAME = "/synthesize"
MELO_TTS_SPACES_ID = "mrfakename/MeloTTS"
MELO_RETRY_ATTEMPTS = 3
MELO_RETRY_DELAY = 5  # in seconds

MELO_TTS_LANGUAGE_MAPPING = {
    "en": "EN",
    "es": "ES",
    "fr": "FR",
    "zh": "ZJ",
    "ja": "JP",
    "ko": "KR",
}


# Suno related constants
SUNO_LANGUAGE_MAPPING = {
    "English": "en",
    "Chinese": "zh",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Polish": "pl",
    "Portuguese": "pt",
    "Russian": "ru",
    "Spanish": "es",
    "Turkish": "tr",
}

# General audio-related constants
NOT_SUPPORTED_IN_MELO_TTS = list(
    set(SUNO_LANGUAGE_MAPPING.values()) - set(MELO_TTS_LANGUAGE_MAPPING.keys())
)
NOT_SUPPORTED_IN_MELO_TTS = [
    key for key, id in SUNO_LANGUAGE_MAPPING.items() if id in NOT_SUPPORTED_IN_MELO_TTS
]

# Jina Reader-related constants
JINA_READER_URL = "https://r.jina.ai/"
JINA_RETRY_ATTEMPTS = 3
JINA_RETRY_DELAY = 5  # in seconds

# UI-related constants

#- [Llama 3.1 405B 🦙](https://huggingface.co/meta-llama/Llama-3.1-405B) via [Fireworks AI 🎆](https://fireworks.ai/) and [Instructor 📐](https://github.com/instructor-ai/instructor) 

# UI_DESCRIPTION = """
# Generate Podcasts from PDFs using open-source AI.

# Built with:
# - [GPT-4o Mini 🤖](https://huggingface.co/openai/gpt-4o-mini) via [OpenAI 🌐](https://openai.com/)
# - [MeloTTS 🐚](https://huggingface.co/myshell-ai/MeloTTS-English)
# - [Bark 🐶](https://huggingface.co/suno/bark)
# - [Jina Reader 🔍](https://jina.ai/reader/)

# **Note:** Only the text is processed (100k character limits).
# """
UI_DESCRIPTION = """
<div style="position: relative; padding-top: 20px; padding-bottom: 38px; color: white; background: url('https://coolbackgrounds.io/images/backgrounds/index/sea-edge-79ab30e2.png') no-repeat center center; background-size: cover; border-radius: 10px;">
    <h1 style="text-align: center; font-size: 3rem; color: white;">Open NotebookLM</h1>
    <h2 style="text-align: center; font-size: 1.5rem; color: white;">Generate Your Podcasts from PDFs or URLs</h2>

</div>

<div style="opacity: 0.8;">

<p style="text-align: center; font-size: 0.9rem; padding-top: 10px;">
    <a href="https://github.com/motiong-io/open-notebooklm-test" target="_blank" style="color: #12c2e9; display: inline-flex; align-items: center;">Project</a>
    built with
    <a href="https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/" target="_blank" style="color: #12c2e9;">GPT-4o Mini</a>, 
    <a href="https://huggingface.co/myshell-ai/MeloTTS-English" target="_blank" style="color: #12c2e9;">MeloTTS</a>, 
    <a href="https://huggingface.co/suno/bark" target="_blank" style="color: #12c2e9;">Bark</a>, 
    and 
    <a href="https://jina.ai/reader/" target="_blank" style="color: #12c2e9;">Jina Reader</a>
    <br>
    <strong>Note:</strong> Only the text will be processed, and the input must be less than 100,000 characters.
</p>

</div>
"""


UI_AVAILABLE_LANGUAGES = list(SUNO_LANGUAGE_MAPPING.keys())
UI_INPUTS = {
    "file_upload": {
        "label": "1. 📄 Upload your PDF(s)",
        "file_types": [".pdf"],
        "file_count": "multiple",
    },
    "url": {
        "label": "2. 🔗 Paste a URL (optional)",
        "placeholder": "Enter a URL to include its content",
    },
    "question": {
        "label": "3. 🤔 Do you have a specific question or topic in mind?",
        "placeholder": "Enter a question or topic",
    },
    "tone": {
        "label": "4. 🎭 Choose the tone",
        "choices": ["Fun", "Formal"],
        "value": "Fun",
    },
    "length": {
        "label": "5. ⏱️ Choose the length",
        "choices": ["Short (1-2 min)", "Medium (3-5 min)"],
        "value": "Medium (3-5 min)",
    },
    "language": {
        "label": "6. 🌐 Choose the language",
        "choices": UI_AVAILABLE_LANGUAGES,
        "value": "English",
    },
    "advanced_audio": {
        "label": "7. 🔄 Use advanced audio generation? (Experimental)",
        "value": True,
    },
}
UI_OUTPUTS = {
    "audio": {"label": "🔊 Podcast", "format": "mp3"},
    "transcript": {
        "label": "📜 Transcript",
    },
}
UI_API_NAME = "generate_podcast"
UI_ALLOW_FLAGGING = "never"
UI_CONCURRENCY_LIMIT = 3
UI_EXAMPLES = [
    [
        [str(Path("app/examples/MotionG_bolg_1.pdf"))],
        "",
        "Explain this blog to me like in a fun way",
        "Fun",
        "Short (1-2 min)",
        "English",
        True,
        2
    ],
    [
        [],
        "https://www.motiong.ai/company/about-us",
        "Introduce MotionG to me in a fruitful way",
        "Fun",
        "Short (1-2 min)",
        "English",
        True,
        1
    ],
    [
        [],
        "https://www.motiong.ai/company/news-room/e3d5e3c8-59aa-41ce-98b1-fe7c44165049",
        "Tell me recent news of MotionG to me like I'm 5 years old",
        "Formal",
        "Short (1-2 min)",
        "English",
        True,
        8
    ]
]

EMPTY_EXAMPLE_DATA = [
    [],
    "",
    "",
    "Formal",
    "Short (1-2 min)",
    "English",
    True,
    0
]

UI_CACHE_EXAMPLES = False
UI_SHOW_API = True

CSS_STYLES = """
footer {
    visibility: hidden;
}
"""


ST_HIDE_HEADER_HTML = '''
    <style>
        header {visibility: hidden;}
'''

# [data-testid='stFileUploader'] {
#     display: flex;
#     flex-direction: column; /* Stack items vertically */
#     align-items: center; /* Center items horizontally */
#     width: 100%; /* Ensure the container takes full width */
# }

# [data-testid='stFileUploader'] section {
#     padding: 0;
#     display: flex;
#     justify-content: left; /* Centers the upload button */
# }

# [data-testid='stFileUploader'] section > input + div {
#     display: none; /* Hide the default file display */
# }

# [data-testid='stFileUploader'] section + div {
#     padding-top: 2px;
#     margin-top: 10px; /* Space between button and file display */
#     width: 100%; /* Ensures the file display takes the full width */
# }




ST_MAINPAGE_TITLE_HTML = """
<div style="display: flex; justify-content: center; align-items: center; height: 50vh; text-align: center; flex-direction: column;">
    <h1 style="font-size: 4rem; font-weight: bold; color: #2b2b2b; font-family: Arial, sans-serif; margin-bottom: 20px;">
        NotebookLM 
        <span style=" display: inline-block; background-color: red; color: white; padding: 5px 15px; border-radius: 15px;
            font-size: 1.5rem; font-weight: bold; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); position: relative; top: -20px;">
            Plus
        </span>
    </h1>
   <ul style="list-style-type: none; padding: 0; text-align: left; font-size: 1.25rem; color: #333; line-height: 1.8;">
        <li style="margin-bottom: 15px; padding: 10px 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
            <strong>Upload a file or set a link:</strong> Make sure the reference content you upload is less than 10,000 characters.
        </li>
        <li style="margin-bottom: 15px; padding: 10px 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
            <strong>Click the "Start" button:</strong> Begin the blog conversation generation.
        </li>
        <li style="margin-bottom: 15px; padding: 10px 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
            <strong>Participate in the conversation:</strong> Ask questions and interact through the text input box below.
        </li>
        <li style="margin-bottom: 15px; padding: 10px 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
            <strong>Note:</strong> Allowing the browser to use the microphone is required for voice input.<br> HTTP solutions for <a href="https://stackoverflow.com/questions/52759992/how-to-access-camera-and-microphone-in-chrome-without-https">Chorme</a>
            and <a href="https://blog.csdn.net/baidu_31788709/article/details/125652048#:~:text=Microsoft%20Edge%E7%BD%91%E9%A1%B5%E8%B0%83%E7%94%A8%E6%91%84%E5%83%8F%E5%A4%B4%E5%A4%B1%E8%B4%A5%EF%BC%88%E8%AE%BE%E7%BD%AE%E6%9D%83%E9%99%90%E5%A4%84%E6%8C%89%E9%92%AE%E4%B8%BA%E7%81%B0%E8%89%B2%E4%B8%8D%E5%8F%AF%E4%BF%AE%E6%94%B9%EF%BC%89%E7%9A%84%E5%8E%9F%E5%9B%A0%E5%92%8C%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95%201%20%E6%B5%8F%E8%A7%88%E5%99%A8%E8%AE%BF%E9%97%AE%20edge%3A%2F%2Fflags%EF%BC%8C%E8%BF%9B%E5%85%A5%E9%85%8D%E7%BD%AE%E7%95%8C%E9%9D%A2%E3%80%82%202%20%E6%90%9C%E7%B4%A2%E5%85%B3%E9%94%AE%E5%AD%97%20Insecure.,http%3A%2F%2Ftest.com%E3%80%82%206%20%E5%9C%A8%E7%A9%BA%E7%99%BD%E5%A4%84%E7%82%B9%E5%87%BB%E4%B8%80%E4%B8%8B%EF%BC%8C%E5%B0%B1%E4%BC%9A%E6%8F%90%E7%A4%BA%E6%98%AF%E5%90%A6%E7%94%9F%E6%95%88%EF%BC%8C%E7%94%9F%E6%95%88%E9%9C%80%E8%A6%81%E9%87%8D%E5%90%AF%E4%B9%8B%E7%B1%BB%E7%9A%84%E6%8F%90%E7%A4%BA%E3%80%82%207%20%E8%BF%99%E6%97%B6%E5%80%99%E5%86%8D%E5%8E%BB%E6%B5%8F%E8%A7%88%E5%99%A8%E5%8F%B3%E4%B8%8A%E8%A7%92%E2%80%9C%E2%80%A6%E2%80%9D%EF%BC%8C%E9%80%89%E6%8B%A9%20%E8%AE%BE%E7%BD%AE%20-%3E%20Cookie%E5%92%8C%E7%BD%91%E7%AB%99%E6%9D%83%E9%99%90%EF%BC%8C%E7%82%B9%E5%BC%80%E7%AB%99%E7%82%B9%EF%BC%8C%E5%B0%B1%E5%8F%AF%E4%BB%A5%E7%9C%8B%E5%88%B0%E8%AF%A5%E7%AB%99%E7%82%B9%E7%9A%84%E6%9D%83%E9%99%90%E5%8F%AF%E9%80%89%E4%BA%86%EF%BC%8C%E4%B9%8B%E5%89%8D%E6%91%84%E5%83%8F%E5%A4%B4%E7%AD%89%E6%8C%89%E9%92%AE%E9%83%BD%E6%98%AF%E7%81%B0%E8%89%B2%E7%9A%84%E3%80%82">Edge</a>.
        </li>
    </ul>
</div>

"""

ST_MAINPAGE_TITLE_TOP_HTML = """
<div style="display: flex; justify-content: center; align-items: center; text-align: center; flex-direction: column;">
    <h1 style="font-size: 4rem; font-weight: bold; color: #2b2b2b; font-family: Arial, sans-serif; margin-bottom: 20px;">
        NotebookLM 
        <span style=" display: inline-block; background-color: gold; color: white; padding: 5px 15px; border-radius: 15px;
            font-size: 1.5rem; font-weight: bold; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); position: relative; top: -20px;">
            Plus
        </span>
    </h1>
</div>
"""