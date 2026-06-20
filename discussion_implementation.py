# Object-Oriented Programming Four Core Pillars

#Inheritance allows a new class to adopt the attributes and methods of an existing class
# From main.py
from pydantic import BaseModel

class AgentRequest(BaseModel):
    """Request model for agent invocation."""
    prompt: str

class AgentResponse(BaseModel):
    """Response model for agent invocation."""
    response: str

#Abstraction hides the complex background details, meaning it only shows the essential interface to the user
@app.post("/agent", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    """
    Invoke the AI agent with a prompt.

    The agent can read and write text files based on natural language instructions.
    """
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # Run the agent with the user's prompt
        result = run_agent(request.prompt) #Where abstraction takes place

        return AgentResponse(response=result)

#Encapsulation involves wrapping data and methods that operate on that data into a single unit, restricting direct access to some object's component
# Refactoring agent.py into an Encapsulated Class
class NoteTakingAgent:
    def __init__(self, model_name: str = "gpt-4"):
        # Private/Protected attributes encapsulated inside the class
        self.__llm = ChatOpenAI(model=model_name, temperature=0)
        self.__tools = [read_note, write_note]
        self.__system_message = "You are a helpful note-taking assistant."
        self.__agent = create_react_agent(self.__llm, self.__tools, prompt=self.__system_message)

    def execute_query(self, user_input: str) -> str:
        """Public interface to interact with the hidden agent logic."""
        result = self.__agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"recursion_limit": 50}
        )
        return result["messages"][-1].content

#Polymorphism allows different objects to be treated as instances of a common superclass
# Custom Polymorphic Tool Interface
class BaseCustomTool:
    def execute(self, *args, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement this method")

class ReadNoteTool(BaseCustomTool):
    def execute(self, filepath: str) -> str:
        return read_note(filepath) # Uses existing read_note logic

class WriteNoteTool(BaseCustomTool):
    def execute(self, filepath: str, content: str) -> str:
        return write_note(filepath, content) # Uses existing write_note logic

# Polymorphic Execution Example
my_tools = [ReadNoteTool(), WriteNoteTool()]
for tool in my_tools:
    # Polymorphism: Same method call ('execute'), completely different behaviors!
    print(tool.execute("notes.txt", "Hello World"))

