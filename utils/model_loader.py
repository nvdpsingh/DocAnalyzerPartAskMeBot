import os
import sys
from dotenv import load_dotenv 
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from langchain_community.embeddings import HuggingFaceEmbeddings
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class ModelLoader:

    """
    This class is used to load the model and the configuration for the project.
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        log.info("Configurations loaded successfully", config_keys=list(self.config.keys()))
    
    def _validate_env(self):
        """
        This method is used to validate the environment variables.
        """
        required_vars = ["GROQ_API_KEY"]
        self.api_keys = {key: os.getenv(key) for key in required_vars}  # Fixed: was using 'vars' instead of 'key'
        missing = {k for k, v in self.api_keys.items() if not v}
        if missing:
            log.error("Missing required environment variables", missing_vars=list(missing))
            raise DocumentPortalException(f"Missing required environment variables: {missing}", sys)
        
        # Log which keys are available
        available = [k for k, v in self.api_keys.items() if v]
        log.info("Environment variables validated successfully", available_keys=available)

    def load_embeddings(self):
        """
        This method is used to load the embeddings model.
        """
        try:
            log.info("Loading embeddings model....")
            return HuggingFaceEmbeddings(model_name=self.config["embedding_model"]["model_name"])
        except Exception as e:
            log.error("Error loading embeddings model", error=str(e))
            raise DocumentPortalException(f"Error loading embeddings model: {e}", sys)

    def load_llm(self):
        """this method is used to load the llm model.
        """
        llm_block = self.config["llm"]

        log.info("Loading llm model....")

        provider_key = os.getenv("LLM_PROVIDER","groq")

        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider=provider_key, available_providers=list(llm_block.keys()))
            raise ValueError(f"LLM provider '{provider_key}' not found in config")

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)

        log.info("Loading LLM", provider=provider, model=model_name)


        if provider == "groq":
            return ChatGroq(
                model=model_name,
                api_key=self.api_keys.get("GROQ_API_KEY"),  # Fixed: was api_key_mgr
                temperature=temperature,
            )

        # elif provider == "openai":
        #     return ChatOpenAI(
        #         model=model_name,
        #         api_key=self.api_key_mgr.get("OPENAI_API_KEY"),
        #         temperature=temperature,
        #         max_tokens=max_tokens
        #     )

        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")

        
    

if __name__ == "__main__":
    loader = ModelLoader()

    # Test Embedding
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result: {result}")

    # Test LLM
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")