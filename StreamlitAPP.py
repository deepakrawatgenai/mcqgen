import os
import json
import pandas as pd
from  dotenv import load_dotenv
from src.mcqgenerator.utills import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import traceback

with open('Response.json','r') as file:
    response_json=json.load(file)

st.title ("MCQ Application with  Lang Chain")

with st.form("user_inputs"):
    upload_file=st.file_uploader("Upload a file in pdf and txt format")
    mcq_count=st.number_input("No.of MCQ Question",min_value=3,max_value=50)
    subject=st.text_input("Insert Subject",max_chars=50)
    tone=st.text_input ("Complexity Level of Questions", max_chars=20,placeholder="Simple")
    button=st.form_submit_button("Create MCQ.")
    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading......."):
            try:
                text = read_file(upload_file)
                #https://python.langchain.com/docs/modules/model_io/llms/token_usage_tracking

        #How to setup Token Usage Tracking in LangChain
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject":subject,
                            "tone": tone,
                            "response_json": json.dumps(response_json)
                        }
                        )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                if isinstance(response,dict):
                    quiz=response.get("quiz",None)
                    if(quiz is not None):
                        table_data=get_table_data(quiz)
                        
                        if table_data is not None:                            
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in Table Data")
                else:
                    st.write(response)

