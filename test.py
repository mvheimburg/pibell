
from fletbell.app import App
# from fletbell.model import GuiConfig



t = App(assets_dir="assets", cfg_dir="config.yaml", dev_mode=True)
t.deploy()
