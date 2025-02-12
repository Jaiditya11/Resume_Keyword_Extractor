from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from pdf_parse import resume_texts
import json
import re
import time
from datetime import datetime
from pymongo import MongoClient




client = MongoClient('mongodb+srv://jaidityanair10:Jaiditya123@cluster0.dazhe.mongodb.net/')
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
##############################################################################################
# import os
# import time
# import json
# import re
# from datetime import datetime
# from PyPDF2 import PdfReader
# from docx import Document
# from langchain_ollama import OllamaLLM
# from langchain.prompts import PromptTemplate
# from pymongo import MongoClient

# def extract_resume_texts(directory='data'):
#     """
#     Extract text from PDF and Word resumes in the specified directory.
#     Yields one resume text at a time.
#     """
#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
        
#         # Process PDF files
#         if filename.endswith('.pdf'):
#             try:
#                 reader = PdfReader(file_path)
#                 text = ''
#                 for page in reader.pages:
#                     text += page.extract_text()
#                 yield filename, text
#             except Exception as e:
#                 print(f"Error processing PDF {filename}: {str(e)}")
        
#         # Process Word (.docx) files
#         elif filename.endswith('.docx'):
#             try:
#                 doc = Document(file_path)
#                 text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
#                 yield filename, text
#             except Exception as e:
#                 print(f"Error processing Word file {filename}: {str(e)}")

# def process_resumes(directory='data', model="deepseek-r1:7b"):
#     # MongoDB Connection
#     client = MongoClient('mongodb+srv://jaidityanair10:Jaiditya123@cluster0.dazhe.mongodb.net/')
#     db = client['Resume']  # database name
#     collection = db['Candidate']  # collection name

#     # LLM Setup
#     llm = OllamaLLM(model=model)

#     # Prompt Template
#     prompt = PromptTemplate(
#         input_variables=["resume_text"],
#         template="""Extract information from the resume text in a structured JSON format. 
# Provide accurate and concise details. If information is not found, use empty strings or empty lists.

# Resume Text:
# {resume_text}

# Output Format:
# {{
#     "name": "",
#     "email": "",
#     "phone": "",
#     "skills": [],
#     "education": [
#         {{
#             "degree": "",
#             "institution": "",
#             "year": ""
#         }}
#     ],
#     "professional_experience": [
#         {{
#             "company": "",
#             "position": "",
#             "duration": ""
#         }}
#     ]
# }}

# Provide ONLY the JSON output without any additional text or explanation."""
#     )

#     # Process Resumes
#     total_resumes = 0
#     successful_resumes = 0
#     failed_resumes = 0

#     for filename, resume_text in extract_resume_texts(directory):
#         total_resumes += 1
#         print(f"\n=== Processing Resume: {filename} ===")
        
#         start_time = time.time()

#         try:
#             # Create processing chain
#             chain = prompt | llm
#             result = chain.invoke({"resume_text": resume_text})
            
#             # Try multiple ways to parse the JSON
#             parsing_methods = [
#                 # Try direct JSON parsing
#                 lambda r: json.loads(r),
                
#                 # Try extracting JSON from between curly braces
#                 lambda r: json.loads(re.search(r'{.*}', r, re.DOTALL).group(0)),
                
#                 # Try parsing JSON block if present
#                 lambda r: json.loads(r.split('```json')[-1].split('```')[0] if '```json' in r else r)
#             ]
            
#             parsed_result = None
#             for method in parsing_methods:
#                 try:
#                     parsed_result = method(result)
#                     break
#                 except Exception:
#                     continue
            
#             if not parsed_result:
#                 raise ValueError("Could not parse JSON")
            
#             # Add metadata
#             parsed_result['filename'] = filename
#             parsed_result['timestamp'] = datetime.now().isoformat()
            
#             # Insert into MongoDB
#             collection.insert_one(parsed_result)
#             successful_resumes += 1
#             print(f"Successfully processed: {filename}")
#             print(f"Extracted Data: {parsed_result}")
        
#         except json.JSONDecodeError as e:
#             failed_resumes += 1
#             print(f"Invalid JSON format for {filename}: {e}")
#             print(f"Problematic result: {result}")
#         except Exception as e:
#             failed_resumes += 1
#             print(f"Error processing {filename}: {e}")
#             print(f"Raw LLM output: {result}")
        
#         end_time = time.time()
#         processing_time = end_time - start_time
#         print(f"Time taken to process {filename}: {processing_time:.2f} seconds")

#     # Summary
#     print("\n--- Processing Summary ---")
#     print(f"Total Resumes: {total_resumes}")
#     print(f"Successfully Processed: {successful_resumes}")
#     print(f"Failed to Process: {failed_resumes}")

# # Run the processing
# if __name__ == "__main__":
#     process_resumes(directory='data')

#########################################################################
# from langchain_ollama import OllamaLLM
# from langchain.prompts import PromptTemplate
# from pdf_parse import chunked_resumes  # Import `chunked_resumes`
# import json
# import re
# import time
# from datetime import datetime
# from pymongo import MongoClient

# # MongoDB setup
# client = MongoClient('mongodb+srv://jaidityanair10:Jaiditya123@cluster0.dazhe.mongodb.net/')
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
