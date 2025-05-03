from datetime import datetime
from db import Base, engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func, ForeignKey






class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    creation_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    processing_results: Mapped[list["ProcessingResult"]] = relationship(
        "ProcessingResult",  # Указание целевого класса строкой
        back_populates="user",
        cascade="all, delete-orphan"
    )

class ProcessingResult(Base):
    __tablename__ = 'processing_results'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    photo_url: Mapped[str] = mapped_column(nullable=False)  # URL оригинальной фотографии
    processed_data: Mapped[str] = mapped_column(nullable=True)  # JSON с результатами обработки
    processing_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    status: Mapped[str] = mapped_column(default='pending')  # pending/completed/failed  Статус обработки со значением по умолчанию 'pending'
    
    # Связь с пользователем
    user: Mapped["User"] = relationship("User", back_populates="processing_results")

    def __repr__(self):
        return f'<ProcessingResult {self.id} for user {self.user_id}>'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)