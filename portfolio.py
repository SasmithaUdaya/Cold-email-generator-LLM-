import pandas as pd
import chromadb
import chromadb.config
import uuid

class Portfolio:
    def __init__(self, file_path="app/resources/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Configure Chroma client with persistent directory
        settings = chromadb.config.Settings(
            persist_directory="vectorstore",  # folder to save vector DB
            anonymized_telemetry=False
        )

        self.chroma_client = chromadb.Client(settings=settings)

        # Get or create a collection named "portfolio"
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],  # needs to be a list
                    metadatas=[{"links": row["Links"]}],  # needs to be a list of dicts
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        # skills should be a list of strings
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
