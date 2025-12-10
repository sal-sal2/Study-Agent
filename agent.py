"""
Docstring for agent. This file includes the code for our api
I plan to change the ai model to Google AI Studio (Gemini): Completely free for testing with Gemini models (like 2.5 Flash) 
"""
from langchain import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

#load_dotenv()


###functions for agent will call
#read 
@tool
def read_note(filepath):
    """Read the contents of the file"""
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            content = f.read()
        return f"Contents of '{filepath}' : \n{content}"
    except FileNotFoundError:
        return f"Error: file '{filepath}' not found"
    #store any errors in error
    except Exception as error:
        return f"Error reading file: {str(error)}"

#write to file
@tool
def write_note(filepath, content):
    """Write content to a text file. This will overwrite the content if file exists"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"successfully wrote {len(content)} to '{filepath}'"
    except Exception as error:
        return f"error writig to: '{filepath}'"
    

TOOLS = [read_note, write_note]

#first prompt agent will look at
SYSTEM_MESSAGE = """You are a helpful note-taking assistant.
You can read and write text files to help users manage their notes.
Be concise and helpful."""


#Initialize agent and LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_MESSAGE)

#run agent
def run_agent(user_input):
    """Run the agent with a user query and run the response."""
    try:
        result = agent.invoke(
            {"message": [{"role": "user", "content": user_input}]}, 
            config={"recursion_limit":50}
        )
        return result["message"][-1].content
    except Exception as error:
        return f"Error: {str(error)}"
    

print(run_agent("Hello, how are you!"))