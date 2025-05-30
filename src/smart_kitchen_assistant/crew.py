from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, task, agent
from dotenv import load_dotenv
from src.smart_kitchen_assistant.tools.custom_tool import search_youtube_links
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()
MODEL = os.getenv("MODEL")
API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL")

llm = LLM(
    model=MODEL,
    api_key=API_KEY,
    temperature=0.7
    )

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=15,  # Store last 15 interactions for rich context
    return_messages=True
)

@CrewBase
class SmartKitchenAssistant:
    """SmartKitchenAssistant Crew with hierarchical cooking and support agents"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def cooking_manager(self) -> Agent:
        return Agent(
			config=self.agents_config['cooking_manager'],
            llm=llm,
			verbose=True,
            max_iter=1,
            sub_agents=[self.youtube_agent(), self.recipe_agent()]
		)

    @agent
    def recipe_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['recipe_agent'],
            llm=llm,
            max_iter=1,
			verbose=True
		)
        
    @agent
    def ingredient_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['ingredient_agent'],
            llm=llm,
            max_iter=1,
			verbose=True
		)
    
    @agent
    def support_manager(self) -> Agent:
        return Agent(
			config=self.agents_config['support_manager'],
            llm=llm,
            max_iter=1,
            sub_agents=[self.ingredient_agent(), self.kitchen_emergency_expert()],
			verbose=True
		)

    @agent
    def kitchen_emergency_expert(self) -> Agent:
        return Agent(
			config=self.agents_config['kitchen_emergency_expert'],
            llm=llm,
            max_iter=1,
			verbose=True
		)
    
    @agent
    def youtube_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['youtube_agent'],
            llm=llm,
            max_iter=1,
            tools=[search_youtube_links],
			verbose=True
		)

    @task
    def recipe_task(self) -> Task:
        return Task(
            config=self.tasks_config['recipe_task'],
        )
        
    @task
    def ingredient_task(self) -> Task:
        return Task(
            config=self.tasks_config['ingredient_task'],
        )
        
    @task
    def kitchen_emergency_task(self) -> Task:
        return Task(
            config=self.tasks_config['kitchen_emergency_task']
        )
        
    @task
    def youtube_task(self) -> Task:
        return Task(
            config=self.tasks_config['youtube_task']
        )
        
    def run(self, user_input):
        cooking_crew = Crew(
                agents=[self.cooking_manager()],
                tasks=[self.recipe_task(), self.youtube_task()],
                process=Process.hierarchical,
                manager_llm=llm,
                verbose=True,
            )
        
        support_crew = Crew(
                agents=[self.support_manager()],
                tasks=[self.ingredient_task(), self.kitchen_emergency_task()],
                process=Process.hierarchical,
                manager_llm=llm,
                verbose=True,
            )
        
        user_responses = []
        
        while True:
            user_responses.append(user_input)
            memory.save_context(
                inputs={"human": user_input},
                outputs={"ai": "Processing response..."}
            )
            
            conversation_history = "\n".join([
                f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
                for m in memory.chat_memory.messages[-10:]
            ])

            # Use safe, primitive-only dictionary
            inputs = {
                'user': user_input,
                'history': conversation_history
            }
            
            if any(keyword in user_input.lower() for keyword in ["cook", "make", "recipe"]):
                response = cooking_crew.kickoff(inputs=inputs).tasks_output[0].raw
                print("Assistant:", response)
                return response
                
            elif any(keyword in user_input.lower() for keyword in ["video", "youtube"]):
                response = cooking_crew.kickoff(inputs=inputs).tasks_output[1].raw
                print("Assistant:", response)
                return response
                
            elif any(keyword in user_input.lower() for keyword in ["ingredient", "nutrition"]):
                response = support_crew.kickoff(inputs=inputs).tasks_output[0].raw
                print("Assistant:", response)
                return response
                
            elif any(keyword in user_input.lower() for keyword in ["burnt", "suggest", "fix"]):
                response = support_crew.kickoff(inputs=inputs).tasks_output[1].raw
                print("Assistant:", response)
                return response
            
            memory.save_context(
                    inputs={"human": user_input},
                    outputs={"ai": response}
                )
            
            if user_input.lower() in ["exit", "quit"]:
                print("Assistant:", "Thanks! We are closing the chat.")
                return 