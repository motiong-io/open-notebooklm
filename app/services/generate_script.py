from typing import Any, List, Union
from app.prompts import HISTORY_DIALOGUES, SYSTEM_PROMPT, QUESTION_MODIFIER, TONE_MODIFIER, LENGTH_MODIFIERS, LANGUAGE_MODIFIER,SYSTEM_PROMPT_FOR_USER
from app.constants import OPENAI_MODEL_ID, OPENAI_TEMPERATURE
from app.schema import DialogueItem, ShortDialogue, MediumDialogue
import openai
from app.config import env
import instructor


openai_client = openai.Client(api_key=env.openai_api_key, base_url=env.openai_base_url)
openai_client = instructor.from_openai(openai_client)

def call_llm(system_prompt: str, text: str, dialogue_format: Any) -> Any:
    """Call the LLM with the given prompt and dialogue format."""
    response = openai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        model=OPENAI_MODEL_ID,
        temperature=OPENAI_TEMPERATURE,
        response_model=dialogue_format,
    )
    return response


def generate_script(
    system_prompt: str,
    input_text: str,
    output_model: Union[ShortDialogue, MediumDialogue],
) -> Union[ShortDialogue, MediumDialogue]:
    """Get the dialogue from the LLM."""

    # Call the LLM for the first time
    first_draft_dialogue = call_llm(system_prompt, input_text, output_model)

    # Call the LLM a second time to improve the dialogue
    system_prompt_with_dialogue = f"{system_prompt}\n\nHere is the first draft of the dialogue you provided:\n\n{first_draft_dialogue.model_dump_json()}."
    final_dialogue = call_llm(system_prompt_with_dialogue, "Please improve the dialogue. Make it more natural and engaging.", output_model)

    return final_dialogue




def generate_init_script(question: str, tone: str, length: str, language: str, text: str):
    # Modify the system prompt based on the user input
    modified_system_prompt = SYSTEM_PROMPT

    if question:
        modified_system_prompt += f"\n\n{QUESTION_MODIFIER} {question}"
    if tone:
        modified_system_prompt += f"\n\n{TONE_MODIFIER} {tone}."
    if length:
        modified_system_prompt += f"\n\n{LENGTH_MODIFIERS[length]}"
    if language:
        modified_system_prompt += f"\n\n{LANGUAGE_MODIFIER} {language}."

    # Call the LLM
    if length == "Short (1-2 min)":
        llm_output = generate_script(modified_system_prompt, text, ShortDialogue)
    else:
        llm_output = generate_script(modified_system_prompt, text, MediumDialogue)

    return llm_output

def generate_modified_script(question: str, tone: str, length: str, language: str, text: str,history_dialogues:List[DialogueItem]):
    # Modify the system prompt based on the user input
    modified_system_prompt = SYSTEM_PROMPT_FOR_USER

    if history_dialogues:
        history_dialogues_str = ""
        for dia in history_dialogues:
            history_dialogues_str += dia.to_brief_str()+"\n"
        modified_system_prompt += f"\n\n{HISTORY_DIALOGUES} {history_dialogues_str}"

    if question:
        modified_system_prompt += f"\n\n{QUESTION_MODIFIER} {question}"
    if tone:
        modified_system_prompt += f"\n\n{TONE_MODIFIER} {tone}."
    if length:
        modified_system_prompt += f"\n\n{LENGTH_MODIFIERS[length]}"
    if language:
        modified_system_prompt += f"\n\n{LANGUAGE_MODIFIER} {language}."

    # Call the LLM
    if length == "Short (1-2 min)":
        llm_output = generate_script(modified_system_prompt, text, ShortDialogue)
    else:
        llm_output = generate_script(modified_system_prompt, text, MediumDialogue)

    return llm_output