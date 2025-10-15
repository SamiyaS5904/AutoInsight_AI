from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
import uuid

class MongoDBHelper:
    
    def __init__(self):
        """
        Initialize MongoDB connection (Atlas in your case).
        Make sure you keep credentials safe (ideally via env variables).
        """
        self.client = MongoClient(
            "mongodb+srv://connectsamiya5904:samiya2025@cluster0.45dsjs4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            server_api=ServerApi('1')
        )
        print('[MongoDBHelper] ✅ Connection Created')

    def select_db(self, db_name='Vehicle_Agent', collection='chat_history'):
        """
        Select database and collection where chats will be stored.
        Default: Vehicle_Agent > chat_history
        """
        self.db = self.client[db_name]
        self.collection = self.db[collection]
        print(f'[MongoDBHelper] ✅ DB "{db_name}" Collection "{collection}" Selected')

    def insert_chat(self, session_id, role, content):
        """
        Insert a chat message into the collection.
        Each document will have: session_id, role, content, timestamp
        """
        document = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.utcnow()
        }
        result = self.collection.insert_one(document)
        print(f'[MongoDBHelper] 💬 Message inserted ({role}) in collection "{self.collection.name}"')
        return result

    def fetch_chat_history(self, session_id, limit=20):
        """
        Fetch chat history for a given session_id.
        Sorted by timestamp ascending (oldest → newest).
        """
        documents = list(
            self.collection.find({"session_id": session_id})
                           .sort("timestamp", 1)
                           .limit(limit)
        )
        print(f'[MongoDBHelper] 📂 {len(documents)} Messages fetched for session_id="{session_id}"')
        return documents

    def get_new_session_id(self):
        """
        Generate a new unique session ID for tracking user conversations.
        """
        return str(uuid.uuid4())

def fetch_vehicle_info(self, vehicle_name: str):
    """
    Fetch vehicle details from MongoDB by name.
    """
    query = {"name": {"$regex": vehicle_name, "$options": "i"}}  # case-insensitive search
    document = self.collection.find_one(query)
    if document:
        return document
    else:
        return None
