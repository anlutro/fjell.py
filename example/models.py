from fjell.plugins.sqla import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def as_dict(self):
        return {"id": self.id, "name": self.name}
