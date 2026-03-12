# mcp/schema_reader.py

from pymongo import MongoClient


class SchemaReader:

    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def get_collections(self) -> list:
        return self.db.list_collection_names()

    def get_sample(self, collection: str, limit: int = 1) -> list:
        return list(
            self.db[collection].find({}, {"_id": 0}).limit(limit)
        )

    def get_indexes(self, collection: str) -> list:
        info = self.db[collection].index_information()
        return [
            ", ".join(f"{k}:{v}" for k, v in idx["key"])
            for idx in info.values()
        ]

    def describe_all(self) -> str:
        result = "AVAILABLE COLLECTIONS:\n\n"
        for name in self.get_collections():
            sample = self.get_sample(name)
            fields = list(sample[0].keys()) if sample else []
            indexes = self.get_indexes(name)
            result += (
                "COLLECTION: " + name + "\n"
                "FIELDS: " + ", ".join(fields) + "\n"
                "INDEXES: " + ", ".join(indexes) + "\n\n"
            )
        return result