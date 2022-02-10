# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401


class IndyRequestedCredsRequestedPred(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    IndyRequestedCredsRequestedPred - a model defined in OpenAPI

        cred_id: The cred_id of this IndyRequestedCredsRequestedPred.
        timestamp: The timestamp of this IndyRequestedCredsRequestedPred [Optional].
    """

    cred_id: str
    timestamp: Optional[int] = None

    @validator("timestamp")
    def timestamp_max(cls, value):
        assert value <= -1
        return value

    @validator("timestamp")
    def timestamp_min(cls, value):
        assert value >= 0
        return value


IndyRequestedCredsRequestedPred.update_forward_refs()