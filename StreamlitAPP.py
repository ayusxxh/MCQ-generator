import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open('C:\Users\ayush\last\Response.json', 'r') as file:
    RESPONSE_JSON= json.load(file)
    
st.title("mcq generation with langchain")

with st.form("user inputs"):
    uploaded_file= st.file_uploader("upload a pdf or text file")
    
    mcq_count= st.number_input("number of mcqs", min_value=3, max_value= 50)
    
    tone= st.text_input("compexity level:", max_chars=20, placeholder="Simple")
    
    subject= st.text_input("insert subject", max_chars=20)
    
    button= st.form_submit_button("create mcqs")
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("LOADING..."):
        try:
            text= read_file(uploaded_file)
            with get_openai_callback() as cb:
                response= generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json"= json.dumps(RESPONSE_JSON)
                    }
                )
                
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("error")
            
        else:
            print(f"total tokens:{cb.total_tokens}")
            print(f"prompt tokens:{cb.prompt_tokens}")
            print(f"completion tokens:{completion_tokens}")
            print(f"total cost:{cb.total_cost}")
            if isinstance(response, dict):
                quiz= response.get("quiz", None)
                if quiz is not None:
                    table_data= get_table_data(quiz)
                    if table_data is not None:
                        df= pd.DataFrame(table_data)
                        df.index= df.index+1
                        st.table(df )
                        st.text_area(label="Review", value= response["review"])
                    else:
                        st.error("error in the table data")
            else:
                st.write(response)
                
                
                    
           
            
            