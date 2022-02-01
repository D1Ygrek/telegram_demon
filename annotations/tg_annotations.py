from pydantic import BaseModel

from typing import Optional, List



class TGMessage(BaseModel):
    message_id: int
    from_: Optional[dict]
    date: int
    chat: dict
    forward_from: Optional[dict]
    forward_date: Optional[int]
    reply_to_message: Optional[dict]
    text: Optional[str]
    entities: Optional[List]
    audio: Optional[dict]
    document: Optional[dict]
    photo: Optional[List]
    sticker: Optional[dict]
    video: Optional[dict]
    voice: Optional[dict]
    caption: Optional[str]
    contact: Optional[dict]
    location: Optional[dict]
    venue: Optional[dict]
    new_chat_member: Optional[dict]
    left_chat_user: Optional[dict]
    new_chat_title: Optional[str]
    new_chat_photo: Optional[List]
    delete_chat_photo: Optional[bool]
    group_chat_created: Optional[bool]
    supergroup_chat_created: Optional[bool]
    channel_chat_created: Optional[bool]
    migrate_to_chat_id: Optional[int]
    migrate_from_chat_id: Optional[int]
    pinned_message: Optional[dict]

    class Config:
        fields = {
            'from_': 'from'
        }

class TGBody(BaseModel):
    update_id: int
    message: Optional[TGMessage]

class BackResponse(BaseModel):
    project: str
    v: str
    message: str