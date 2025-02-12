
# import ollama
# from pydantic import BaseModel
# from typing import List, Optional

# # Define schema for structured output
# class ResumeInfo(BaseModel):
#     name: Optional[str]
#     email: Optional[str]
#     phone: Optional[str]
#     skills: List[str]
#     education: List[str]
#     experience: List[str]
#     current_company: Optional[str]
#     current_designation: Optional[str]
#     marital_status: Optional[str]

# response = ollama.chat(
#     messages=[
#         {
#             'role': 'user',
#             'content': '''
#             Extract structured information from this resume text:
#             CURRICULUM VITAE \n \nAMIT KUMAR MAHAR \n# 1860 sector 4 Part-2, KARNAL \nMobile no: +91-9729902324 \namitmahar25@gmail.com \n \nCareer Objective \n \nTo build a successful career in a challenging and creative environment that will allow me to explore \nmy abilities and elevate myself to the role assigned to me. \n \nProfile \n \n1. Learning Proficiency to acquire and apply new knowledge and skills. \n2. Extensive exposure to comprehensive range of team management activities, thrive on working \nin diverse teams and challenging environment. \n3. A self \u2013 starter with a can- do attitude, I think on my feet, look at challenges as opportunities, \nextremely productive in a high volume, high stress environment. \n \nExperience- \n1. Worked as Unit Manager in Niva Bupa Health Insurance (13 July 2022 to 3 December 2022)  \n2. Worked in Mahindra Automobiles as Sale Executive (22 February 2022 to 30 June 2022) \n3. Worked in Edelweiss Tokio Life Insurance as Agent (26 November 2019 to 20 july 2022)  \n4. Worked in Ply Wood Company as Sales Executive 1 year (10 December 2020 to 15 \nJanuary 2021) \n5. Worked in AVI Suzuki as Sales Executive 1 year (1 August 2019 to 21 October 2020) \n6. Worked as Sales Executive in idea 1 year 8 months (17 November 2017 to 5 July 2019) \n7. Worked as Sales Manager in Burger Uncle 3 year (1 April 2014 to 24 October 2017) \n \nEducation Qualification: \n\u2022 Passed BA from MDU. \n\u2022 Class XII Passed from SD MODEL PUBLIC SCHOOL KARNAL. \n\u2022 Matriculation from SARASWATI  VIDYA MANDIR. \nTechnical Skill: \n \n\u2022 Knowledge of Basic Computer. \nKey Strength: \n \n\u2022 Confidence \n\u2022 Hard work \n\u2022 Ability to do work in a team as well as individually.Hobbies: \n \nListening Music and Traveling \n \n \nPersonal Profile \n \nName : AMIT KUMAR MAHAR \n \nFather : SH. RAMESH KUMAR MAHAR \n \nMarital Status : Married \n \nNationality : Indian \n \nHobbies : Traveling & Listening Music. \nDate of Birth : 25.12.1988 \nLanguage- : Hindi, English \n \n \nPlace:\u2026\u2026\u2026\u2026\u2026  \nSIGNATURE \n \nDate:\u2026\u2026\u2026\u2026\u2026
#             ''',
#         }
#     ],
#     model='llama3.1:8b',
#     format=ResumeInfo.model_json_schema(),
# )

# resume_info = ResumeInfo.model_validate_json(response.message.content)
# print(resume_info)

###########################################################################################################
# import ollama
# from pydantic import BaseModel
# from typing import List, Optional
# from pymongo import MongoClient
# from datetime import datetime
# from pdf_parse import resume_texts
# import time

# # Define schema for structured output
# class ResumeInfo(BaseModel):
#     name: Optional[str]
#     email: Optional[str]
#     phone: Optional[str]
#     location: Optional[str]
#     highest_qualification: Optional[str]
#     marital_status: Optional[str]
#     current_company: Optional[List[dict]]
#     education: Optional[List[str]]
#     skills: Optional[List[str]]
#     experience: Optional[List[dict]]

# # Connect to MongoDB
# client = MongoClient('mongodb+srv://jaidityanair10:Jaiditya123@cluster0.dazhe.mongodb.net/')
# db = client['Resume']  # Database name
# collection = db['Candidate']  # Collection name

# print(f"Found {len(resume_texts)} resumes to process")

# for i, resume_text in enumerate(resume_texts, 1):
#     print(f"\n=== Processing Resume {i} ===")
#     start_time = time.time()
    
#     response = ollama.chat(
#         messages=[
#             {
#                 'role': 'user',
#                 'content': f"""
#                 Extract structured information from this resume text:
#                 {resume_text}
#                 """,
#             }
#         ],
#         model='llama3.1:8b',
#         format=ResumeInfo.model_json_schema(),
#     )
    
#     try:
#         resume_info = ResumeInfo.model_validate_json(response.message.content)
#         resume_dict = resume_info.model_dump()
#         resume_dict['timestamp'] = datetime.now().isoformat()
        
#         collection.insert_one(resume_dict)
#         print(f"Successfully processed and stored resume {i}")
#     except Exception as e:
#         print(f"Error processing resume {i}: {e}")
    
#     end_time = time.time()
#     print(f"Time taken to process resume {i}: {end_time - start_time:.2f} seconds")

# print("\nProcessing complete")

#####################################################################################################

# import ollama
# from pydantic import BaseModel
# from typing import List, Optional
# from pymongo import MongoClient
# from datetime import datetime
# from pdf_parse import resume_texts
# import time

# # Define schema for structured output
# class CompanyInfo(BaseModel):
#     name: Optional[str] = None
#     position: Optional[str] = None
#     duration: Optional[str] = None
#     responsibilities: Optional[List[str]] = None

# class ResumeInfo(BaseModel):
#     name: Optional[str]
#     email: Optional[str]
#     phone: Optional[str]
#     location: Optional[str]
#     highest_qualification: Optional[str]
#     marital_status: Optional[str]
#     current_company: Optional[List[CompanyInfo]]
#     education: Optional[List[str]]
#     skills: Optional[List[str]]
#     experience: Optional[List[CompanyInfo]]

# # Connect to MongoDB
# client = MongoClient('mongodb+srv://jaidityanair10:Jaiditya123@cluster0.dazhe.mongodb.net/')
# db = client['Resume']  # Database name
# collection = db['Candidate']  # Collection name

# print(f"Found {len(resume_texts)} resumes to process")

# for i, resume_text in enumerate(resume_texts, 1):
#     print(f"\n=== Processing Resume {i} ===")
#     start_time = time.time()
    
#     response = ollama.chat(
#         messages=[
#             {
#                 'role': 'user',
#                 'content': f"""
#                 Extract structured information from this resume text:
#                 {resume_text}
#                 """,
#             }
#         ],
#         model='llama3.1:8b',
#         format=ResumeInfo.model_json_schema(),
#     )
    
#     try:
#         resume_info = ResumeInfo.model_validate_json(response.message.content)
#         resume_dict = resume_info.model_dump()
#         resume_dict['timestamp'] = datetime.now().isoformat()
        
#         collection.insert_one(resume_dict)
#         print(f"Successfully processed and stored resume {i}")
#     except Exception as e:
#         print(f"Error processing resume {i}: {e}")
    
#     end_time = time.time()
#     print(f"Time taken to process resume {i}: {end_time - start_time:.2f} seconds")

# print("\nProcessing complete")
#####################################################################################################
import ollama
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from datetime import datetime
from pdf_parse import resume_texts
import time
from dateutil import parser


# Define schema for structured output
class CompanyInfo(BaseModel):
    name: Optional[str]
    position: Optional[str]
    duration: Optional[str]
    responsibilities: Optional[List[str]]

class ResumeInfo(BaseModel):
    candidate_name: Optional[str]
    email: Optional[str]
    phone_no: Optional[str]
    location: Optional[str]
    highest_qualification: Optional[str]
    marital_status: Optional[str]
    current_company: Optional[CompanyInfo]  # Stores the most recent company
    education: Optional[List[str]]
    skills: Optional[List[str]]
    experience: Optional[List[CompanyInfo]]

# Connect to MongoDB
client = MongoClient('mongodb+srv://jaidityanair10:Jaiditya123@cluster0.dazhe.mongodb.net/')
db = client['Resume']  # Database name
collection = db['Candidate']  # Collection name

print(f"Found {len(resume_texts)} resumes to process")

for i, resume_text in enumerate(resume_texts, 1):
    print(f"\n=== Processing Resume {i} ===")
    start_time = time.time()
    
    response = ollama.chat(
        messages=[
            {
                'role': 'user',
                'content': f"""
                Extract structured information from this resume text:
                Add the most recent experience according to date in current_comapny.
                {resume_text}
                """,
            }
        ],
        model='qwen2.5-coder',
        format=ResumeInfo.model_json_schema(),
    )
    # def extract_end_date(duration: str) -> datetime: 
    #     try:
    #         if "till date" in duration.lower():
    #             return datetime.today()  # Assume it's the current job
    #         return parser.parse(duration.split(" to ")[-1])  # Extract end date
    #     except Exception:
    #        return datetime.min  # Default to the earliest date if parsing fails
 
 
    try:
        resume_info = ResumeInfo.model_validate_json(response.message.content)
        resume_dict = resume_info.model_dump()
        resume_dict['timestamp'] = datetime.now().isoformat()

        
        collection.insert_one(resume_dict)
        print(f"Successfully processed and stored resume {i}")
    except Exception as e:
        print(f"Error processing resume {i}: {e}")
    
    end_time = time.time()
    print(f"Time taken to process resume {i}: {end_time - start_time:.2f} seconds")

print("\nProcessing complete")


