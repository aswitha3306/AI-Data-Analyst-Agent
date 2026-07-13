import os
import google.generativeai as genai
from dotenv import load_dotenv
from router import route_question

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_agent(question, df):
    """
    Agent that:
    1. Decides which tool to use.
    2. Gets the tool result.
    3. Sends the result to Gemini.
    4. Returns a professional answer.
    """

    # Route question
    tool_response = route_question(question, df)

    tool_name = tool_response["tool"]
    tool_result = tool_response["result"]

    # If no specific tool matched
    if tool_name == "General":

        prompt = f"""
You are an expert Data Analyst.

Answer the user's question professionally.

Question:
{question}
"""

    else:

        prompt = f"""
You are an expert AI Data Analyst.

The following information was produced by the tool:

Tool Used:
{tool_name}

Tool Result:
{tool_result}

User Question:
{question}

Instructions:

- Explain the result in simple English.
- Give useful insights.
- Mention if any action is recommended.
- Format the answer using bullet points.
"""

    response = model.generate_content(prompt)

    return response.text