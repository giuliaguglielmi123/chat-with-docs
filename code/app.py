from chat import get_semantic_answer_lang_chain
import streamlit as st
from streamlit_chat import message
import json
import re

# Creating the chatbot interface
st.title("Chatbot")

# Storing the chat: to preserve message generated or past message within the same session, if none return en empty list
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'chat_source_chunks' not in st.session_state:
    st.session_state['chat_source_chunks'] = []

if 'chat_source_documents' not in st.session_state:
    st.session_state['chat_source_documents'] = []

if "chat_question" not in st.session_state:
    st.session_state["chat_question"] = []


def store_feedback(question, answer, feedback):
    data={

        "question": question,
        "answer": answer,
        "feedback": feedback

    }
    # try to read the existing data
    try: # verify if the file doesn't exist or if it isn't correct 
        with open("feedback.json", mode="r", encoding="utf-8") as f:
            existing_data = json.load(f)
            if not isinstance(existing_data, list):
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    # Write updated data back to the file
    with open("feedback.json", mode="w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)


# Function to clean all
def clear_chat_data():
    st.session_state['past'] = [] # history chat
    st.session_state['generated'] = []
    st.session_state['chat_source_chunks'] = []
    st.session_state['chat_source_documents'] = []
    st.session_state['chat_question'] = []


# button to clear all
clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)

user_input = st.text_input("Ask your Question", key="input")


if user_input: # did user ask a question ?
        

    st.session_state['chat_question'], result, sources, source_chunks = get_semantic_answer_lang_chain(user_input, st.session_state['past']) # generate the answer
    

    st.session_state['chat_source_documents'].append(sources)
    st.session_state['past'].append((st.session_state['chat_question'], result)) # question - answer
    st.session_state["chat_source_chunks"] = source_chunks


history_range = range(len(st.session_state['past'])-1, -1, -1) # start, stop, steps

if st.session_state['past']: # is there any history?
    for i in range(len(st.session_state['past'])-1, -1, -1):
        if i == history_range.start:
            # Feedback buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button('👍'):
                    store_feedback(st.session_state['past'][i][0], st.session_state['past'][i][1], 'up')
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button('👎'):
                    store_feedback(st.session_state['past'][i][0], st.session_state['past'][i][1], 'down')
                    st.error("Thank you for your feedback!")



        answer_with_citations = re.sub(r'\$\^\{(.*?)\}\$', r'(\1)', st.session_state['past'][i][1])
        message(st.session_state["past"][i][0], key=str(i)) # zero gets the question 
        message(answer_with_citations, is_user=True, key=str(i) + '_user') # one gets the answer
        st.markdown(f'\n\nSources: {st.session_state["chat_source_documents"][i]}') # this add the resource


