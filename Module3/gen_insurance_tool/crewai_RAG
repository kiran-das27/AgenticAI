#1. Install Required Packages
#pip install crewai crewai-tools langchain chromadb

#2. Prepare the PDF and Vector Store
from crewai_tools import RagTool

# Initialize the RAG tool

rag_tool = RagTool(
    persist_directory="./vector_db",  # Optional: to persist the DB
    embedding_model="openai"          # or "huggingface"
)


# Add your PDF to the vector store
rag_tool.add(data_type="file", path="path/to/your/document.pdf")


#3. Create a CrewAI Agent with the RAG Tool

from crewai import Agent

knowledge_agent = Agent(
    role="PDF Knowledge Expert",
    goal="Answer questions based on the uploaded PDF",
    backstory="An expert trained to extract insights from documents.",
    tools=[rag_tool],
    verbose=True
)

#4. Define a Task

from crewai import Task

task = Task(
    description="Summarize the key points from the uploaded PDF.",
    expected_output="A concise summary of the document.",
    agent=knowledge_agent
)

#5. Run the Crew

from crewai import Crew

crew = Crew(
    agents=[knowledge_agent],
    tasks=[task]
)

result = crew.kickoff()
print(result)
