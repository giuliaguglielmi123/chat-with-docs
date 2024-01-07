# 💁 Chatbot for Interacting with Your Books 📝
## Introduction

🤖 Welcome to my chatbot, a unique tool designed for engaging conversations with books. This chatbot leverages the OpenAI API to interact specifically with an amazing book, "The Almanack of Naval Ravikant." I used Streamlit to develop the graphical interface, Langchain for the QA chain, and Chroma as the vector database. While it's primarily tailored for books, you can easily adapt it to engage with various types of content.

![Alt text](<Screenshot 2024-01-07 202455.png>)

## Features

1. Generates responses based on a book written by Naval Ravikant.
2. Allows users to provide feedback with a thumbs up or down.
3. Stores user feedback in a JSON file for historical analysis.
4. Cites sources for the information provided in responses.

## Requirements

- OpenAI API key with access to Large Language Models.

## Installation

1. Clone the repository:
git clone https://github.com/your-username/your-repository.git

2. Create a virtual environment:
python -m venv .venv_chatbot
.venv_chatbot\Scripts\activate

3. Install the required Python packages:
pip install -r requirements.txt

4. Set up your OpenAI API key. Create a `.env` file in the root directory of the project with your API key:

5. Run the Streamlit app:
streamlit run app.py


## Customize the Document

To test with a personalized document, please replace the files in the `docs` directory.

## Usage

1. Type your query into the input box and press enter.
2. After receiving the response, provide feedback by clicking the thumbs up or down button.
3. Review the sources cited in the response.

## Contributions

📝 Contributions are welcome! If you have suggestions for improvements, please feel free to submit a pull request.

### Additional Notes

Before running `streamlit run app.py`, I installed `chromadb`. For this specific package, I needed to visit "Microsoft C++ Build Tools" and install all necessary components to compile C++ projects.

