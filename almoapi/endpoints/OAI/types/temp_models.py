from typing import Optional, Union

from pydantic import BaseModel


class TempModelForGenerator(BaseModel):
    token_healing: Optional[bool] = False
    generate_window: Optional[int] = None
    temperature: Optional[float] = 1.0
    temperature_last: Optional[bool] = False
    smoothing_factor: Optional[float] = 0.0
    top_k: Optional[int] = 0
    top_p: Optional[float] = 1.0
    top_a: Optional[float] = 0.0
    min_p: Optional[float] = 0.0
    tfs: Optional[float] = 1.0
    typical: Optional[float] = 1.0
    mirostat: Optional[bool] = False
    skew: Optional[int] = 0
    xtc_probability: Optional[float] = 0.0
    xtc_threshold: Optional[float] = 0.1
    max_temp: Optional[float] = 1.0
    min_temp: Optional[float] = 1.0
    temp_exponent: Optional[float] = 1.0
    mirostat_tau: Optional[float] = 1.5
    mirostat_eta: Optional[float] = 0.1
    cfg_scale: Optional[float] = 1.0
    negative_prompt: Optional[str] = None
    repetition_penalty: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    penalty_range: Optional[int] = None
    repetition_decay: Optional[int] = None
    dry_multiplier: Optional[float] = 0.0
    dry_allowed_length: Optional[int] = 0
    dry_base: Optional[float] = 0.0
    dry_range: Optional[int] = None
    dry_sequence_breakers: Optional[list[str]] = None
    json_schema: Optional[dict] = None
    regex_pattern: Optional[str] = None
    grammar_string: Optional[str] = None
    banned_strings: Optional[list[str]] = None
    stop: Optional[list[Union[str, int]]] = None
    add_bos_token: Optional[bool] = True
    ban_eos_token: Optional[bool] = False
    logit_bias: Optional[dict] = None
    logprobs: Optional[int] = 0
    speculative_ngram: Optional[bool] = False
    max_tokens: Optional[int] = None
    min_tokens: Optional[int] = 0
    skip_special_tokens: Optional[bool] = False
    banned_tokens: Optional[list[int]] = None
    allowed_tokens: Optional[list[int]] = None
    stream: Optional[bool] = False
