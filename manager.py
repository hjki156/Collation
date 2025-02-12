from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import VARCHAR
from sqlalchemy import TEXT
from typing import Optional

def Exam_Factory(Base):
    class Exam(Base):
        __tablename__ = 'Question'
        id: Mapped[int] = mapped_column(primary_key=True)
        content: Mapped[str] = mapped_column(TEXT)
        author: Mapped[str] = mapped_column(VARCHAR(50))
        tags: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
        other: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
        def to_dict(self):
            return {
                    'id': self.id,
                    'content': self.content,
                    'author': self.author,
                    'tags': self.tags,
                    'other': self.other,
                }
        def __repr__():
            return f'<Exam {self.id}>'
    return Exam
