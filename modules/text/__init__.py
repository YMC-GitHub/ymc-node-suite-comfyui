from yors_comfyui_node_setup import entry,node_install_requirements
node_install_requirements(__file__)
__all__,NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES = entry(__name__,__file__,False)

# from . import *