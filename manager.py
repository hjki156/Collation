from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import VARCHAR
from sqlalchemy import TEXT
from typing import Optional

class Base(DeclarativeBase):
    pass

class Exam(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[TEXT]
    author: Mapped[VARCHAR(50)]
    tags: Mapped[Optional[VARCHAR(100)]]
    other: Mapped[VARCHAR(100)]
    def __repr__():
        return f'<Exam {id}>'

