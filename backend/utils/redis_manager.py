import json
import os
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisManager:
    def __init__(self):
        try:
            import redis
            self.client = redis.from_url(REDIS_URL, decode_responses=True)
            # Test connection
            self.client.ping()
            self.use_redis = True
            print("✓ Connected to Redis")
        except Exception as e:
            print(f"⚠️  Redis not available, using in-memory storage: {e}")
            self.client = {}
            self.use_redis = False
    
    def set_session(self, session_id: str, data: Dict[str, Any], ttl: int = 86400):
        """Store session data with TTL"""
        try:
            if self.use_redis:
                self.client.setex(
                    f"session:{session_id}",
                    ttl,
                    json.dumps(data, default=str)
                )
            else:
                # In-memory storage
                self.client[f"session:{session_id}"] = json.dumps(data, default=str)
            return True
        except Exception as e:
            print(f"Session set error: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        try:
            if self.use_redis:
                data = self.client.get(f"session:{session_id}")
            else:
                data = self.client.get(f"session:{session_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Session get error: {e}")
            return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update specific fields in session"""
        try:
            session_data = self.get_session(session_id)
            if session_data:
                session_data.update(updates)
                session_data['last_updated'] = datetime.now().isoformat()
                self.set_session(session_id, session_data)
                return True
            return False
        except Exception as e:
            print(f"Redis update error: {e}")
            return False
    
    def delete_session(self, session_id: str):
        """Delete session data"""
        try:
            self.client.delete(f"session:{session_id}")
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def cache_product(self, product_id: str, data: Dict[str, Any], ttl: int = 3600):
        """Cache product data"""
        try:
            self.client.setex(
                f"product:{product_id}",
                ttl,
                json.dumps(data, default=str)
            )
            return True
        except Exception as e:
            print(f"Redis cache error: {e}")
            return False
    
    def get_cached_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get cached product data"""
        try:
            data = self.client.get(f"product:{product_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Redis get cache error: {e}")
            return None
    
    def add_to_conversation(self, session_id: str, message: Dict[str, Any]):
        """Add message to conversation history"""
        try:
            session_data = self.get_session(session_id)
            if session_data:
                if 'conversation_history' not in session_data:
                    session_data['conversation_history'] = []
                session_data['conversation_history'].append(message)
                self.set_session(session_id, session_data)
                return True
            return False
        except Exception as e:
            print(f"Redis conversation error: {e}")
            return False
    
    def get_conversation_history(self, session_id: str) -> list:
        """Get conversation history"""
        try:
            session_data = self.get_session(session_id)
            if session_data and 'conversation_history' in session_data:
                return session_data['conversation_history']
            return []
        except Exception as e:
            print(f"Redis get conversation error: {e}")
            return []


# Singleton instance
redis_manager = RedisManager()
