"""LLM client using LangChain."""
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Optional
import logging

from src.config import Config

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified LLM client using LangChain abstractions."""
    
    def __init__(self, config: Config):
        """
        Initialize LLM client.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.llm = self._initialize_llm()
        self.json_parser = JsonOutputParser()
        self.str_parser = StrOutputParser()
    
    def _initialize_llm(self) -> BaseChatModel:
        """Initialize LLM based on provider configuration."""
        provider = self.config.llm_provider.lower()
        
        logger.info(f"Initializing LLM provider: {provider}")
        
        if provider == "openai":
            if not self.config.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
            
            return ChatOpenAI(
                model=self.config.openai_model,
                openai_api_key=self.config.openai_api_key,
                temperature=self.config.llm_temperature,
                max_tokens=self.config.llm_max_tokens,
                max_retries=3,
                timeout=self.config.llm_timeout,
            )
        
        elif provider == "gemini":
            if not self.config.google_api_key:
                raise ValueError("GOOGLE_API_KEY is required when LLM_PROVIDER=gemini")
            
            return ChatGoogleGenerativeAI(
                model=self.config.gemini_model,
                google_api_key=self.config.google_api_key,
                temperature=self.config.llm_temperature,
                max_output_tokens=self.config.llm_max_tokens,
                max_retries=3,
            )
        
        elif provider == "anthropic":
            if not self.config.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
            
            return ChatAnthropic(
                model=self.config.anthropic_model,
                anthropic_api_key=self.config.anthropic_api_key,
                temperature=self.config.llm_temperature,
                max_tokens=self.config.llm_max_tokens,
                max_retries=3,
            )
        
        elif provider == "ollama":
            return Ollama(
                base_url=self.config.ollama_base_url,
                model=self.config.ollama_model,
                temperature=self.config.llm_temperature,
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def invoke(self, prompt: str, parse_json: bool = True) -> Dict | str:
        """
        Invoke LLM with prompt.
        
        Args:
            prompt: The prompt text
            parse_json: Whether to parse response as JSON
            
        Returns:
            Parsed JSON dict or raw string response
        """
        try:
            # Create simple prompt template
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant."),
                ("human", "{input}")
            ])
            
            # Create chain
            if parse_json:
                chain = prompt_template | self.llm | self.json_parser
            else:
                chain = prompt_template | self.llm | self.str_parser
            
            # Invoke chain
            result = chain.invoke({"input": prompt})
            
            logger.debug(f"LLM response received: {type(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Error invoking LLM: {str(e)}")
            raise
    
    def invoke_with_template(self, template: ChatPromptTemplate, variables: Dict, parse_json: bool = True) -> Dict | str:
        """
        Invoke LLM with prompt template.
        
        Args:
            template: ChatPromptTemplate instance
            variables: Variables to format the template
            parse_json: Whether to parse response as JSON
            
        Returns:
            Parsed JSON dict or raw string response
        """
        try:
            # Create chain
            if parse_json:
                chain = template | self.llm | self.json_parser
            else:
                chain = template | self.llm | self.str_parser
            
            # Invoke chain
            result = chain.invoke(variables)
            
            logger.debug(f"LLM response received: {type(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Error invoking LLM with template: {str(e)}")
            raise

