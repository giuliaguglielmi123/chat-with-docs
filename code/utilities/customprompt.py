# flake8: noqa
from langchain.prompts import PromptTemplate

template = """{summaries}

You are a personal bot assistant for answer about answer prompt by users.
Please reply to the question using only the information present in the text above.
If you can't find it, do not invent anything and reply politely that the information is not in the knowledge base.
Respond in the same language detected.

Question: {question}
Answer:"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

EXAMPLE_PROMPT = PromptTemplate(
    input_variables=["page_content", "source"],
    template="Content: {page_content}\nSource: {source}",
)


