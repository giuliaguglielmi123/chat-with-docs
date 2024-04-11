# 💁 Chatbot with stored feedbacks and source citation📝
## Introduction

🤖 Welcome to my chatbot! ask it any question and the information would be stored in a JSON file. Plus, if it finds any answers, it will return the sources. 

![Alt text](<img/screen_1.png>)

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

### Additional Notes for windows users

Before running `streamlit run app.py`, I installed `chromadb`. For this specific package, I needed to visit "Microsoft C++ Build Tools" and install all necessary components to compile C++ projects.

