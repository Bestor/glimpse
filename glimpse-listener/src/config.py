import yaml
import os

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return replace_env_vars(config)

def replace_env_vars(config):
    for key, value in config.items():
        if isinstance(value, dict):
            config[key] = replace_env_vars(value)
        elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            config[key] = os.getenv(env_var, value)  # Replace with the env var or keep the placeholder if not found
    return config
