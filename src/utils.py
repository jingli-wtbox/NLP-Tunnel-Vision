from pydantic import BaseModel
from typing import Any

SYSTEM = 0
USER = 1
ASSISTANT = 2

OBJECT_FILE = "file"
OBJECT_FINE_TUNE = "fine_tuning.job"

SYSTEM_PROMPT = "You are a helpful AI assistant. Your job is to generate a personalized comment for the given article and user reading history and comment history."
USER_PROMPT = """As a news reader, your reading history and comment history are provided. Please detect the reading preference and generate a new personalized comment (around 100 words) for a new article based on historical reading and comment."""
ASSISTANT_PROMPT = "{new_comment}"

OPENAI_MESSAGES_FINETUNE = [
    {"role": "system", "content": "{system_prompt}"},
    {"role": "user", "content": "{user_prompt}"},
    {"role": "assistant", "content": "{assistant_prompt}"}
]

OPENAI_MESSAGES_GENERATE = [
    {"role": "system", "content": "{system_prompt}"},
    {"role": "user", "content": "{user_prompt} \n##\nnew article: {new_article}\nnew comment:\n"},
]


class RequestBody(BaseModel):
    history: Any
    new_article: str

class OpenAIAPIKeyError(Exception):
    pass

class OpenAPIError(Exception):
    pass