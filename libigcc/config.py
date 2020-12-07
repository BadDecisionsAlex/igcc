import os.path
import yaml
import argparse

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config/config.yaml')
config = argparse.Namespace(**yaml.safe_load(open(config_path)))
