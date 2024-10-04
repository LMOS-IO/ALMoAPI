from pydantic import BaseModel, Field, PrivateAttr

class Metadata(BaseModel):
    """metadata model for config options"""

    include_in_config: bool = Field(
        True, description="if the model is included by the config file generator"
    )


class BaseConfigModel(BaseModel):
    """Base model for config models with added metadata"""

    _metadata: Metadata = PrivateAttr(Metadata())