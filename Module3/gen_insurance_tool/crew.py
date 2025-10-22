import decimal
from doctest import OutputChecker
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pydantic import BaseModel,Field
from typing import List
from crewai_tools import SerperDevTool
import yaml
import os
from .tools.visual_tool1 import PolicyVisualizerInput, PolicyVisualizerTool
#from crewai import FunctionCallingAgent

class TraditionalPolicy(BaseModel):
    """ Traditional Policies that is in the news and attracting attention """
    policy_name:str=Field("Name of the Traditional policy")
    premium_amount:int=Field("Policy premium amount to be paid")
    policy_term:int=Field("No of years the policy will be effective")
    premium_paying_term:int=Field(" No of years premium need to be paid")
    benifits_and_coverage:str=Field(" Policy benifts and coverage")
    Maturity_amount:int=Field("The amount to be paid to customer on Maturity")
    percentage_rate_of_incresase:float=Field("The rate with which the policy maturity amount is calculated")

class TradtionalPolicyList(BaseModel):
     """ List of multiple Traditional Policies that are in the news """
     companies: List[TraditionalPolicy] = Field(description="List of Traditional Policies trending in the news")

class MarketLinkedPolicy(BaseModel):
    """ MarketLinkedPolicy Policies that is in the news and attracting attention """
    policy_name:str=Field("Name of the Market Linked policy")
    premium_amount:int=Field("Policy premium amount to be paid")
    policy_term:int=Field("No of years the policy will be effective")
    premium_paying_term:int=Field(" No of years premium need to be paid")
    benifits_and_coverage:str=Field(" Policy benifts and coverage")
    Maturity_amount:int=Field("The amount to be paid to customer on Maturity")
    percentage_rate_of_incresase:float=Field("The rate with which the policy maturity amount is calculated")

class MarketLinkedPolicyPolicyList(BaseModel):
     """ List of multiple Market Linked  that are in the news """
     companies: List[MarketLinkedPolicy] = Field(description="List of Market Linked  trending in the news")



@CrewBase
class GenInsuranceTool():
    agents_config_path = 'src/gen_insurance_tool/config/agents.yaml'
    tasks_config_path = 'src/gen_insurance_tool/config/tasks.yaml'

    def __init__(self):
        # Load YAML files once, convert to dicts
        with open(self.agents_config_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)

        with open(self.tasks_config_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

        self.agents=[]
        self.tasks=[]
        print("Agents config loaded keys:", self.agents_config.keys())
        print("Tasks config loaded keys:", self.tasks_config.keys())
        print("traditionalPolicyResearcher config type:", type(self.agents_config.get('traditionalPolicyResearcher')))
        print("find_traditional_policies config type:", type(self.tasks_config.get('find_traditional_policies')))




    

    @agent
    def traditionalPolicyResearcher(self) -> Agent:
        return Agent(
            config=self.agents_config['traditionalPolicyResearcher'], 
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def marketlinkedPolicyResearcher(self) -> Agent:
        return Agent(
            config=self.agents_config['marketlinkedPolicyResearcher'], 
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def policyPicker(self) -> Agent:
        return Agent(
            config=self.agents_config['policyPicker'], 
            verbose=True
        )


    @task
    def find_traditional_policies(self) -> Task:
        return Task(
            config=self.tasks_config['find_traditional_policies'], 
            max_iterations=2,
            output_pydantic=TradtionalPolicyList
        )

    @task
    def find_marketlinked_policies(self) -> Task:
        return Task(
            config=self.tasks_config['find_marketlinked_policies'], # type: ignore[index]
            max_iterations=2,
            output_pydantic=MarketLinkedPolicyPolicyList
        )

    @task
    def pick_best_policy(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_policy'], # type: ignore[index]
            
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Personalinsurance crew"""

        manager=Agent(
            config=self.agents_config['Policymanager'],
            allow_delegation=True
        )

        ##---This below code is dfifrent from  personalinsurance crew ----------------------------#
        traditional_task = self.find_traditional_policies()
        marketlinked_task = self.find_marketlinked_policies()
        pick_best_task = self.pick_best_policy()

        
        visualizer_agent = Agent(
                                role='Senior Insurance Analyst',
                                goal='Compare and visualize the best policies for investment',
                                backstory='You are responsible for generating user-friendly visual summaries of policies.',
                                tools=[PolicyVisualizerTool()], #dont pass class name but instance indicated by ()
                                llm='gpt-4o-mini',
                                allow_delegation=False,
                                args_schema=PolicyVisualizerInput
                            )
        

        '''
        visualizer_agent = FunctionCallingAgent(
                            role='Senior Insurance Analyst',
                            goal='Compare and visualize the best policies for investment',
                            backstory='You are responsible for generating user-friendly visual summaries of policies.',
                            tools=[PolicyVisualizerTool()],
                            allow_delegation=False
                        )
        '''
        visualize_task = Task(
            config={},
            description="Generate a visual comparison chart of the policies considered.",
            expected_output="A PNG chart saved to disk comparing premium, term, and returns for each policy.",
            agent=visualizer_agent,
            context=[traditional_task,marketlinked_task,pick_best_task] #context expect task instances(object) not their name as strings
              
            
        )


        # Add to agents and tasks lists
        self.agents.append(visualizer_agent)
        self.tasks.append(visualize_task)
        
        #-------------------------------------------------------------------------------------------------

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical, #not sequential here but hirarchal  equivalent of handoff
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
            manager_agent=manager
        )
