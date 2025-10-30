#this one is able to split any spolliter 
from langchain_community.document_loaders import (
    PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader, WebBaseLoader, WikipediaLoader
)
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter, MarkdownTextSplitter, HTMLHeaderTextSplitter
)
from langchain.schema import Document
from typing import List
import bs4
import os

class SmartDataLoader:
    def __init__(self, context, chunk_size=1000, chunk_overlap=100):
        self.context = context
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_and_split(self):
        """Load the document(s) and split into Document chunks."""
        doc_type = self._get_file_type(self.context)
        raw_docs = self._load_document(doc_type)

        if doc_type == "html":
            return self._split_html_documents(raw_docs)
        else:
            splitter = self._get_splitter(doc_type)
            return splitter.split_documents(raw_docs)

    def _split_html_documents(self, raw_docs):
        """
        HTMLHeaderTextSplitter + RecursiveCharacterTextSplitter pipeline
        that returns Document objects with preserved metadata.
        """
        html_splitter = HTMLHeaderTextSplitter(
            headers_to_split_on=[
                ("h1", "Header 1"),
                ("h2", "Header 2"),
                ("h3", "Header 3")
            ]
        )
        structured_docs = []
        for doc in raw_docs:
            structured_docs.extend(html_splitter.split_text(doc.page_content))

        # Wrap into Document objects with metadata
        structured_docs = [Document(page_content=text, metadata={"source": "html_section"})
                           for text in structured_docs]

        # Now chunk those sections using RecursiveCharacterTextSplitter
        size_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return size_splitter.split_documents(structured_docs)

    def _get_file_type(self, path_or_url):
        """Detect document type from file extension or URL"""
        if path_or_url.startswith("http"):
            return "html"
        ext = os.path.splitext(path_or_url)[1].lower()
        if ext == ".pdf":
            return "pdf"
        elif ext in (".doc", ".docx"):
            return "docx"
        elif ext == ".txt":
            return "txt"
        elif ext == ".md":
            return "md"
        elif ext == "":
            return "wiki"
        else:
            return "txt"

    def _load_document(self, doc_type):
        """Load document(s) by type"""
        dt = doc_type.lower()
        if dt == "pdf":
            return PyPDFLoader(self.context).load()
        elif dt in ("doc", "docx"):
            return UnstructuredWordDocumentLoader(self.context).load()
        elif dt == "txt":
            return TextLoader(self.context).load()
        elif dt == "html":
            return WebBaseLoader(
                web_path=self.context,
                bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                    class_=("post-title", "post-content", "post-header")
                ))
            ).load()
        elif dt == "wiki":
            return WikipediaLoader(query=self.context, load_max_docs=2).load()
        elif dt == "md":
            return TextLoader(self.context).load()
        else:
            raise ValueError(f"Unsupported document type: {doc_type}")

    def _get_splitter(self, doc_type):
        """Return the appropriate text splitter (for non-HTML docs)"""
        dt = doc_type.lower()
        if dt == "md":
            return MarkdownTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        else:
            return RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

# Smart Batch Loader For Context Reading Of Batch of documents 


class SmartBatchLoader:
    def __init__(self, documents: List[str], chunk_size=1000, chunk_overlap=100):
        """
        documents: list of file paths or URLs
        chunk_size: size of each text chunk
        chunk_overlap: overlap between chunks
        """
        self.documents = documents
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_and_split_all(self) -> List[str]:
        """Load and split all documents into chunks using SmartDataLoader"""
        all_chunks = []
        for doc in self.documents:
            loader = SmartDataLoader(doc, self.chunk_size, self.chunk_overlap)
            chunks = loader.load_and_split()
            all_chunks.extend(chunks)
        return all_chunks