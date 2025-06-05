# v1
# from yors_comfyui_node_setup import entry,node_install_requirements # global

# # install requirements
# node_install_requirements(__file__)

# # export comfyui node vars
# __all__,NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES = entry(__name__,__file__)

# v4
import os
from yors_comfyui_node_setup import custom_nodes_get_path,custom_nodes_add_to_sys,import_custom_node_module,node_install_requirements,get_module_name_contains_x_in_sys,get_node_class_in_sys_modules,register_node_list_local
from yors_pano_ansi_color import info_status,info_step,msg_padd,log_msg
import importlib

info_step("add comfui/custom_nodes to sys.path")
custom_nodes_path = [custom_nodes_get_path(__file__,'../../custom_nodes')]
custom_nodes_add_to_sys(custom_nodes_path)

info_step("import modules in sub diretory modules")
import_custom_node_module(os.path.dirname(__file__),__name__,"modules")

# info_step(f"install deps (not installed) in requirements.txt if file exits")
# node_install_requirements(__file__)

# info_step(f"read name in sys.modules if name including name")
# - custom_node_module_class_name_list = read_module_class_name(__name__)
# custom_node_module_class_name_list = get_module_name_contains_x_in_sys(__name__)

info_step(f"read valid node class if key in sys.modules including this module name")
# - NodeClassList,NodeClassNameList = read_module_valid_node_class(__name__)
NodeClassList,NodeClassNameList = get_node_class_in_sys_modules(__name__)

info_step(f"make node_class_mappings and node_display_name_mappings {__name__}")
NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES = register_node_list_local(NodeClassList)

info_step(f"print node name of {__name__}")
NODE_MENU_NAMES.sort()
# print("\n".join(NODE_MENU_NAMES))


# register node with default category
# - NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES  = register_node_list(this_module_all_classes,False)
# NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES  = register_node_list_local(this_module_all_classes,False)

# addtional register node with custom category
# NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES  = register_node_list_local(this_module_all_classes,True,"ymc/suite")
# print(NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES)
# print("\n".join(NODE_MENU_NAMES))

# info_step(f"define __all__ (not web ext) {__name__}")
# __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

info_step(f"define __all__ (support web ext) {__name__}")
WEB_DIRECTORY = "./web"
# docs(core): export NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,WEB_DIRECTORY
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

# get version from pyproject.toml
# ...
version="3.0.0"

log_msg(msg_padd("=",60,"="))
log_msg(msg_padd("welocme to ymc_node_suite_comfyui",60,"="))
log_msg(f'version: {version}')
log_msg(f'node counts:{len(NODE_MENU_NAMES)}')
log_msg(f'node menu names:')
for node_name in NODE_MENU_NAMES:
    # log_msg(f'node name:{node_name}')
    info_status(f'{node_name}',0)
log_msg(msg_padd("=",60,"="))