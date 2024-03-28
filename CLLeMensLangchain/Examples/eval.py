from langchain.document_loaders import DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context, conditional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import find_dotenv, load_dotenv
#from langchain_community.embeddings import OllamaEmbeddings
#from langchain_mistralai.chat_models import ChatMistralAI
#embedding = OllamaEmbeddings(model="mistral")
#model = ChatMistralAI(llm=Ollama(model="mistral"))
load_dotenv(find_dotenv())
loader = DirectoryLoader("C:\\Users\\Jimmy\\PycharmProjects\\CLLeMens\\media\\uploads")
documents = loader.load()
print(documents)

# generator with openai models
generator_llm = ChatOpenAI(model="gpt-3.5-turbo")
critic_llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
    #with_debugging_logs=True
)
generator.adapt(language="german",evolutions=[simple, multi_context, conditional, reasoning])


# generate testset
testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25},with_debugging_logs=True)
testset.to_pandas()
print(testset.to_pandas())
