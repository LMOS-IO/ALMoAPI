"""Common functions for sampling parameters"""

import json
from pydantic_core import ValidationError
from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from typing import Dict, List, Optional, Union


# Common class for sampler params
class BaseSamplerRequest(BaseModel):
    """Common class for sampler params that are used in APIs"""

    max_tokens: Optional[int] = Field(
        default=150,
        validation_alias=AliasChoices("max_tokens", "max_length"),
        description="Aliases: max_length",
        examples=[150],
        ge=0,
    )

    min_tokens: Optional[int] = Field(
        default=0,
        validation_alias=AliasChoices("min_tokens", "min_length"),
        description="Aliases: min_length",
        examples=[0],
        ge=0,
    )

    generate_window: Optional[int] = Field(
        default=512,
        examples=[512],
        ge=0,
    )

    stop: Optional[Union[str, List[Union[str, int]]]] = Field(
        default=[],
        validation_alias=AliasChoices("stop", "stop_sequence"),
        description="Aliases: stop_sequence",
    )

    banned_strings: Optional[Union[str, List[str]]] = Field(default=[])

    banned_tokens: Optional[Union[List[int], str]] = Field(
        default=[],
        validation_alias=AliasChoices("banned_tokens", "custom_token_bans"),
        description="Aliases: custom_token_bans",
        examples=[[128, 330]],
    )

    allowed_tokens: Optional[Union[List[int], str]] = Field(
        default=[],
        validation_alias=AliasChoices("allowed_tokens", "allowed_token_ids"),
        description="Aliases: allowed_token_ids",
        examples=[[128, 330]],
    )

    token_healing: Optional[bool] = Field(default=False)

    temperature: Optional[float] = Field(
        default=1.0,
        examples=[1.0],
        ge=0,
        le=10,
    )

    temperature_last: Optional[bool] = Field(default=False)

    smoothing_factor: Optional[float] = Field(
        default=0.0,
        ge=0,
    )

    top_k: Optional[int] = Field(
        default=0,
        ge=0,
    )

    top_p: Optional[float] = Field(
        default=1.0,
        ge=0,
        le=1,
        examples=[1.0],
    )

    top_a: Optional[float] = Field(default=0.0)

    min_p: Optional[float] = Field(default=0.0)

    tfs: Optional[float] = Field(
        default=1.0,
        examples=[1.0],
    )

    typical: Optional[float] = Field(
        default=1.0,
        validation_alias=AliasChoices("typical", "typical_p"),
        description="Aliases: typical_p",
        examples=[1.0],
        gt=0,
        le=1,
    )

    skew: Optional[float] = Field(
        default=0.0,
        examples=[0.0],
    )

    xtc_probability: Optional[float] = Field(
        default=0.0,
    )

    xtc_threshold: Optional[float] = Field(default=0.1)

    frequency_penalty: Optional[float] = Field(
        default=0.0,
        ge=0,
    )

    presence_penalty: Optional[float] = Field(
        default=0.0,
        ge=0,
    )

    repetition_penalty: Optional[float] = Field(
        default=1.0,
        validation_alias=AliasChoices("repetition_penalty", "rep_pen"),
        description="Aliases: rep_pen",
        examples=[1.0],
        gt=0,
    )

    penalty_range: Optional[int] = Field(
        default=-1,
        validation_alias=AliasChoices(
            "penalty_range",
            "repetition_range",
            "repetition_penalty_range",
            "rep_pen_range",
        ),
        description=(
            "Aliases: repetition_range, repetition_penalty_range, rep_pen_range"
        ),
    )

    repetition_decay: Optional[int] = Field(default=0)

    dry_multiplier: Optional[float] = Field(default=0.0)

    dry_base: Optional[float] = Field(default=0.0)

    dry_allowed_length: Optional[int] = Field(default=0)

    dry_range: Optional[int] = Field(
        default=0,
        validation_alias=AliasChoices("dry_range", "dry_penalty_last_n"),
        description="Aliases: dry_penalty_last_n",
    )

    dry_sequence_breakers: Optional[Union[str, List[str]]] = Field(default=[])

    mirostat: Optional[bool] = False

    mirostat_mode: Optional[int] = Field(default=0)

    mirostat_tau: Optional[float] = Field(
        default=1.5,
        examples=[1.5],
    )

    mirostat_eta: Optional[float] = Field(
        default=0.3,
        examples=[0.3],
    )

    add_bos_token: Optional[bool] = Field(default=True)

    ban_eos_token: Optional[bool] = Field(
        default=False,
        validation_alias=AliasChoices("ban_eos_token", "ignore_eos"),
        description="Aliases: ignore_eos",
        examples=[False],
    )

    skip_special_tokens: Optional[bool] = Field(
        default=True,
        examples=[True],
    )

    logit_bias: Optional[Dict[int, float]] = Field(
        default={},
        examples=[{"1": 10, "2": 50}],
    )

    negative_prompt: Optional[str] = Field(default=None)

    json_schema: Optional[object] = Field(
        default=None,
    )

    regex_pattern: Optional[str] = Field(
        default=None,
    )

    grammar_string: Optional[str] = Field(
        default=None,
    )

    speculative_ngram: Optional[bool] = Field(
        default=None,
    )

    cfg_scale: Optional[float] = Field(
        default=1.0,
        validation_alias=AliasChoices("cfg_scale", "guidance_scale"),
        description="Aliases: guidance_scale",
        examples=[1.0],
    )

    max_temp: Optional[float] = Field(
        default=1.0,
        validation_alias=AliasChoices("max_temp", "dynatemp_high"),
        description="Aliases: dynatemp_high",
        examples=[1.0],
        ge=0,
    )

    min_temp: Optional[float] = Field(
        default=1.0,
        validation_alias=AliasChoices("min_temp", "dynatemp_low"),
        description="Aliases: dynatemp_low",
        examples=[1.0],
        ge=0,
    )

    temp_exponent: Optional[float] = Field(
        default=1.0,
        validation_alias=AliasChoices("temp_exponent", "dynatemp_exponent"),
        examples=[1.0],
        ge=0,
    )

    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="after")
    def validate_params(self):
        """
        Validates sampler parameters to be within sane ranges.
        """

        if self.min_temp and self.max_temp and self.min_temp > self.max_temp:
            raise ValidationError("min temp cannot be more then max temp")

        if self.min_tokens and self.max_tokens and self.min_tokens > self.max_tokens:
            raise ValidationError("min tokens cannot be more then max tokens")

        return self

    @field_validator("stop", "banned_strings", mode="before")
    def convert_str_to_list(cls, v):
        """Convert single string to list of strings."""
        if isinstance(v, str):
            return [v]
        return v

    @field_validator("banned_tokens", "allowed_tokens", mode="before")
    def convert_tokens_to_int_list(cls, v):
        """Convert comma-separated string of numbers to a list of integers."""
        if isinstance(v, str):
            return [int(x) for x in v.split(",") if x.isdigit()]
        return v

    @field_validator("dry_sequence_breakers", mode="before")
    def parse_json_if_needed(cls, v):
        """Parse dry_sequence_breakers string to JSON array."""
        if isinstance(v, str) and not v.startswith("["):
            v = f"[{v}]"
        try:
            return json.loads(v) if isinstance(v, str) else v
        except Exception:
            return []  # Return empty list if parsing fails

    @field_validator("mirostat", mode="before")
    def convert_mirostat(cls, v, values):
        """Mirostat is enabled if mirostat_mode == 2."""
        return values.get("mirostat_mode") == 2
