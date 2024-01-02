import streamlit as st
import requests
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="Ecoact Dashboard App", 
    page_icon=":smiley:",
    layout="wide",
)

st.title("Ecoact Dashboard App")

# Load data
def load_data():
    r = requests.get('http://127.0.0.1:8000/ef/')
    json_data = r.json()
    df = pd.DataFrame.from_dict(json_data)

    return df

# Load data from csv
def load_csv_data():
    df = pd.read_csv("clean_data.csv")
    return df

# Generate LLM response
def generate_response(input_query):
  llm = ChatOpenAI(model_name='gpt-3.5-turbo-1106', temperature=0.2, openai_api_key=openai_api_key)
  # Load Data via api
#   df = load_data()
  # Load Data via csv
  df = load_csv_data()
  # Create Pandas DataFrame Agent
  agent = create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)
  # Perform Query using the Agent
  response = agent.run(input_query)
  return st.success(response)

# dashboard title
st.title("Data QA with LLM")

st.text("Sample questions:")
st.text("what is the average of CH4f where Cat1 is Combustibles?")
st.text("what is the highest value of CO2f which has belong to Fossiles in Cat2?")

query_text = st.text_area('Ask me a question')
openai_api_key = "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"

# App logic
if not openai_api_key.startswith('sk-'):
  st.warning('Incorrect OpenAI API key!', icon='⚠')
if openai_api_key.startswith('sk-'):
  st.header('Output')
  generate_response(query_text)

# st.dataframe(df, use_container_width=True, hide_index=True)