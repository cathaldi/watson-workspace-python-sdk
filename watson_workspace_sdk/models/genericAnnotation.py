import logging
from watson_workspace_sdk.config import Config

logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


class Annotation:

    def __init__(self, *, title: str, text: str, actor: str, type: str = "generic", version="1", color="#36a64f",
                 annotation_id=None, created=None, created_by=None):
        self.type: str = type
        self.version: str = version
        self.color: str = color
        self.title: str = title
        self.text: str = text
        self.actor: str = actor

        self.annotationId = annotation_id
        self.created = created
        self.createdBy = created_by

    @classmethod
    def from_json(cls, annotation_body) -> 'Annotation':
        type= annotation_body.get("type")  # enum
        version: str = annotation_body.get("version")   # Fixed to start as 1
        color: str = annotation_body.get("color")  # "#36a64f"
        title: str = annotation_body.get("title")
        text: str = annotation_body.get("text")
        actor: str = annotation_body.get("actor", {}).get("name", None)

        annotation_id: str = annotation_body.get("annotationId")
        created: str = annotation_body.get("created")
        created_by: str = annotation_body.get("createdBy")
        annotation = cls(type=type, version=version, color=color, title=title, text=text, actor=actor,
                         annotation_id=annotation_id, created=created, created_by=created_by)
        return annotation

    @classmethod
    def from_dict(cls, annotation_body: {}) -> 'Annotation':
        type_: str = annotation_body.get("type")
        version: str = annotation_body.get("version")
        color: str = annotation_body.get("color")
        title: str = annotation_body.get("title")
        text: str = annotation_body.get("text")
        actor: str = annotation_body.get("actor", {}).get("name", None)

        annotation_id: str = annotation_body.get("annotationId")
        created: str = annotation_body.get("created")
        created_by: str = annotation_body.get("createdBy")
        annotation = cls(type=type_, version=version, color=color, title=title, text=text, actor=actor,
                         annotation_id=annotation_id, created=created, created_by=created_by)
        return annotation

    def to_json(self) -> str:
        return f"""
       {{
            "type": "{self.type}",
            "version": "{self.version}",
            "color": "{self.color}",
            "title": "{self.title}",
            "text": "{self.text}",
            "actor":{{
                "name": "{self.actor}"
            }}
        }}
        """