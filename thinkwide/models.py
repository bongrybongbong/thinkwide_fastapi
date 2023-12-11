import sqlalchemy
from database import metadata

savemindmapnode = sqlalchemy.Table(
    "savemindmapnode",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("Node_Text", sqlalchemy.String),
    sqlalchemy.Column("Node_type", sqlalchemy.Integer),
    sqlalchemy.Column("aiData", sqlalchemy.String),
    sqlalchemy.Column("isSelected", sqlalchemy.Boolean),
    sqlalchemy.Column("Children", sqlalchemy.String),
)