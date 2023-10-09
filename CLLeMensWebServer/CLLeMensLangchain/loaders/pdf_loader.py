import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from CLLeMensWebServer.CLLeMensLangchain.schema.loaders import Loaders
from typing import Union, List
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document


class PdfLoader(Loaders):
    def __init__(self, file_path: str, extract_images: bool = True):
        """
        Initialize PdfLoader.

        :param extract_images: If True(default), extract image text with OCR, otherwise, don't.
        :param file_path: The path to the file to be loaded.
        """
        self.file_path = file_path
        self.extract_images = extract_images
        if "~" in self.file_path:
            self.file_path = os.path.expanduser(self.file_path)

    def load(self) -> Union[str, List[str], List[Document]]:
        """Load content from a PDF and return it.
            :return: The content of the PDF as a pagewise list of Langchain Documents.
        """
        try:
            content = PyPDFLoader(self.file_path, extract_images=self.extract_images)
            pages = content.load()

        except Exception as e:
            return f"Error loading PDF: {str(e)}"

        return pages

    def chunkDocument(self, document: List[Document], chunkSize=750) -> List[Document]:
        """Chunk a document into smaller parts for processing via embeddings"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunkSize,
            chunk_overlap=20,
            add_start_index=True,
        )
        chunked_content = text_splitter.split_documents(document)
        return chunked_content
