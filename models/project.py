#!/usr/bin/python3
"""create the Project model"""

from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import (String, Column, Float,
                        TEXT, ForeignKey, Table)
from sqlalchemy.orm import relationship
from models.tools import Tool

if storage_type == "db":
    project_tools = Table("project_tools", Base.metadata,
                          Column("project_id", ForeignKey("projects.id", 
                                                          onupdate="CASCADE",
                                                          ondelete="CASCADE"),
                                  primary_key=True),
                          Column("tool_id", ForeignKey("tools.id",
                                                       onupdate="CASCADE",
                                                       ondelete="CASCADE"),
                                 primary_key=True),
                          Column("tool_version", String(60)
                                ))


class Project(BaseModel, Base):
    """create the Project model"""
    if storage_type == "db": # meaning the storage engine is db
        __tablename__ = "projects"
        name = Column("name", String(60), nullable=False, unique=True)
        description = Column("description", String(255), nullable=True)
        video_url = Column("video_url", String(255), nullable=True)
        #   video_url --> if the image is on device use the following naming convention:
        #    "project_id-0.vid_extension",
        images = Column("images", TEXT, nullable=True)
        # JSON NULL, ---> for passing a list of images urls
        # --> if the image is on device use the following naming convention:
            # "project_id-img_no.img_extension"
        category_id = Column(String(60), ForeignKey("categories.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        rate = Column("rate", Float, default=0) # must be between 0 and 5
        tools = relationship("Tool", secondary="project_tools", viewonly=False)

        def to_dict(self):
            """
            get the tools names and category name of projects
            besides other attributes
            """
            from models import storage
            tool_ids = [tool.id for tool in self.tools]
            dict_repr = super().to_dict()
            tool_names = [storage.find("Tool", tool_id).name for tool_id in tool_ids]
            dict_repr["tools"] = tool_names
            category_id = self.category_id
            dict_repr["category"] = storage.find("Category", category_id).name
            return dict_repr

    else:
        name = ""
        description = ""
        video_url = ""
        images = []
        category_id = ""
        user_id = ""
        rate = 0.0 # must be between 0 and 5
        tools = []
        
        @property
        def owner(self):
            return getattr(self, "owner", None)
                    

    def __init__(self, **kwargs):
        """
        instansiate a Project instance
        and set all attribute passed of the form of kwargs
        """
        super().__init__()
        for key, val in kwargs.items():
            setattr(self, key, val)
