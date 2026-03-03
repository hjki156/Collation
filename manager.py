from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, TEXT, DateTime
from typing import Any, Optional
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class eBase:
    def to_dict(self) -> dict[str, Optional[str] | int]:
        raise NotImplementedError

def Exam_Factory(Base: type[Any]):
    class Exam(Base, eBase):
        __tablename__ = 'Question'
        id: Mapped[int] = mapped_column(primary_key=True)
        content: Mapped[str] = mapped_column(TEXT)
        author: Mapped[str] = mapped_column(VARCHAR(50))
        tags: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
        other: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
        def to_dict(self) -> dict[str, Optional[str]|int]:
            return {
                    'id': self.id,
                    'content': self.content,
                    'author': self.author,
                    'tags': self.tags,
                    'other': self.other,
                }
        def __repr__(self):
             return f'<Exam {self.id}>'
    return Exam

def User_Factory(Base: type[Any]):
    class User(Base, eBase):
        __tablename__ = 'users'
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(VARCHAR(80), unique=True)
        password_hash: Mapped[str] = mapped_column(VARCHAR(256))
        created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
        
        def set_password(self, password: str):
            self.password_hash = generate_password_hash(password)
            
        def check_password(self, password: str) -> bool:
            return check_password_hash(self.password_hash, password)
            
        def to_dict(self) -> dict[str, Optional[str]|int]:
            return {
                'id': self.id,
                'username': self.username,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
            
        def __repr__(self):
            return f'<User {self.id}>'
            
    return User