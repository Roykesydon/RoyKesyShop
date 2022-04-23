import yaml


def get_config():
    with open("./config.yml", "r") as f:
        cfg = yaml.safe_load(f)
        return cfg
