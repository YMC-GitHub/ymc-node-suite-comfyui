# v1
# from yors_comfyui_node_setup import entry,node_install_requirements # global

# # install requirements
# node_install_requirements(__file__)

# # export comfyui node vars
# __all__,NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES = entry(__name__,__file__)

# v2
from yors_comfyui_node_setup import node_install_requirements,entry_pre_import,entry_import,get_all_classs_in_sys,register_node_list_local

# install requirements
node_install_requirements(__file__)

# gen __all__
__all__ = entry_pre_import(__name__,__file__)

# import moudle with __all__
entry_import(__name__,__all__)

# get class after importing moudle with __all__
this_module_all_classes = get_all_classs_in_sys(__name__)

# register node with default category
# NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES  = register_node_list(this_module_all_classes,False)

# addtional register node with custom category
NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES  = register_node_list_local(this_module_all_classes,True,"ymc/suite")
# print(NODE_CLASS_MAPPINGS,NODE_DISPLAY_NAME_MAPPINGS,NODE_MENU_NAMES)
print("\n".join(NODE_MENU_NAMES))