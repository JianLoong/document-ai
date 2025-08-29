from google.adk.agents import LlmAgent


import os
import datetime

from .tools.general_tools import confluence_tool


today = datetime.date.today().strftime("%B %d, %Y")

with open(
    os.path.join(os.path.dirname(__file__), "instructions", "ANALYSER_INSTRUCTION.md"),
    encoding="utf-8",
) as f:
    instruction = f.read().format(today=today)


root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="schemes_mandate_agent",
    instruction=instruction,
    tools=[confluence_tool],
)
