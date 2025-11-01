from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Связующая таблица для Many-to-Many организация <-> деятельность
organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
)


class Building(Base):
    """
    Модель здания
    """
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)

    # Связь: одно здание может содержать несколько организаций
    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    """
    Модель деятельности с иерархией
    """
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=True)

    # Рекурсивная связь для дерева деятельности
    children = relationship("Activity", backref="parent", remote_side=[id])

    # Связь организации-многие-ко-многим
    organizations = relationship(
        "Organization",
        secondary=organization_activities,
        back_populates="activities"
    )


class Organization(Base):
    """Модель организации"""
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # У Organization ЕСТЬ поле building_id (внешний ключ)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="SET NULL"), nullable=True)
    building = relationship("Building", back_populates="organizations")

    phones = relationship("Phone", back_populates="organization", cascade="all, delete-orphan")
    activities = relationship(
        "Activity",
        secondary=organization_activities,
        back_populates="organizations"
    )


class Phone(Base):
    """
    Телефоны организации
    """
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    organization = relationship("Organization", back_populates="phones")
