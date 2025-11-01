from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey


class Base(DeclarativeBase):
    pass


class List(Base):
    __tablename__ = "lists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    items: Mapped[list["Item"]] = relationship("Item", back_populates="list", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(280), index=True)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id", ondelete="CASCADE"))
    list: Mapped["List"] = relationship("List", back_populates="items")