from pydantic import BaseModel, Field, field_validator, ConfigDict
import sys

from app.models.commons.values import Event, Source

class CollectInteraction(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    
    id_: str = Field(alias="id")
    source: Source
    event: Event
    user_ids: list[str] = Field(alias="userIds")

    @field_validator("id_")
    @classmethod
    def intern_ids(cls, v: str) -> str:
        return sys.intern(v)

    @field_validator("user_ids")
    @classmethod
    def intern_user_ids(cls, v: list[str]) -> list[str]:
        return [sys.intern(uid) for uid in v if isinstance(uid, str)]

class UpdateInteraction(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id_: str = Field(alias="id")
    user_ids: list[str] = Field(alias="userIds")

    @field_validator("id_")
    @classmethod
    def intern_ids(cls, v: str) -> str:
        return sys.intern(v)

    @field_validator("user_ids")
    @classmethod
    def intern_user_ids(cls, v: list[str]) -> list[str]:
        return [sys.intern(uid) for uid in v if isinstance(uid, str)]