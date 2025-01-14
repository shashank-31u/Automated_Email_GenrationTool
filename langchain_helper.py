from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# Initialize the OllamaLLM with the desired model
llm = OllamaLLM(temperature=0.7, model="llama3.2",)

from langchain.memory import ConversationBufferMemory



def generate_restaurant_name_and_items(cuisine):
    # Chain 1: Generate restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this restaurant."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")
    
    
    
    memory= ConversationBufferMemory()
    
    chain=LLMChain(llm=llm,prompt=prompt_template_name,memory=memory)
    name= chain.run("Mexican")
    name= chain.run("Indian")
    print(chain.memory.buffer
          )
    
    
    
    # Chain 2: Generate menu items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma-separated string."
    )
    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")
    
    # Sequential Chain: Combine the two chains
    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )
    
    # Run the chain with the input
    response = chain({'cuisine': cuisine})
    
    return response
    