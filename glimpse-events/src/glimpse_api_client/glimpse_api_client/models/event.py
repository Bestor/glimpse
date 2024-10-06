import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location import Location
    from ..models.transcription import Transcription


T = TypeVar("T", bound="Event")


@_attrs_define
class Event:
    """
    Attributes:
        description (str): A description of the event.
        timestamp (datetime.datetime): The time the event occurred.
        id (Union[Unset, str]): Unique identifier for the event.
        location (Union[Unset, Location]):
        transcriptions (Union[Unset, List['Transcription']]):
    """

    description: str
    timestamp: datetime.datetime
    id: Union[Unset, str] = UNSET
    location: Union[Unset, "Location"] = UNSET
    transcriptions: Union[Unset, List["Transcription"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        timestamp = self.timestamp.isoformat()

        id = self.id

        location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.location, Unset):
            location = self.location.to_dict()

        transcriptions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.transcriptions, Unset):
            transcriptions = []
            for transcriptions_item_data in self.transcriptions:
                transcriptions_item = transcriptions_item_data.to_dict()
                transcriptions.append(transcriptions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "timestamp": timestamp,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if location is not UNSET:
            field_dict["location"] = location
        if transcriptions is not UNSET:
            field_dict["transcriptions"] = transcriptions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.location import Location
        from ..models.transcription import Transcription

        d = src_dict.copy()
        description = d.pop("description")

        timestamp = isoparse(d.pop("timestamp"))

        id = d.pop("id", UNSET)

        _location = d.pop("location", UNSET)
        location: Union[Unset, Location]
        if isinstance(_location, Unset):
            location = UNSET
        else:
            location = Location.from_dict(_location)

        transcriptions = []
        _transcriptions = d.pop("transcriptions", UNSET)
        for transcriptions_item_data in _transcriptions or []:
            transcriptions_item = Transcription.from_dict(transcriptions_item_data)

            transcriptions.append(transcriptions_item)

        event = cls(
            description=description,
            timestamp=timestamp,
            id=id,
            location=location,
            transcriptions=transcriptions,
        )

        event.additional_properties = d
        return event

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
