import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Transcription")


@_attrs_define
class Transcription:
    """
    Attributes:
        content (str): The content of the transcription.
        audio (str): The path to the original recording.
        timestamp (datetime.datetime): The time the transcription was created.
        id (Union[Unset, str]): Unique identifier for the transcription.
    """

    content: str
    audio: str
    timestamp: datetime.datetime
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content

        audio = self.audio

        timestamp = self.timestamp.isoformat()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "audio": audio,
                "timestamp": timestamp,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content")

        audio = d.pop("audio")

        timestamp = isoparse(d.pop("timestamp"))

        id = d.pop("id", UNSET)

        transcription = cls(
            content=content,
            audio=audio,
            timestamp=timestamp,
            id=id,
        )

        transcription.additional_properties = d
        return transcription

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
