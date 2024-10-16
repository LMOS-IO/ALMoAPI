import json
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Dict, List, Optional


class BaseSamplerRequest(BaseModel):
    """Common class for sampler parameters used in APIs."""

    max_tokens: int = Field(
        None, # No inital value unless client sets it
        alias="max_length",
        ge=0,
        description="Maximum number of tokens to generate.",
        examples=[150, 256],
    )
    min_tokens: int = Field(
        0,
        alias="min_length",
        ge=0,
        description="Minimum number of tokens to generate.",
        examples=[0, 10],
    )
    generate_window: int = Field(
        512,
        ge=0,
        description="The size of the generation window for the model.",
        examples=[512, 1024],
    )
    stop: List[str] = Field(
        default_factory=list,
        alias="stop_sequence",
        description="Sequences that will cause the model to stop generation.",
        examples=[[".", "\n"]],
    )
    banned_strings: List[str] = Field(
        default_factory=list,
        description="Strings that should not appear in the generated output.",
        examples=[["banned_word1", "banned_word2"]],
    )
    banned_tokens: List[int] = Field(
        default_factory=list,
        alias="custom_token_bans",
        description="List of token IDs that should not appear in the output.",
        examples=[[128, 330]],
    )
    allowed_tokens: List[int] = Field(
        default_factory=list,
        alias="allowed_token_ids",
        description="List of token IDs that are allowed to be used.",
        examples=[[128, 330]],
    )
    token_healing: bool = Field(
        False,
        description="Enables token healing to improve text generation quality.",
        examples=[True],
    )
    temperature: float = Field(
        0,
        ge=0,
        le=10,
        description="Controls randomness in generation; "
        + "lower values make output more deterministic.",
        examples=[1.0, 0.7, 2.0],
    )
    temperature_last: bool = Field(
        False,
        description="Applies temperature scaling only"
        + "to the final token in the sequence.",
        examples=[False, True],
    )
    smoothing_factor: float = Field(
        0.0,
        ge=0,
        description="Smoothing factor for probability distribution.",
        examples=[0.0, 0.5],
    )
    top_k: int = Field(
        0,
        ge=0,
        description="Limits the next token choices to the top K most likely tokens.",
        examples=[0, 50, 100],
    )
    top_p: float = Field(
        1.0,
        ge=0,
        le=1,
        description="Limits the next token choices to a cumulative probability.",
        examples=[1.0, 0.9, 0.7],
    )
    top_a: float = Field(
        0.0,
        description="Controls the threshold to add diversity in sampling.",
        examples=[0.0, 0.5],
    )
    min_p: float = Field(
        0.0,
        description="Minimum cumulative probability"
        + "threshold for next token selection.",
        examples=[0.0, 0.2],
    )
    tfs: float = Field(
        1.0, description="Tail free sampling value.", examples=[1.0, 0.9]
    )
    typical: float = Field(
        1.0,
        alias="typical_p",
        gt=0,
        le=1,
        description="Typical sampling, a strategy to ensure "
        + "the generated text follows typical use cases.",
        examples=[1.0, 0.8],
    )
    skew: float = Field(
        0.0,
        description="Skew factor for token selection probability distribution.",
        examples=[0.0, 0.1],
    )
    xtc_probability: float = Field(
        0.0,
        description="Probability of applying the"
        + "Exclude Top Choices (XTC) sampling method.",
        examples=[0.0, 0.4],
    )
    xtc_threshold: float = Field(
        0.1,
        description="Threshold for determining which tokens"
        + "are excluded by the XTC sampler.",
        examples=[0.1, 0.3],
    )
    frequency_penalty: float = Field(
        0.0,
        ge=0,
        description="Penalty applied to repeated tokens based on frequency.",
        examples=[0.0, 0.5],
    )
    presence_penalty: float = Field(
        0.0,
        ge=0,
        description="Penalty for tokens that have already appeared in the text.",
        examples=[0.0, 0.6],
    )
    repetition_penalty: float = Field(
        1.0,
        alias="rep_pen",
        gt=0,
        description="Penalty factor applied to repeated tokens.",
        examples=[1.0, 1.2],
    )
    penalty_range: int = Field(
        -1,
        alias="rep_pen_range",
        description="Range over which the repetition penalty is applied.",
        examples=[-1, 20],
    )
    repetition_decay: int = Field(
        0,
        description="Controls decay of repetition penalty over tokens.",
        examples=[0, 10],
    )
    dry_multiplier: float = Field(
        0.0, description="Multiplier for dry run scoring.", examples=[0.0, 1.5]
    )
    dry_base: float = Field(
        0.0, description="Base value used in dry run calculations.", examples=[0.0, 2.0]
    )
    dry_allowed_length: int = Field(
        0,
        description="The length allowed before dry penalty takes effect.",
        examples=[0, 15],
    )
    dry_range: int = Field(
        0,
        alias="dry_penalty_last_n",
        description="Range for dry penalty application.",
        examples=[0, 5],
    )
    dry_sequence_breakers: List[str] = Field(
        default_factory=list,
        description="Sequence breakers for dry penalty calculation.",
        examples=[["breaker1", "breaker2"]],
    )
    mirostat: bool = Field(
        False, description="Enables the Mirostat sampling algorithm.", examples=[True]
    )
    mirostat_mode: int = Field(
        0,
        description="Set Mirostat mode; different modes for different behaviors.",
        examples=[0, 2],
    )
    mirostat_tau: float = Field(
        1.5,
        description="Controls the target mean entropy for Mirostat.",
        examples=[1.5, 2.0],
    )
    mirostat_eta: float = Field(
        0.3,
        description="Controls the learning rate for entropy adjustments in Mirostat.",
        examples=[0.3, 0.5],
    )
    add_bos_token: bool = Field(
        True,
        description="Indicates whether to add a beginning-of-sequence (BOS) token.",
        examples=[True, False],
    )
    ban_eos_token: bool = Field(
        False,
        alias="ignore_eos",
        description="Prevents the end-of-sequence (EOS) token from being used.",
        examples=[False, True],
    )
    skip_special_tokens: bool = Field(
        True,
        description="Skip special tokens during generation.",
        examples=[True, False],
    )
    logit_bias: Dict[int, float] = Field(
        default_factory=dict,
        description="Adjusts the probability of specific tokens via bias values.",
        examples=[{1: 10.0, 2: -5.0}],
    )
    negative_prompt: Optional[str] = Field(
        None,
        description="A prompt to negatively influence the generated content.",
        examples=["Do not generate violent content."],
    )
    json_schema: Optional[object] = Field(
        None, description="Optional JSON schema for structure validation."
    )
    regex_pattern: Optional[str] = Field(
        None,
        description="Regular expression pattern to validate generated output.",
        examples=["[A-Za-z0-9]+"],
    )
    grammar_string: Optional[str] = Field(
        None, description="Grammar string used for advanced parsing requirements."
    )
    speculative_ngram: Optional[bool] = Field(
        None,
        description="Enable speculative n-gram processing for improved prediction.",
        examples=[True],
    )
    cfg_scale: float = Field(
        1.0,
        alias="guidance_scale",
        description="Scale for classifier-free guidance during generation.",
        examples=[1.0, 3.0],
    )
    max_temp: float = Field(
        1.0,
        alias="dynatemp_high",
        ge=0,
        description="Maximum temperature for dynamic adjustment.",
        examples=[1.0, 2.5],
    )
    min_temp: float = Field(
        1.0,
        alias="dynatemp_low",
        ge=0,
        description="Minimum temperature for dynamic adjustment.",
        examples=[0.5, 1.0],
    )
    temp_exponent: float = Field(
        1.0,
        alias="dynatemp_exponent",
        ge=0,
        description="Exponent for temperature scaling calculations.",
        examples=[1.0, 0.8],
    )

    model_config = ConfigDict(validate_assignment=True, populate_by_name=True)

    @model_validator(mode="after")
    def validate_params(self):
        """Validates sampler parameters to be within sane ranges."""
        if self.min_temp > self.max_temp:
            raise ValueError("min_temp cannot be greater than max_temp")
        
        if self.max_tokens is not None and self.min_tokens > self.max_tokens:
            # for the case where user overrides to min > max
            raise ValueError("min_tokens cannot be greater than max_tokens")

        # Enable mirostat based on mirostat_mode
        if self.mirostat_mode == 2:
            self.mirostat = True

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
        except json.JSONDecodeError:
            return []
