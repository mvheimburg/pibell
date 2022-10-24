
import pathlib
from pathlib import Path
import yaml
from os import environ


# def cfg_loader(cfg_path:Path=None):
#     if cfg_path is None:
#         return cfg_loader_env()
#     else:
#         return cfg_loader_yaml(cfg_path)


def cfg_loader(cfg_path:Path):

    if not cfg_path.startswith("/"):
        x = cfg_path.split("/")
        cfg_path=pathlib.Path().parent.resolve()
        print(cfg_path)
        for p in x:
            if p == "..":
                cfg_path = cfg_path.parent
            else:
                cfg_path = cfg_path / p
            print(cfg_path)
    # cfg_path = cfg_path/"config.yaml"
    with open(cfg_path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.FullLoader)
    
    # print(cfg)

    # cfg_= Config(**cfg)

    return cfg


# def cfg_loader_env():

#     MQTT_BROKER     =environ.get('MQTT_BROKER','mqtt')
#     MQTT_PORT       =int(environ.get('MQTT_PORT',1883))
#     MQTT_USERNAME   =environ.get('MQTT_USERNAME','mqtt')
#     MQTT_PASSWORD   =environ.get('MQTT_PASSWORD','mqtt')
#     MQTT_CLIENT_ID  =environ.get('MQTT_CLIENT_ID','mqtt')

#     LOCKMASTER_URL  =environ.get('LOCKMASTER_URL','lockmaster')

#     #TODO: Fix all env get

    return None