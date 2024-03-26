from langchain.text_splitter import RecursiveCharacterTextSplitter
from CLLeMensLangchain.schema.loaders import Loaders
from typing import Union, List
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
import os
import shutil
from pydub import AudioSegment
from openai import OpenAI


from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Set OpenAI API key from environment variable


class AudioLoader(Loaders):
    def __init__(self, file_path: str):
        """
        Initialize AudioLoader

        :param file_path: The path to the file to be loaded
        """
        self.file_path = file_path
        if "~" in self.file_path:
            self.file_path = os.path.expanduser(self.file_path)

    def transcribe_audio(self, audio_file_path, chunk_length_in_seconds=120):
        # Load audio file
        audio = AudioSegment.from_mp3(audio_file_path)

        # Convert chunk length to milliseconds (PyDub uses milliseconds)
        chunk_length = chunk_length_in_seconds * 1000

        # Calculate number of chunks needed
        num_chunks = len(audio) // chunk_length + 1  # +1 to account for any remaining part

        # Create cache directory if it doesn't exist
        cache_dir = "cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Initialize an empty string to store the full transcription
        full_transcription = ""

        # Loop over the audio file, chunk by chunk
        for i in range(num_chunks):
            # Extract the chunk
            start_time = i * chunk_length
            end_time = (i + 1) * chunk_length
            chunk = audio[start_time:end_time]

            # Export the chunk to a temporary file
            temp_file_name = os.path.join(cache_dir, f"temp_chunk_{i}.mp3")
            chunk.export(temp_file_name, format="mp3")

            # Transcribe the chunk using OpenAI Whisper
            with open(temp_file_name, "rb") as audio_file:
                transcript = client.audio.transcribe(model="whisper-1", file=audio_file)
                full_transcription += transcript.text + " "

            # Delete the temporary chunk file
            os.remove(temp_file_name)

        # Delete the cache directory
        shutil.rmtree(cache_dir)

        return full_transcription

    def load(self) -> Union[str, List[str], List[Document]]:
        """
        Load content from an audio file and return its transcription
        :return: The transcribed content of the audio
        """
        try:
            transcription = self.transcribe_audio(self.file_path)

            # Split the filepath into path and extension
            path, _ = os.path.splitext(self.file_path)

            cache_path = path.replace("uploads", "audio_cache")
            cache_base_path = os.path.dirname(cache_path)

            # Create the cache directory if it doesn't exist
            if not os.path.exists(cache_base_path):
                os.makedirs(cache_base_path)

            # Append the new extension .txt
            cache_file_path = cache_path + ".txt"


            # Write the string to the file
            with open(cache_file_path, 'w') as file:
                file.write(transcription)

            try:
                content = TextLoader(cache_file_path)
                pages = content.load()

            except Exception as e:
                return f"Error loading audio: {str(e)}"

            # Remove the cache file
            os.remove(cache_file_path)
            return pages

        except Exception as e:
            return f"Error loading audio: {str(e)}"

    def chunkDocument(self, document: List[Document], chunkSize=750) -> List[Document]:
        """Chunk a document into smaller parts for processing via embeddings
        :param document: The document to be chunked (generated by load())
        :param chunkSize: The size of the chunks (default 750), greatly affects the result of the embeddings & prompts
        :return: The chunked document as a list of Langchain Documents with metadata [page, source, start_index]
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunkSize,
            chunk_overlap=20,
            add_start_index=True,
        )
        chunked_content = text_splitter.split_documents(document)
        return chunked_content
