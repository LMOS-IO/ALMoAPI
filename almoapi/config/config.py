import pathlib
from inspect import getdoc
from os import getenv
from textwrap import dedent
from typing import Optional

from loguru import logger
from pydantic import BaseModel
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import PreservedScalarString

from config.models import BaseConfigModel, TabbyConfigModel
from common.utils import merge_dicts, filter_none_values, unwrap

yaml = YAML(typ=["rt", "safe"])
yaml.representer.add_representer(pathlib.Path, pathlib.Path.as_posix)


class TabbyConfig(TabbyConfigModel):
    # Persistent defaults
    # TODO: make this pydantic?
    model_defaults: dict = {}

    def load(self, arguments: Optional[dict] = None):
        """Synchronously loads the global application config"""

        # config is applied in order of items in the list
        arguments_dict = unwrap(arguments, {})
        configs = [self._from_environment(), self._from_args(arguments_dict)]

        # If actions aren't present, also look from the file
        # TODO: Change logic if file loading requires actions in the future
        if not arguments_dict.get("actions"):
            configs.insert(0, self._from_file(pathlib.Path("config.yml")))

        # Remove None (aka unset) values from the configs and merge them together
        # This should be less expensive than pruning the entire merged dictionary
        configs = filter_none_values(configs)
        merged_config = merge_dicts(*configs)
        merged_config = filter_none_values(merged_config)

        # validate and update config
        merged_config_model = TabbyConfigModel(**merged_config)
        for field in TabbyConfigModel.model_fields.keys():
            value = getattr(merged_config_model, field)
            setattr(self, field, value)

        # Set model defaults dict once to prevent on-demand reconstruction
        # TODO: clean this up a bit
        for field in self.model.use_as_default:
            if hasattr(self.model, field):
                self.model_defaults[field] = getattr(config.model, field)
            elif hasattr(self.draft_model, field):
                self.model_defaults[field] = getattr(config.draft_model, field)
            else:
                logger.error(
                    f"invalid item {field} in config option `model.use_as_default`"
                )

    def _from_file(self, config_path: pathlib.Path):
        """loads config from a given file path"""

        cfg = {}

        # try loading from file
        try:
            with open(str(config_path.resolve()), "r", encoding="utf8") as config_file:
                cfg = yaml.load(config_file)
                logger.info(f"The '{config_path.name}' file was loaded")
        except FileNotFoundError:
            logger.info(f"The '{config_path.name}' file cannot be found")
        except Exception as exc:
            logger.error(
                f"The YAML config from '{config_path.name}' couldn't load because of "
                f"the following error:\n\n{exc}"
            )

        return unwrap(cfg, {})

    def _from_args(self, args: dict):
        """loads config from the provided arguments"""
        config = {}

        config_override = args.get("config", {}).get("config", None)
        if config_override:
            logger.info("Config file override detected in args.")
            config = self._from_file(pathlib.Path(config_override))
            return config  # Return early if loading from file

        for key in TabbyConfigModel.model_fields.keys():
            override = args.get(key)
            if override:
                config[key] = override

        return config

    def _from_environment(self):
        """loads configuration from environment variables"""

        config = {}

        for field_name in TabbyConfigModel.model_fields.keys():
            section_config = {}
            for sub_field_name in getattr(
                TabbyConfigModel(), field_name
            ).model_fields.keys():
                setting = getenv(f"TABBY_{field_name}_{sub_field_name}".upper(), None)
                if setting is not None:
                    section_config[sub_field_name] = setting

            config[field_name] = section_config

        return config


# Create an empty instance of the config class
config: TabbyConfig = TabbyConfig()


def generate_config_file(
    model: Optional[BaseModel] = None,
    filename: Optional[pathlib.Path] = None,
) -> None:
    """Creates a config.yml file from Pydantic models."""

    file = unwrap(filename, "config_sample.yml")
    schema = unwrap(model, TabbyConfigModel())
    preamble = """
    # Sample YAML file for configuration.
    # Comment and uncomment values as needed.
    # Every value has a default within the application.
    # This file serves to be a drop in for config.yml

    # Unless specified in the comments, DO NOT put these options in quotes!
    # You can use https://www.yamllint.com/ if you want to check your YAML formatting.\n
    """

    yaml_content = pydantic_model_to_yaml(schema)

    with open(file, "w") as f:
        f.write(dedent(preamble).lstrip())
        yaml.dump(yaml_content, f)


def pydantic_model_to_yaml(model: BaseModel, indentation: int = 0) -> CommentedMap:
    """
    Recursively converts a Pydantic model into a CommentedMap,
    with descriptions as comments in YAML.
    """

    # Create a CommentedMap to hold the output data
    yaml_data = CommentedMap()

    # Loop through all fields in the model
    iteration = 1
    for field_name, field_info in model.model_fields.items():
        # Get the inner pydantic model
        value = getattr(model, field_name)

        if isinstance(value, BaseConfigModel):
            # If the field is another config model

            if not value._metadata.include_in_config:
                continue

            yaml_data[field_name] = pydantic_model_to_yaml(
                value, indentation=indentation + 2
            )
            comment = getdoc(value)
        elif isinstance(value, BaseModel):
            # If the field is another Pydantic model

            yaml_data[field_name] = pydantic_model_to_yaml(
                value, indentation=indentation + 2
            )
            comment = getdoc(value)
        elif isinstance(value, list) and len(value) > 0:
            # If the field is a list

            yaml_list = CommentedSeq()
            if isinstance(value[0], BaseModel):
                # If the field is a list of Pydantic models
                # Do not add comments for these items

                for item in value:
                    yaml_list.append(
                        pydantic_model_to_yaml(item, indentation=indentation + 2)
                    )
            else:
                # If the field is a normal list, prefer the YAML flow style

                yaml_list.fa.set_flow_style()
                yaml_list += [
                    PreservedScalarString(element)
                    if isinstance(element, str)
                    else element
                    for element in value
                ]

            yaml_data[field_name] = yaml_list
            comment = field_info.description
        else:
            # Otherwise, just assign the value

            yaml_data[field_name] = value
            comment = field_info.description

        if comment:
            # Add a newline to every comment but the first one
            if iteration != 1:
                comment = f"\n{comment}"

            yaml_data.yaml_set_comment_before_after_key(
                field_name, before=comment, indent=indentation
            )
        else:
            comment = "\n"

        # Increment the iteration counter
        iteration += 1

    return yaml_data
