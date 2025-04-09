from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils import rate_limit, retry_with_exponential_backoff
from loguru import logger

class GroqClient:
    def __init__(self):
        self.llm = None

    def initialize(self, api_key):
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=3000,
            temperature=0.7
        )

    @retry_with_exponential_backoff(max_retries=3)
    @rate_limit(calls=50, period=60)  # 50 calls per minute
    def generate_completion(self, prompt, template=None, **kwargs):
        if not self.llm:
            raise ValueError("Client not initialized.")

        try:
            if template:
                prompt_template = PromptTemplate.from_template(template)
                chain = LLMChain(llm=self.llm, prompt=prompt_template)
                response = chain.run(**kwargs)
            else:
                messages = [HumanMessage(content=prompt)]
                response = self.llm.invoke(messages).content
            logger.debug(f"Successfully generated completion for prompt: {prompt[:100]}...")
            return response
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise

    @retry_with_exponential_backoff(max_retries=3)
    @rate_limit(calls=50, period=60)
    def create_chain(self, prompt_template):
        if not self.llm:
            raise ValueError("Client not initialized.")
        return LLMChain(llm=self.llm, prompt=PromptTemplate.from_template(prompt_template))