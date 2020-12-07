import os.path
import yaml
import argparse


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config/config.yaml')
with open(config_path) as default:
    y_data = yaml.safe_load(default)

locked = ['version']
alternative_paths = ['$XDG_CONFIG_HOME/igcc/igcc.yaml', '$HOME/.config/igcc/igcc.yaml', '$HOME/.config/igcc.yaml']


def merge(user, default, locked):
    for k,v in default.items():
        if k in locked:
            user[k] = v
        elif k not in user:
            user[k] = v
    return user

for path in alternative_paths:
    path = os.path.expandvars(path)
    if os.path.isfile(path):
        temp_y_data = yaml.safe_load(open(path))
        y_data = merge(temp_y_data, y_data, locked)


config = argparse.Namespace(**y_data)



