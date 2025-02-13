from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from pdf_parse import resume_texts
import json
import re
from dotenv import load_dotenv 
import time
from datetime import datetime
from pymongo import MongoClient
import os

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)



db = client['Resume']  # database name
collection = db['Candidate']  # collection name


llm = OllamaLLM(model="deepseek-r1:7b",temperature=0.1)
# llm = OllamaLLM(model="llama2")
print(resume_texts)

prompt = PromptTemplate(
    input_variables=["resume_text"],
    template="""
      You are a resume parser. Your job is to extract key details from resumes and output them in JSON format. Here is an example:
```json
{{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "location": "City, State, Country",
    "highest_qualification":"MS",
    "marital_status":"single",
    "current_company":[
        {{
            "company_name": "Google"
            "designation": "Product Manger"
            "duration": "2021-present"
        }}
    ],
    "skills": ["Python", "Machine Learning", "Data Analysis"],
    "experience": [
        {{
            "role": "Software Engineer",
            "company": "ABC Corp",
            "duration": "Jan 2022 - Present"
        }}
    ]
}}
If a field is not present in the text ,set it to  null.
ONLY return FIELDS name,email,phone,location,highest_qualification,marital_status,current_company,education,skills,experience.
Please produce result in json format so that it can be extracted through regex and stored in a DB.
Resume text: {resume_text} """
)

print(f"Found {len(resume_texts)} resumes to process")

for i, resume_text in enumerate(resume_texts, 1):
    print(f"\n=== Processing Resume {i} ===")
    
    start_time = time.time()  # Start time for processing

    chain = prompt | llm
    result = chain.invoke({"resume_text": resume_text})  # This should send one resume at a time
    
    try:
        print(result)
        
        # Extract JSON block using regex
        json_match = re.search(r"```json\n(.*?)\n```", result, re.DOTALL)
        if json_match:
            json_string = json_match.group(1)  # Extract the JSON string
            
            
            parsed_result = json.loads(json_string)
            
            required_fields = ["name", "email", "phone", "location", "highest_qualification", 
                               "marital_status", "current_company", "education", "skills", "experience"]
            for field in required_fields:
                if field not in parsed_result:
                    parsed_result[field] = None
            
            parsed_result['timestamp'] = datetime.now().isoformat()  # Convert to ISO format string
            
            
            collection.insert_one(parsed_result)
            print(f"Successfully processed and stored resume {i}")
        else:
            print(f"No JSON block found in result for resume {i}")
    
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format for resume {i}: {e}")
    except Exception as e:
        print(f"Error processing resume {i}: {e}")   
    
    end_time = time.time()  # End time for processing
    processing_time = end_time - start_time  
    print(f"Time taken to process resume {i}: {processing_time:.2f} seconds")

print(f"\nProcessing complete")
#################################################################################
# from langchain_ollama import OllamaLLM
# from langchain.prompts import PromptTemplate
# from pdf_parse import chunked_resumes  # Import `chunked_resumes`
# import json
# import re
# import time
# from datetime import datetime
# from pymongo import MongoClient

# # MongoDB setup
# client = MongoClient('')
# db = client['Resume']  # Database name
# collection = db['Candidate']  # Collection name

# # LLM setup
# llm = OllamaLLM(model="deepseek-r1:7b")
# print(chunked_resumes)

# # Prompt template
# prompt = PromptTemplate(
#     input_variables=["resume_text"],
#     template="""
#       You are a resume parser. Your job is to extract key details from resumes and output them in JSON format. Here is an example:
# ```json
# {{
#     "name": "John Doe",
#     "email": "john.doe@example.com",
#     "phone": "+1234567890",
#     "location": "City, State, Country",
#     "highest_qualification":"MS",
#     "marital_status":"single",
#     "current_company":[
#         {{
#             "company_name": "Google"
#             "designation": "Product Manger"
#             "duration": "2021-present"
#         }}
#     ],
#     "skills": ["Python", "Machine Learning", "Data Analysis"],
#     "experience": [
#         {{
#             "role": "Software Engineer",
#             "company": "ABC Corp",
#             "duration": "Jan 2022 - Present"
#         }}
#     ]
# }}
# If a field is not present in the text let it be empty or null.
# ONLY return FIELDS name,email,phone,location,highest_qualification,marital_status,current_company,education,skills,experience.
# Please produce result in json format so that it can be extracted through regex and stored in a DB.
# Resume text: {resume_text} """)

# print(f"Found {len(chunked_resumes)} resumes to process")

# # Process resumes
# for i, resume_data in enumerate(chunked_resumes, 1):
#     name = resume_data["name"]  # Resume source name
#     resume_text = resume_data["resume"]  # Extract the resume text

#     print(f"\n=== Processing Resume {i}: {name} ===")
#     start_time = time.time()  # Start time for processing

#     # Build chain
#     chain = prompt | llm
#     try:
#         # Invoke the chain with resume text
#         result = chain.invoke({"resume_text": resume_text})
#         print(result)

#         # Extract JSON block using regex
#         json_match = re.search(r"```json\n(.*?)\n```", result, re.DOTALL)
#         if json_match:
#             json_string = json_match.group(1)  # Extract the JSON string

#             parsed_result = json.loads(json_string)
#             parsed_result['timestamp'] = datetime.now().isoformat()  # Add a timestamp
#             parsed_result['source_name'] = name  # Include the source name

#             # Store result in MongoDB
#             collection.insert_one(parsed_result)
#             print(f"Successfully processed and stored resume {i}: {name}")
#         else:
#             print(f"No JSON block found in result for resume {i}: {name}")

#     except json.JSONDecodeError as e:
#         print(f"Invalid JSON format for resume {i}: {name}, Error: {e}")
#     except Exception as e:
#         print(f"Error processing resume {i}: {name}, Error: {e}")

#     end_time = time.time()  # End time for processing
#     processing_time = end_time - start_time
#     print(f"Time taken to process resume {i}: {processing_time:.2f} seconds")
