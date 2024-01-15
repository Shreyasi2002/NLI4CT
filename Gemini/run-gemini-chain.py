import os
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
import json

from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

console = Console()

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  }
]

model = genai.GenerativeModel("gemini-pro", safety_settings=safety_settings, generation_config={"temperature":0.3})

data = json.load(open('../training-data/test.json'))
data_expanded = []
for _id, value in data.items():
    temp = {}
    temp["id"] = _id
    sec_id = value.get("Secondary_id")
    temp["section_id"] = value["Section_id"]
    temp["statement"] = value["Statement"]
    temp["primary_id"] = value["Primary_id"]
    if sec_id is not None:
        temp["secondary_id"] = sec_id

    data_expanded.append(temp)


CT_files = os.listdir("../training-data/CT_json")
CT_files_data = {}
for file in CT_files:
    if file == ".DS_Store":
        CT_files.remove(file)
        continue

    path = f"../training-data/CT_json/{file}".encode('latin-1')
    path = path.decode('utf-8')
    content = json.load(open(path))
    CT_files_data[file[:-5]] = content

samples = []
for sample in data_expanded:
    primary_evidence = "".join(CT_files_data[sample['primary_id']][sample['section_id']])
    sentence = f"For the primary trial participants, \n\n {primary_evidence}"
    secondary_evidence = sample.get("secondary_id")
    if secondary_evidence:
        secondary_evidence = "".join(CT_files_data[sample['secondary_id']][sample['section_id']])
        sentence = f"{sentence}\n For the secondary trial participants, \n\n{secondary_evidence}"
    temp = {"id": sample['id'], "clinical_trial":sentence, "hypothesis":sample['statement']}
    samples.append(temp)


def get_question(context, question):
    template = f"""
        Imagine three different clinical experts are answering the question given below.
        All experts will write down first step of their thinking, then share it with the group.
        Then all experts will go on to the next step of their thinking.
        If any expert realises they're wrong at any point then they leave.
        Continue till a definite conclusion is reached.

        Incorporate information from the context given below into the evaluation process. 
        Cross-reference the model's responses with relevant details from the context to 
        enhance the accuracy of interpretation.

        Give a final conclusion after assessing the logical consistency within the model's responses.

        CONTEXT: {context}

        QUESTION: Does the statement {question} contradict or support the context? Give a step by step explanation of your thinking.
        
    """
    return template

FINAL_QUESTION = '''
Based on the comprehensive evaluation of the model's responses and the given context, hypothesis and logical analysis, 
does the given hypothesis support the context or not? Write one word answer - Yes or No.
'''

# function to add to JSON
def write_json(id, new_data, filename='./Gemini_results.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[id] = new_data
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


count = 2221
for sample in samples[count:]:
    count += 1
    
    print("\n############################################\n")
    print(f"-------Running for sample {count} : {sample['id']} --------\n")

    prediction = {}

    chat = model.start_chat()

    def get_chat_response(chat: genai.ChatSession, prompt: str) -> str:
        response = chat.send_message(prompt)
        return response.text

    question = get_question(sample['clinical_trial'], sample['hypothesis'])
    explanation = get_chat_response(chat, question)

    answer = get_chat_response(chat, FINAL_QUESTION)

    console.print(Markdown(explanation))
    print("\n")
    console.print(Markdown(answer))
    print("\n")
    prediction["explanation"] = explanation
    prediction["answer"] = answer
    write_json(sample['id'], prediction)