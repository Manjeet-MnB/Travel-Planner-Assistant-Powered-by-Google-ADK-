from google.adk.agents import Agent


from travel_planner.supporting_agents import travel_inspiration_agent

#import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

LLM = "gemma-4-31b-it" # gemini-2.5-flash #gemma-4-31b-it

root_agent = Agent(
    model=LLM,
    name="travel_planner_main",
    description="A helpful travel planning assistant that helps users plan their trips by providing information and suggestions based on their preferences.",
    instruction="""
            - You are an exclusive travel concierge agent
            - You help users to discover their dream holiday destination and plan their vacation.
            - Use the inspiration_agent to get the best destination, news, places nearby e.g hotels, cafes, etc near attractions and points of interest for the user.
            - You cannot use any tool directly. 
            """,
    sub_agents=[travel_inspiration_agent]
)