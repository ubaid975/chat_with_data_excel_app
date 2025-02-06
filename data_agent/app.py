import os
from langchain_experimental.agents import create_csv_agent,create_pandas_dataframe_agent
from langchain.prompts import ChatMessagePromptTemplate,ChatPromptTemplate,PromptTemplate
import pandas as pd
from langchain_groq import ChatGroq

import langchain
import gradio as gr


llm=ChatGroq(api_key=os.getenv('groq_api'))




# df=pd.read_csv('customer_churn_data.csv')
# template=ChatPromptTemplate.from_messages(
#     [('system','you are a helpful data agent perform task only analyze data you cannot perform create update and delete')
#     ,('human','{input}')]
# )

# agent=create_pandas_dataframe_agent(llm=llm,df=df,allow_dangerous_code=True)
# chain=template|agent
# print(chain.invoke({'input':'please delete one column'})['output'])

def csv_agent(file_path,query):
    if file_path:
      
      
        if file_path.endswith('.csv'):
            df=pd.read_csv(file_path)
            try:
                agent=create_pandas_dataframe_agent(llm=llm,df=df,allow_dangerous_code=True,handle_parsing_errors=True)
                agent.handle_parsing_errors=True
                if query:
                    reponse=agent.run(query)
                    return reponse
                else:
                    return 'query not found'
            except Exception as e:
                return str(e)
        elif file_path.endswith('.xlsx'):
            df=pd.read_excel(file_path)
            try:
                agent=create_pandas_dataframe_agent(llm=llm,df=df,allow_dangerous_code=True,handle_parsing_errors=True)
                agent.handle_parsing_errors=True
                if query:
                    reponse=agent.run(query)
                    return reponse
                else:
                    return 'query not found'
            except Exception as e:
                return str(e)
        elif file_path.endswith('.json'):
            df=pd.read_json(file_path)
            try:
                agent=create_pandas_dataframe_agent(llm=llm,df=df,allow_dangerous_code=True,handle_parsing_errors=True)
                if query:
                    reponse=agent.run(query)
                    return reponse
                else:
                    return 'query not found'
            except Exception as e:
                return str(e)
        
            
        else:
            return 'only file format are allowed csv excel and json'
    else:
        return 'file not found '

app=gr.Interface(fn=csv_agent,inputs=[gr.File(file_types=['.csv','.xlsx','.json']),gr.TextArea(placeholder='enter your query')],outputs=gr.TextArea(),title='Talking Data Agent',description='Use the the file format only xlsx csv and json',theme=gr.themes.Citrus())
app.launch(share=True)