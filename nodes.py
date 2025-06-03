
# [save text file of was node suite](D:\code\python\comfyui\custom_nodes\was-node-suite-comfyui\WAS_Node_Suite.py)

# from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops, ImageFont
# from PIL.PngImagePlugin import PngInfo
# from io import BytesIO
# from typing import Optional
from typing import Callable, List, Dict, Any, Union, Tuple, cast,Optional
from urllib.request import urlopen
# import comfy.diffusers_convert
# import comfy.samplers
# import comfy.sd
# import comfy.utils
# import comfy.clip_vision
# import model_management
import folder_paths as comfy_paths
# from comfy_extras.chainner_models import model_loading
import glob
import hashlib
import json
# import nodes
# import math
# import numpy as np
from numba import jit
import os
import random
import re
# import requests
import socket
# import subprocess
import sys
import time
# import torch
# from tqdm import tqdm

# define manifest about this project in dict
MANIFEST = {
    "name": "ymc node suite",
    "version": (1,0,0),
    "author": "ymc-github",
    "project": "https://github.com/ymc-github/ymc-node-suite-comfyui",
    "description": "an extensive node suite for comfyui",
}

#! SET SYS PATH
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "ymc_node_suite_comfyui"))
sys.path.append(comfy_paths.base_path)


#! SYSTEM HOOKS
"""color str"""
class cstr(str):
    class color:
        END = '\33[0m'
        BOLD = '\33[1m'
        ITALIC = '\33[3m'
        UNDERLINE = '\33[4m'
        BLINK = '\33[5m'
        BLINK2 = '\33[6m'
        SELECTED = '\33[7m'

        BLACK = '\33[30m'
        RED = '\33[31m'
        GREEN = '\33[32m'
        YELLOW = '\33[33m'
        BLUE = '\33[34m'
        VIOLET = '\33[35m'
        BEIGE = '\33[36m'
        WHITE = '\33[37m'

        BLACKBG = '\33[40m'
        REDBG = '\33[41m'
        GREENBG = '\33[42m'
        YELLOWBG = '\33[43m'
        BLUEBG = '\33[44m'
        VIOLETBG = '\33[45m'
        BEIGEBG = '\33[46m'
        WHITEBG = '\33[47m'

        GREY = '\33[90m'
        LIGHTRED = '\33[91m'
        LIGHTGREEN = '\33[92m'
        LIGHTYELLOW = '\33[93m'
        LIGHTBLUE = '\33[94m'
        LIGHTVIOLET = '\33[95m'
        LIGHTBEIGE = '\33[96m'
        LIGHTWHITE = '\33[97m'

        GREYBG = '\33[100m'
        LIGHTREDBG = '\33[101m'
        LIGHTGREENBG = '\33[102m'
        LIGHTYELLOWBG = '\33[103m'
        LIGHTBLUEBG = '\33[104m'
        LIGHTVIOLETBG = '\33[105m'
        LIGHTBEIGEBG = '\33[106m'
        LIGHTWHITEBG = '\33[107m'

        @staticmethod
        def add_code(name, code):
            if not hasattr(cstr.color, name.upper()):
                setattr(cstr.color, name.upper(), code)
            else:
                raise ValueError(f"'cstr' object already contains a code with the name '{name}'.")

    def __new__(cls, text):
        return super().__new__(cls, text)

    def __getattr__(self, attr):
        if attr.lower().startswith("_cstr"):
            code = getattr(self.color, attr.upper().lstrip("_cstr"))
            modified_text = self.replace(f"__{attr[1:]}__", f"{code}")
            return cstr(modified_text)
        elif attr.upper() in dir(self.color):
            code = getattr(self.color, attr.upper())
            modified_text = f"{code}{self}{self.color.END}"
            return cstr(modified_text)
        elif attr.lower() in dir(cstr):
            return getattr(cstr, attr.lower())
        else:
            raise AttributeError(f"'cstr' object has no attribute '{attr}'")

    def print(self, **kwargs):
        print(self, **kwargs)
        
#! MESSAGE TEMPLATES
cstr.color.add_code("msg", f"{cstr.color.BLUE}Ymc Node Suite: {cstr.color.END}")
cstr.color.add_code("warning", f"{cstr.color.BLUE}Ymc Node Suite {cstr.color.LIGHTYELLOW}Warning: {cstr.color.END}")
cstr.color.add_code("error", f"{cstr.color.RED}Ymc Node Suite {cstr.color.END}Error: {cstr.color.END}")



#! GLOBALS
NODE_FILE = os.path.abspath(__file__)
MIDAS_INSTALLED = False
CUSTOM_NODES_DIR = comfy_paths.folder_names_and_paths["custom_nodes"][0][0]
MODELS_DIR =  comfy_paths.models_dir
WAS_SUITE_ROOT = os.path.dirname(NODE_FILE)
WAS_DATABASE = os.path.join(WAS_SUITE_ROOT, 'was_suite_settings.json')
WAS_HISTORY_DATABASE = os.path.join(WAS_SUITE_ROOT, 'was_history.json')
WAS_CONFIG_FILE = os.path.join(WAS_SUITE_ROOT, 'was_suite_config.json')
STYLES_PATH = os.path.join(WAS_SUITE_ROOT, 'styles.json')
ALLOWED_EXT = ('.jpeg', '.jpg', '.png',
                        '.tiff', '.gif', '.bmp', '.webp')
                        


#! INSTALLATION CLEANUP

# Delete legacy nodes
legacy_was_nodes = ['fDOF_WAS.py', 'Image_Blank_WAS.py', 'Image_Blend_WAS.py', 'Image_Canny_Filter_WAS.py', 'Canny_Filter_WAS.py', 'Image_Combine_WAS.py', 'Image_Edge_Detection_WAS.py', 'Image_Film_Grain_WAS.py', 'Image_Filters_WAS.py',
                    'Image_Flip_WAS.py', 'Image_Nova_Filter_WAS.py', 'Image_Rotate_WAS.py', 'Image_Style_Filter_WAS.py', 'Latent_Noise_Injection_WAS.py', 'Latent_Upscale_WAS.py', 'MiDaS_Depth_Approx_WAS.py', 'NSP_CLIPTextEncoder.py', 'Samplers_WAS.py']
legacy_was_nodes_found = []

WAS_NODES_DIR_NAME="ymc-node-suite-comfyui"
WAS_NODES_INDEX="Ymc_Node_Suite.py"
if os.path.basename(CUSTOM_NODES_DIR) == WAS_NODES_DIR_NAME:
    legacy_was_nodes.append(WAS_NODES_INDEX)

f_disp = False
node_path_dir = os.getcwd()+os.sep+'ComfyUI'+os.sep+'custom_nodes'+os.sep
for f in legacy_was_nodes:
    file = f'{node_path_dir}{f}'
    if os.path.exists(file):
        if not f_disp:
            cstr("Found legacy nodes. Archiving legacy nodes...").msg.print()
            f_disp = True
        legacy_was_nodes_found.append(file)

if legacy_was_nodes_found:
    import zipfile
    from os.path import basename
    archive = zipfile.ZipFile(
        f'{node_path_dir}WAS_Legacy_Nodes_Backup_{round(time.time())}.zip', "w")
    for f in legacy_was_nodes_found:
        archive.write(f, basename(f))
        try:
            os.remove(f)
        except OSError:
            pass
    archive.close()

if f_disp:
    cstr("Legacy cleanup complete.").msg.print()
    
#! WAS SUITE CONFIG

was_conf_template = {
                    "run_requirements": True,
                    "suppress_uncomfy_warnings": True,
                    "show_startup_junk": True,
                    "show_inspiration_quote": True,
                    "text_nodes_type": "STRING",
                    "webui_styles": None,
                    "webui_styles_persistent_update": True,
                    "blip_model_url": "https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth",
                    "blip_model_vqa_url": "https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_vqa_capfilt_large.pth",
                    "sam_model_vith_url": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
                    "sam_model_vitl_url": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth",
                    "sam_model_vitb_url": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth",
                    "history_display_limit": 36,
                    "use_legacy_ascii_text": False,
                    "ffmpeg_bin_path": "/path/to/ffmpeg",
                    "ffmpeg_extra_codecs": {
                        "avc1": ".mp4",
                        "h264": ".mkv",
                    },
                    "wildcards_path": os.path.join(WAS_SUITE_ROOT, "wildcards"),
                    "wildcard_api": True,
                }

# Create, Load, or Update Config
def getSuiteConfig():
    global was_conf_template
    try:
        with open(WAS_CONFIG_FILE, "r") as f:
            was_config = json.load(f)
    except OSError as e:
        cstr(f"Unable to load conf file at `{WAS_CONFIG_FILE}`. Using internal config template.").error.print()
        return was_conf_template
    except Exception as e:
        cstr(f"Unable to load conf file at `{WAS_CONFIG_FILE}`. Using internal config template.").error.print()
        return was_conf_template
    return was_config
    
def updateSuiteConfig(conf):
    try:
        with open(WAS_CONFIG_FILE, "w", encoding='utf-8') as f:
            json.dump(conf, f, indent=4)
    except OSError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False
    return True

if not os.path.exists(WAS_CONFIG_FILE):
    if updateSuiteConfig(was_conf_template):
        cstr(f'Created default conf file at `{WAS_CONFIG_FILE}`.').msg.print()
        was_config = getSuiteConfig()
    else:
        cstr(f"Unable to create default conf file at `{WAS_CONFIG_FILE}`. Using internal config template.").error.print()
        was_config = was_conf_template
    
else:
    was_config = getSuiteConfig()
    
    update_config = False
    for sett_ in was_conf_template.keys():
        if not was_config.__contains__(sett_):
            was_config.update({sett_: was_conf_template[sett_]})
            update_config = True
       
    if update_config:
        updateSuiteConfig(was_config)


# WAS SETTINGS MANAGER

class WASDatabase:
    """
    The WAS Suite Database Class provides a simple key-value database that stores 
    data in a flatfile using the JSON format. Each key-value pair is associated with 
    a category.

    Attributes:
        filepath (str): The path to the JSON file where the data is stored.
        data (dict): The dictionary that holds the data read from the JSON file.

    Methods:
        insert(category, key, value): Inserts a key-value pair into the database
            under the specified category.
        get(category, key): Retrieves the value associated with the specified
            key and category from the database.
        update(category, key): Update a value associated with the specified
            key and category from the database.
        delete(category, key): Deletes the key-value pair associated with the
            specified key and category from the database.
        _save(): Saves the current state of the database to the JSON file.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        try:
            with open(filepath, 'r') as f:
                 self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

    def catExists(self, category):
        return self.data.__contains__(category)
        
    def keyExists(self, category, key):
        return self.data[category].__contains__(key)

    def insert(self, category, key, value):
        if category not in self.data:
            self.data[category] = {}
        self.data[category][key] = value
        self._save()

    def update(self, category, key, value):
        if category in self.data and key in self.data[category]:
            self.data[category][key] = value
            self._save()
            
    def updateCat(self, category, dictionary):
        self.data[category].update(dictionary)
        self._save()
        
    def get(self, category, key):
        return self.data.get(category, {}).get(key, None)
        
    def getDB(self):
        return self.data
        
    def insertCat(self, category):
        if self.data.__contains__(category):
            cstr(f"The database category `{category}` already exists!").error.print()
            return
        self.data[category] = {}
        self._save()
        
    def getDict(self, category):
        if not self.data.__contains__(category):
            cstr(f"\033[34mYmc Node Suite\033[0m Error: The database category `{category}` does not exist!").error.print()
        return self.data[category]

    def delete(self, category, key):
        if category in self.data and key in self.data[category]:
            del self.data[category][key]
            self._save()

    def _save(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except FileNotFoundError:
            cstr(f"Cannot save database to file '{self.filepath}'."
                  " Storing the data in the object instead. Does the folder and node file have write permissions?").warning.print()

# Initialize the settings database
WDB = WASDatabase(WAS_DATABASE)

# WAS Token Class

class TextTokens:
    def __init__(self):
        self.WDB = WDB
        if not self.WDB.getDB().__contains__('custom_tokens'):
            self.WDB.insertCat('custom_tokens')
        self.custom_tokens = self.WDB.getDict('custom_tokens')
                
        self.tokens =  {
            '[time]': str(time.time()).replace('.','_'),
            '[hostname]': socket.gethostname(),
        }

        if '.' in self.tokens['[time]']:
            self.tokens['[time]'] = self.tokens['[time]'].split('.')[0]

        try:
            self.tokens['[user]'] = ( os.getlogin() if os.getlogin() else 'null' )
        except Exception:
            self.tokens['[user]'] = 'null'
                
    def addToken(self, name, value):
        self.custom_tokens.update({name: value})
        self._update()
                
    def removeToken (self, name):
        self.custom_tokens.pop(name)
        self._update()
        
    def format_time(self, format_code):
        return time.strftime(format_code, time.localtime(time.time()))
        
    def parseTokens(self, text):
        tokens = self.tokens.copy()

        if self.custom_tokens:
            tokens.update(self.custom_tokens)

        # Update time
        tokens['[time]'] = str(time.time())
        if '.' in tokens['[time]']:
            tokens['[time]'] = tokens['[time]'].split('.')[0]

        for token, value in tokens.items():
            if token.startswith('[time('):
                continue
            text = text.replace(token, value)

        def replace_custom_time(match):
            format_code = match.group(1)
            return self.format_time(format_code)

        text = re.sub(r'\[time\((.*?)\)\]', replace_custom_time, text)

        return text
                
    def _update(self):
        self.WDB.updateCat('custom_tokens', self.custom_tokens)


# Update text file history

def update_history_text_files(new_paths):
    HDB = WASDatabase(WAS_HISTORY_DATABASE)
    if HDB.catExists("History") and HDB.keyExists("History", "TextFiles"):
        saved_paths = HDB.get("History", "TextFiles")
        for path_ in saved_paths:
            if not os.path.exists(path_):
                saved_paths.remove(path_)
        if isinstance(new_paths, str):
            if new_paths in saved_paths:
                saved_paths.remove(new_paths)
            saved_paths.append(new_paths)
        elif isinstance(new_paths, list):
            for path_ in new_paths:
                if path_ in saved_paths:
                    saved_paths.remove(path_)
                saved_paths.append(path_)
        HDB.update("History", "TextFiles", saved_paths)
    else:
        if not HDB.catExists("History"):
            HDB.insertCat("History")
        if isinstance(new_paths, str):
            HDB.insert("History", "TextFiles", [new_paths])
        elif isinstance(new_paths, list):
            HDB.insert("History", "TextFiles", new_paths)

# Update output image history

# def update_history_output_images(new_paths):
#     HDB = WASDatabase(WAS_HISTORY_DATABASE)
#     category = "Output_Images"
#     if HDB.catExists("History") and HDB.keyExists("History", category):
#         saved_paths = HDB.get("History", category)
#         for path_ in saved_paths:
#             if not os.path.exists(path_):
#                 saved_paths.remove(path_)
#         if isinstance(new_paths, str):
#             if new_paths in saved_paths:
#                 saved_paths.remove(new_paths)
#             saved_paths.append(new_paths)
#         elif isinstance(new_paths, list):
#             for path_ in new_paths:
#                 if path_ in saved_paths:
#                     saved_paths.remove(path_)
#                 saved_paths.append(path_)
#         HDB.update("History", category, saved_paths)
#     else:
#         if not HDB.catExists("History"):
#             HDB.insertCat("History")
#         if isinstance(new_paths, str):
#             HDB.insert("History", category, [new_paths])
#         elif isinstance(new_paths, list):
#             HDB.insert("History", category, new_paths)

# set INPUT_TYPES
class WAS_Text_Save:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "path": ("STRING", {"default": './ComfyUI/output/[time(%Y-%m-%d)]', "multiline": False}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "filename_delimiter": ("STRING", {"default":"_"}),
                "filename_number_padding": ("INT", {"default":4, "min":2, "max":9, "step":1}),
                "overwrite_mode": (["false", "prefix_as_filename"],),
                "ext": ("STRING", {"default":".txt"}),

            }
        }

    OUTPUT_NODE = True
    # feat(core): add feat that noted in issue 1
    # https://github.com/YMC-GitHub/ymc-node-suite-comfyui/issues/1
    RETURN_TYPES = ("STRING", "STRING","STRING")
    RETURN_NAMES = ('content','filenameWithoutExt','ext')
    FUNCTION = "save_text_file"
    CATEGORY = "Ymc Suite/IO"

    def save_text_file(self, text, path, filename_prefix='ComfyUI', filename_delimiter='_', filename_number_padding=4,overwrite_mode='false',ext='.txt'):
    
        tokens = TextTokens()
        path = tokens.parseTokens(path)
        filename_prefix = tokens.parseTokens(filename_prefix)
    
        # feat(core): add paths when it does not exits
        if not os.path.exists(path):
            cstr(f"The path `{path}` doesn't exist! Creating it...").warning.print()
            try:
                os.makedirs(path, exist_ok=True)
            except OSError as e:
                cstr(f"The path `{path}` could not be created! Is there write access?\n{e}").error.print()

        # feat(core): out info when text is empty
        if text.strip() == '':
            cstr(f"There is no text specified to save! Text is empty.").error.print()

        
        delimiter = filename_delimiter
        number_padding = int(filename_number_padding)
        # file_extension = '.txt'
        file_extension = ext

        filename ,counter= self.generate_filename_data(path, filename_prefix, delimiter, number_padding, file_extension)
        
        filenameWithoutExt = f"{filename_prefix}{delimiter}{counter:0{number_padding}}"

        # feat(core): use prefix as file name when overwrite_mode is 'prefix_as_filename'
        if overwrite_mode == 'prefix_as_filename':
            filename = f"{filename_prefix}{file_extension}"
            filenameWithoutExt = f"{filename_prefix}"
        
        fileLocation = os.path.join(path, filename)

        self.writeTextFile(fileLocation, text)

        update_history_text_files(fileLocation)
        # filenameWithoutExt,ext = os.path.splitext(filename)

        # return (text, { "ui": { "string": text } } )
        # feat(core): use the 2th result is filename without ext
        # feat(core): use the 3th result is ext
        return text, filenameWithoutExt,file_extension
        
    def generate_filename_data(self, path, prefix, delimiter, number_padding, extension):
        pattern = f"{re.escape(prefix)}{re.escape(delimiter)}(\\d{{{number_padding}}})"
        existing_counters = [
            int(re.search(pattern, filename).group(1))
            for filename in os.listdir(path)
            if re.match(pattern, filename)
        ]
        existing_counters.sort(reverse=True)

        if existing_counters:
            counter = existing_counters[0] + 1
        else:
            counter = 1

        filename = f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"
        while os.path.exists(os.path.join(path, filename)):
            counter += 1
            filename = f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"

        return filename,counter

    def writeTextFile(self, file, content):
        try:
            with open(file, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
        except OSError:
            cstr(f"Unable to save file `{file}`").error.print()

# Image Save (NSP Compatible)
# Originally From ComfyUI/nodes.py

# class WAS_Image_Save:
#     def __init__(self):
#         self.output_dir = comfy_paths.output_directory
#         self.type = 'output'
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "images": ("IMAGE", ),
#                 "output_path": ("STRING", {"default": '[time(%Y-%m-%d)]', "multiline": False}),
#                 "filename_prefix": ("STRING", {"default": "ComfyUI"}),
#                 "filename_delimiter": ("STRING", {"default":"_"}),
#                 "filename_number_padding": ("INT", {"default":4, "min":1, "max":9, "step":1}),
#                 "filename_number_start": (["false", "true"],),
#                 "extension": (['png', 'jpeg', 'gif', 'tiff', 'webp'], ),
#                 "quality": ("INT", {"default": 100, "min": 1, "max": 100, "step": 1}),
#                 "lossless_webp": (["false", "true"],),
#                 "overwrite_mode": (["false", "prefix_as_filename"],),
#                 "show_history": (["false", "true"],),
#                 "show_history_by_prefix": (["true", "false"],),
#                 "embed_workflow": (["true", "false"],),
#                 "show_previews": (["true", "false"],),
#             },
#             "hidden": {
#                 "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
#             },
#         }

#     RETURN_TYPES = ()
#     FUNCTION = "was_save_images"

#     OUTPUT_NODE = True

#     CATEGORY = "WAS Suite/IO"

#     def was_save_images(self, images, output_path='', filename_prefix="ComfyUI", filename_delimiter='_', 
#                         extension='png', quality=100, lossless_webp="false", prompt=None, extra_pnginfo=None, 
#                         overwrite_mode='false', filename_number_padding=4, filename_number_start='false',
#                         show_history='false', show_history_by_prefix="true", embed_workflow="true",
#                         show_previews="true"):
                        
#         delimiter = filename_delimiter
#         number_padding = filename_number_padding
#         lossless_webp = (lossless_webp == "true")

#         # Define token system
#         tokens = TextTokens()

#         original_output = self.output_dir
#         # Parse prefix tokens
#         filename_prefix = tokens.parseTokens(filename_prefix)

#         # Setup output path
#         if output_path in [None, '', "none", "."]:
#             output_path = self.output_dir
#         else:
#             output_path = tokens.parseTokens(output_path)
#         if not os.path.isabs(output_path):
#             output_path = os.path.join(self.output_dir, output_path)
#         base_output = os.path.basename(output_path)
#         if output_path.endswith("ComfyUI/output") or output_path.endswith("ComfyUI\output"):
#             base_output = ""

#         # Check output destination
#         if output_path.strip() != '':
#             if not os.path.isabs(output_path):
#                 output_path = os.path.join(comfy_paths.output_directory, output_path)
#             if not os.path.exists(output_path.strip()):
#                 cstr(f'The path `{output_path.strip()}` specified doesn\'t exist! Creating directory.').warning.print()
#                 os.makedirs(output_path, exist_ok=True)
        
#         # Find existing counter values
#         if filename_number_start == 'true':
#             pattern = f"(\\d{{{filename_number_padding}}}){re.escape(delimiter)}{re.escape(filename_prefix)}"
#         else:
#             pattern = f"{re.escape(filename_prefix)}{re.escape(delimiter)}(\\d{{{filename_number_padding}}})"
#         existing_counters = [
#             int(re.search(pattern, filename).group(1))
#             for filename in os.listdir(output_path)
#             if re.match(pattern, os.path.basename(filename))
#         ]
#         existing_counters.sort(reverse=True)

#         # Set initial counter value
#         if existing_counters:
#             counter = existing_counters[0] + 1
#         else:
#             counter = 1

#         # Set initial counter value
#         if existing_counters:
#             counter = existing_counters[0] + 1
#         else:
#             counter = 1

#         # Set Extension
#         file_extension = '.' + extension
#         if file_extension not in ALLOWED_EXT:
#             cstr(f"The extension `{extension}` is not valid. The valid formats are: {', '.join(sorted(ALLOWED_EXT))}").error.print()
#             file_extension = "png"

#         results = list()
#         for image in images:
#             i = 255. * image.cpu().numpy()
#             img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
#             metadata = PngInfo()
#             if embed_workflow == 'true':
#                 if prompt is not None:
#                     metadata.add_text("prompt", json.dumps(prompt))
#                 if extra_pnginfo is not None:
#                     for x in extra_pnginfo:
#                         metadata.add_text(x, json.dumps(extra_pnginfo[x]))

#             if overwrite_mode == 'prefix_as_filename':
#                 file = f"{filename_prefix}{file_extension}"
#             else:
#                 if filename_number_start == 'true':
#                     file = f"{counter:0{number_padding}}{delimiter}{filename_prefix}{file_extension}"
#                 else:
#                     file = f"{filename_prefix}{delimiter}{counter:0{number_padding}}{file_extension}"
#                 if os.path.exists(os.path.join(output_path, file)):
#                     counter += 1
#             try:
#                 output_file = os.path.abspath(os.path.join(output_path, file))
#                 if extension == 'png':
#                     img.save(output_file,
#                              pnginfo=metadata, optimize=True)
#                 elif extension == 'webp':
#                     img.save(output_file, quality=quality)
#                 elif extension == 'jpeg':
#                     img.save(output_file,
#                              quality=quality, optimize=True)
#                 elif extension == 'tiff':
#                     img.save(output_file,
#                              quality=quality, optimize=True)
#                 elif extension == 'webp':
#                     img.save(output_file, quality=quality, 
#                                 lossless=lossless_webp, exif=metadata)
                
#                 cstr(f"Image file saved to: {output_file}").msg.print()
                
#                 if show_history != 'true' and show_previews == 'true':
#                     subfolder = self.get_subfolder_path(output_file, original_output)
#                     results.append({
#                         "filename": file,
#                         "subfolder": subfolder,
#                         "type": self.type
#                     })
                
#                 # Update the output image history
#                 update_history_output_images(output_file)
            
#             except OSError as e:
#                 cstr(f'Unable to save file to: {output_file}').error.print()
#                 print(e)
#             except Exception as e:
#                 cstr('Unable to save file due to the to the following error:').error.print()
#                 print(e)
            
#             if overwrite_mode == 'false':
#                 counter += 1

#         filtered_paths = []
#         if show_history == 'true' and show_previews == 'true':
#             HDB = WASDatabase(WAS_HISTORY_DATABASE)
#             conf = getSuiteConfig()
#             if HDB.catExists("History") and HDB.keyExists("History", "Output_Images"):
#                 history_paths = HDB.get("History", "Output_Images")
#             else:
#                 history_paths = None

#             if history_paths:
            
#                 for image_path in history_paths:
#                     image_subdir = self.get_subfolder_path(image_path, self.output_dir)
#                     current_subdir = self.get_subfolder_path(output_file, self.output_dir)
#                     if not os.path.exists(image_path):
#                         continue
#                     if show_history_by_prefix == 'true' and image_subdir != current_subdir:
#                         continue
#                     if show_history_by_prefix == 'true' and not os.path.basename(image_path).startswith(filename_prefix):
#                         continue
#                     filtered_paths.append(image_path)

#                 if conf.__contains__('history_display_limit'):
#                     filtered_paths = filtered_paths[-conf['history_display_limit']:]

#                 filtered_paths.reverse()

#         if filtered_paths:
#             for image_path in filtered_paths:
#                 subfolder = self.get_subfolder_path(image_path, self.output_dir)
#                 image_data = {
#                     "filename": os.path.basename(image_path),
#                     "subfolder": subfolder,
#                     "type": self.type
#                 }
#                 results.append(image_data)

#         if show_previews == 'true':
#             return {"ui": {"images": results}}
#         else:
#             return {"ui": {"images": []}}
            

#     def get_subfolder_path(self, image_path, output_path):
#         output_parts = output_path.strip(os.sep).split(os.sep)
#         image_parts = image_path.strip(os.sep).split(os.sep)
#         common_parts = os.path.commonprefix([output_parts, image_parts])
#         subfolder_parts = image_parts[len(common_parts):]
#         subfolder_path = os.sep.join(subfolder_parts[:-1])
#         return subfolder_path

"""python-list-util"""
def list_del_exculde(start,oldlist,exclist,newlist):
  if start==len(oldlist):return newlist  #base condition
  if not(exclist[start] in oldlist):  #checking if
    newlist.append(oldlist[start])
  return list_del_exculde(start+1,oldlist,exclist,newlist)
def list_fill_one(t,n=20):
    return [t] * n
def list_2_tupe(l):
    return tuple(l)

def list_shuffle(l:list,keep_n=0):
    """
    list shuffle with keep n token

    return a new list
    """
    el=l.copy()
    index=keep_n
    if index >=1:
        el=l[index:]
    random.shuffle(el)
    if index >=1:
        el=l[0:index]+el
    return el

"""cutoff-region-util"""
# cutoff region util
class CutoffRegionUtil:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "main_text": ("STRING", {"default": "dress", "multiline": True}),
                "target_text":("STRING", {"default": "white", "multiline": False}),
                "weight": ("STRING", {"default": "1.0", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ('region_text','target_text','prompt_weight')
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/cutoff-region-util"
    OUTPUT_NODE = True

    def exec(self, main_text,target_text,weight):
        # Converted inputs are sent as the string of 'undefined' if not connected
        if target_text == "undefined":
            target_text = ""
        if main_text == "undefined":
            main_text = ""
        region_text = ""
        if weight is None or weight=='' or weight=='1.0':
            region_text = (" ").join(filter(None, [target_text, main_text]))
        else:
            # region_text = (" ").join(filter(None, ["(",target_text, main_text,":",weight,")"]))
            region_text = (" ").join(filter(None, [target_text, main_text]))
            region_text = ("").join(filter(None, ["(",region_text,":",weight,")"]))
        # return {"ui": {"text": (region_text,)}, "result": (region_text,)}
        return region_text,target_text,weight

# cutoff region util


    
TEXT_BASE_COLORS=['red','orange','yellow','green','cyan','blue','purple','black','white','pink','custom']
TEXT_BASE_COLORS_COUNT=len(TEXT_BASE_COLORS)

class CutoffRegionUtilColorTextList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "custom": ("STRING", {"default": "red", "multiline": False})
            }
        }

    # RETURN_TYPES = ("STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING",)
    RETURN_TYPES = list_2_tupe(list_fill_one('STRING',TEXT_BASE_COLORS_COUNT))
    RETURN_NAMES = list_2_tupe(TEXT_BASE_COLORS)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/cutoff-region-util"
    OUTPUT_NODE = True

    def exec(self, custom):
        # Converted inputs are sent as the string of 'undefined' if not connected
        if custom == "undefined":
            custom = "sliver"
        # return red,orange,yellow,green,cyan,blue,purple,black,white,pink,custom
        TEXT_BASE_COLORS_VALUE = TEXT_BASE_COLORS.copy()
        TEXT_BASE_COLORS_VALUE[TEXT_BASE_COLORS_COUNT-1]=custom
        return list_2_tupe(TEXT_BASE_COLORS_VALUE)

TEXT_LIST_RETURN_NAMES=['a','b','c','d','e','f','g']
TEXT_LIST_COUNT=len(TEXT_LIST_RETURN_NAMES)
class TextUtilPathList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "a": ("STRING",{"forceInput":False}),
                "b": ("STRING",{"forceInput":False}),
                "c": ("STRING",{"forceInput":False}),
                "d": ("STRING",{"forceInput":False}),
                "e": ("STRING",{"forceInput":False}),
                "f": ("STRING",{"forceInput":False}),
                "g": ("STRING",{"forceInput":False}),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('STRING',TEXT_LIST_COUNT))
    RETURN_NAMES = list_2_tupe(TEXT_LIST_RETURN_NAMES)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, a,b,c,d,e,f,g):
        return list_2_tupe([a,b,c,d,e,f,g])
    
# "text": (TEXT_TYPE, {"forceInput": (True if TEXT_TYPE == 'STRING' else False)}),
class TextUtilJoinText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "splitchar": ("STRING", {"default": "_", "multiline": False}),
                "a": ("STRING",{"forceInput":False}),
                "b": ("STRING",{"forceInput":False}),
                "c": ("STRING",{"forceInput":False}),
                "d": ("STRING",{"forceInput":False}),
                "e": ("STRING",{"forceInput":False}),
                "f": ("STRING",{"forceInput":False}),
                "g": ("STRING",{"forceInput":False}),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('STRING',1))
    RETURN_NAMES = list_2_tupe(['text'])
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, splitchar,a,b,c,d,e,f,g):
        ls=[a,b,c,d,e,f,g]
        ls = list(filter(None, ls))
        joinedtxt=splitchar.join(ls)
        return list_2_tupe([joinedtxt])


class TextUtilRandomText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "char": ("STRING", {"default": '|', "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",'INT',)
    RETURN_NAMES = list_2_tupe(['text','seed'])
    FUNCTION = "exec"

    CATEGORY = "Ymc Suite/text-util"

    def exec(self, text, seed,char='|'):
        iteml = text.split(char)
        random.seed(seed)
        choice = random.choice(iteml)
        return list_2_tupe([choice,seed])
        
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
    
class TextUtilLoopText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "char": ("STRING", {"default": '|', "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",'INT','STRING')
    RETURN_NAMES = list_2_tupe(['text','seed','index'])
    FUNCTION = "exec"

    CATEGORY = "Ymc Suite/text-util"

    def exec(self, text, seed,char='|'):
        iteml = text.split(char)
        random.seed(seed)
        # get random index in range
        # index = random.randint(0, len(iteml)-1)

        # get loop index with de/cr seed
        length=len(iteml)
        maxindex=(length-1)
        minindex=0
        index=minindex
        if seed == 0:
            index=0
        else:
            if maxindex > seed:
                index=seed
            else:
                index = seed % maxindex
        if index <=0:
            index=0
        if index >length:
            index=maxindex
        
        choice = iteml[index]
        # print(maxindex,seed,index,choice)
        return list_2_tupe([choice,seed,str(index)])
        
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
    
class TextUtilSearchText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": False}),
                "find": ("STRING", {"default": '', "multiline": False}),
                "replace": ("STRING", {"default": '', "multiline": False}),
                "action": (["yes",'no'],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = list_2_tupe(['text'])
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"

    def exec(self, text, find, replace,action='yes'):
        if 'no' in action:
            return list_2_tupe([text])
        return (self.replace_substring(text, find, replace), )

    def replace_substring(self, text, find, replace):
        import re
        text = re.sub(find, replace, text)
        return text
    
class TextUtilSwitchText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("STRING", {"default": '', "multiline": False}),
                "b": ("STRING", {"default": '', "multiline": False}),
                "boolean_number": ("NUMBER",),
            }
        }

    RETURN_TYPES = ('STRING',)
    FUNCTION = "exec"

    CATEGORY = "Ymc Suite/text-util"
    def exec(self, a='', b='', boolean_number=1):

        if int(round(boolean_number)) == 1:
            return (a, )
        else:
            return (b, )


# D:\code\python\comfyui\nodes.py
# class ImageInvert:

#     @classmethod
#     def INPUT_TYPES(s):
#         return {"required": { "image": ("IMAGE",)}}

#     RETURN_TYPES = ("IMAGE",)
#     FUNCTION = "invert"

#     CATEGORY = "image"

#     def invert(self, image):
#         s = 1.0 - image
#         return (s,)
    
"""region-util"""

def region_strify(l:list):
    tl=list(map(str,l))
    tl=list(filter(None, tl))
    return ','.join(tl)

def region_listfy(s:str):
    tl=s.split(",")
    tl=list(filter(None, tl))
    return tl

def region_intify(l:list):
    tl=list(map(int,l))
    return tl

def region_get_location_from_center_size(cx=128, cy=128, w=256, h=256):
    left=cx-w/2
    top=cy-h/2
    right=cx+w/2
    bottom=cy+h/2
    floatl=[left,top,right,bottom,cx,cy,w,h]
    intl=list(map(int,floatl))
    return intl

REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES=['left','top','right','bottom','cx','cy','w','h']
REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES_COUNT=len(REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES)
class RegionUtilGetCropLocationByCenter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "cx": ("INT", {"default":128, "max": 10000000, "min":0, "step":1}),
                "cy": ("INT", {"default":128, "max": 10000000, "min":0, "step":1}),
                "w": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
                "h": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('INT',REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES_COUNT))
    RETURN_NAMES = list_2_tupe(REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/region-util"
    OUTPUT_NODE = True

    def exec(self, cx=128, cy=128, w=256, h=256):
        intl=region_get_location_from_center_size(cx,cy,w,h)
        return list_2_tupe(intl)
    
class RegionUtilGetCropLocationFromCenterSizeText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": '128,128,256,256', "multiline": False}),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('INT',REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES_COUNT))
    RETURN_NAMES = list_2_tupe(REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/region-util"
    OUTPUT_NODE = True

    def exec(self, text='128,128,256,256'):
        tl=region_intify(region_listfy(text))
        cx,cy,w,h=tl
        intl=region_get_location_from_center_size(cx,cy,w,h)
        return list_2_tupe(intl)
    
REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES=['left','top','right','bottom','cx','cy','w','h']
REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES_COUNT=len(REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES)
class RegionUtilGetCropLocationByLT:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "left": ("INT", {"default":0, "max": 10000000, "min":0, "step":1}),
                "top": ("INT", {"default":0, "max": 10000000, "min":0, "step":1}),
                "w": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
                "h": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('INT',REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES_COUNT))
    RETURN_NAMES = list_2_tupe(REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/region-util"
    OUTPUT_NODE = True

    def exec(self, left=0, top=0, w=256, h=256):
        cx=left+w/2
        cy=top+h/2

        right=cx+w/2
        bottom=cy+h/2
        floatl=[left,top,right,bottom,cx,cy,w,h]
        intl=list(map(int,floatl))
        return list_2_tupe(intl)

REGION_LOCATION_RETURN_NAMES=['left','top','right','bottom']
class RegionUtilGetPadOutLocationBySize:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "w": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
                "h": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('INT',len(REGION_LOCATION_RETURN_NAMES)))
    RETURN_NAMES = list_2_tupe(REGION_LOCATION_RETURN_NAMES)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/region-util"
    OUTPUT_NODE = True

    def exec(self, w=256, h=256):
        c=0
        if w<h:
            c=1
        left=-1*c*(w-h)/2
        right=left

        c=0
        if w>=h:
            c=1
        top=c*(w-h)/2
        bottom=top
        floatl=[left,top,right,bottom]
        intl=list(map(int,floatl))
        return list_2_tupe(intl)


"""canvas-util"""
class CanvasUtilCalSize:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "w": ("INT", {"default":512, "max": 10000000, "min":0, "step":1}),
                "h": ("INT", {"default":512, "max": 10000000, "min":0, "step":1}),
                "lockoff": (["false", "w","h"],),
                # "rate": (["1:1", "2:3","9:16"],),
                "rate": ("STRING", {"default": "1:1", "multiline": False}),
                "reverse": (["false", "true"],),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('INT',2))
    RETURN_NAMES = list_2_tupe(['w','h'])
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/canvas-util"
    OUTPUT_NODE = True

    def exec(self,w=512, h=512,lockoff='false',rate='1:1',reverse='false'):
        rw=w
        rh=h
        # get h or w with lockoff
        if lockoff != "false":
            ratel=list(map(int,rate.split(":")))
            raten=(ratel[0]/ratel[1])
        if lockoff == "w":
            rh=int(w/raten)
        if lockoff == "h":
            rw=int(h*raten)

        floatl=[rw,rh]
        # reverse result of w h
        if reverse == "true":
            floatl=[rh,rw]
        intl=list(map(int,floatl))
        return list_2_tupe(intl)

"""hks-util"""
class HksUtilCalDenoiseStep:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "steps": ("INT", {"default":20, "max": 50, "min":0, "step":1}),
                "denoise": ("FLOAT", {"min": 0, "max": 1, "step": 0.05, "default": 0.3}),
            }
        }
    RETURN_TYPES = list_2_tupe(list_fill_one('INT',2))
    RETURN_NAMES = list_2_tupe(['steps','step_at_start'])
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/hks-util"
    OUTPUT_NODE = True

    def exec(self,steps=20, denoise=0.3):
        floatl=[steps,steps*(1-denoise)]
        intl=list(map(int,floatl))
        return list_2_tupe(intl)

# text-util
def tags_listify(s:str):
    ls = s.split(",")
    ls = list(filter(None, ls))
    return ls

def tags_strify(l:list[str]):
    return ','.join(l)

def tag_trim(s:str):
    trimedtag=s
    trimedtag=re.sub(r'^ *', '', trimedtag,0)
    trimedtag=re.sub(r' *$', '', trimedtag,0)
    return trimedtag

def tag_ms2os(s:str):
    return re.sub(re.compile(r' {1,}'), ' ', s,0)

def tag_unweight(s:str):
    # unweight,trim,
    unwdtag=s.replace("(","").replace(")","")
    unwdtag=re.sub(r':\d.*', '', unwdtag,0)
    unwdtag=tag_trim(unwdtag)
    unwdtag=tag_ms2os(unwdtag)
    return unwdtag

def tags_unweight(s:str):
    ls=tags_listify(s)
    nls=[]
    for tag in ls:
        stdedtag=tag_unweight(tag)
        if stdedtag !="":
            nls.append(stdedtag)
    return ",".join(nls)

def tags_onelineify(s:str):
    return re.sub(r'\n', ',', s,0)

def tag_std(s:str):
    # trim,ms2os
    stdedtag=s
    stdedtag=tag_trim(stdedtag)
    stdedtag=tag_ms2os(stdedtag)
    return stdedtag


def tags_dup(s:str):
    nls=tags_listify(s)
    nls=list(dict.fromkeys(nls))
    return ",".join(nls)

def tags_std(s:str):
    ls=tags_listify(s)
    nls=[]
    for tag in ls:
        stdedtag=tag_std(tag)
        if stdedtag !="":
            nls.append(stdedtag)
    return ",".join(nls)

def tags_ignore(s:str,i:str):
    ls=tags_listify(s)
    li=tags_listify(i)

    nls=[]
    for tag in ls:
        stdedtag=tag_unweight(tag)
        if stdedtag !="" and not(stdedtag in li):
            nls.append(tag)
    return ",".join(nls)

def tags_replace(s:str,i:str,r:str):
    ls=tags_listify(s)
    li=tags_listify(i)
    # lr=tags_listify(r)

    nls=[]
    for tag in ls:
        stdedtag=tag_unweight(tag)
        if stdedtag !="":
            if stdedtag in li:
                # replace found with r
                nls.append(r)
            else:
                nls.append(tag)
    return ",".join(nls)

def tags_search(s:str,i:str):
    ls=tags_listify(s)
    li=tags_listify(i)
    nls=[]
    for tag in ls:
        stdedtag=tag_unweight(tag)
        if stdedtag !="" :
            for pattern in li:
                if pattern in stdedtag:
                    nls.append(tag)
    return ",".join(nls)

def tags_head(s:str,i:str):
    """
    move some tags to head
    """
    head=tags_listify(i)
    tails=tags_listify(tags_ignore(s,i))
    return ",".join(head+tails)

def tags_tail(s:str,i:str):
    """
    move some tags to head
    """
    tails=tags_listify(i)
    head=tags_listify(tags_ignore(s,i))
    return ",".join(head+tails)


class TextUtilPromptAdd:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
                "toadd": ("STRING",{"forceInput":False}),
                "action": (["add2head",'add2tail','del|add2head','del|add2tail','none'],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text='',toadd='',action='add2head'):
        # if action =="add2head":
        #     return list_2_tupe([tags_head(text,prev)])
        # if action =="add2tail":
        #     return list_2_tupe([tags_tail(text,prev)])
        if 'none' in action:
            return list_2_tupe([text])
        prev=toadd
        if 'del' in action:
            prev=tags_ignore(text,toadd)
        if 'add2head' in action:
            prev=tags_head(text,prev)
        if 'add2tail' in action:
            prev=tags_tail(text,prev)
        return list_2_tupe([prev])
        
class TextUtilPromptAdvSearch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
                "search": ("STRING",{"forceInput":False}),
                "action": (['none',"del", "move2head",'move2tail',"replace","search"],),
                "replace": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text='',search='',action='none',replace=''):
        if action == "none":
            return list_2_tupe([text])
        
        if action == "search":
            return list_2_tupe([tags_search(text,search)])
        searchedtags=tags_search(text,search)
        if action =="replace":
            return list_2_tupe([tags_replace(text,searchedtags,replace)])
        if action =="del":
            return list_2_tupe([tags_ignore(text,searchedtags)])
        if action =="move2head":
            return list_2_tupe([tags_head(text,searchedtags)])
        if action =="move2tail":
            return list_2_tupe([tags_tail(text,searchedtags)])

        
class TextUtilPromptSearch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
                "search": ("STRING",{"forceInput":False}),            
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text='',search=''):
        return list_2_tupe([tags_search(text,search)])
    
class TextUtilPromptDup:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text):
        return list_2_tupe([tags_dup(text)])

# tags_onelineify
class TextUtilPromptAdvDup:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
                # "mode": (["alline", "in-each-line"],),
            }
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ('STRING',"STRING",)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text):
        a=''
        res=[]
        textl=text.split("\n")
        for line in textl:
            res.append(tags_dup(line))
        a='\n'.join(res)

        tags_dup(tags_onelineify(text))
        return list_2_tupe([tags_dup(tags_onelineify(a)),a])
    

class TextUtilPromptShuffle:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
                "keep_n_token": ("STRING", {"default": "0", "multiline": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text='',keep_n_token='0',seed=0):
        random.seed(seed)
        textl=tags_listify(tags_onelineify(text))
        el=list_shuffle(textl,int(keep_n_token))
        return list_2_tupe([','.join(el)])
    
class TextUtilPromptDel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "search": ("STRING",{"forceInput":False}),
                "todel": ("STRING",{"forceInput":False}),
                "action": (["yes",'no'],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, search='',todel='',action='yes'):
        # https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
        if 'no' in action:
            return list_2_tupe([search]) 
        ca=tags_ignore(search,tags_unweight(todel))
        return list_2_tupe([ca])
    
class TextUtilPromptStd:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text):
        return list_2_tupe([tags_std(text)])
    
class TextUtilPromptUnweight:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, text):
        return list_2_tupe([tags_unweight(text)])
    
class TextUtilPromptJoin:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "a": ("STRING",{"forceInput":False}),
                "b": ("STRING",{"forceInput":False}),
                "c": ("STRING",{"forceInput":False}),
                "d": ("STRING",{"forceInput":False}),
                "e": ("STRING",{"forceInput":False}),
                "f": ("STRING",{"forceInput":False}),
                "g": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/text-util"
    OUTPUT_NODE = True

    def exec(self, a,b,c,d,e,f,g):
        vl=[a,b,c,d,e,f,g]
        vs = (",").join(vl)
        vs=tags_std(vs)
        # vs = vs.replace("  ", " ").replace(" ,", ",").replace(", ", ",").replace(",,", ",").replace(",,", ",")
        return {"ui": {"text": (vs,)}, "result": (vs,)}

# class TextUtilTextShow:
#     @classmethod
#     def INPUT_TYPES(s):
#         return {"required": {
#             "text": ("STRING", {"forceInput": True}),
#         }}

#     # INPUT_IS_LIST = True
#     RETURN_TYPES = ("STRING",)
#     FUNCTION = "notify"
#     OUTPUT_NODE = True
#     # OUTPUT_IS_LIST = (True,)

#     CATEGORY = "Ymc Suite/text-util"

#     def notify(self, text):
#         return {"ui": {"text": text}, "result": (text,)}

class NumberUtilRandomNum:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_type": (["integer", "float", "bool"],),
                "minimum": ("FLOAT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),
                "maximum": ("FLOAT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("NUMBER", "FLOAT", "INT")
    FUNCTION = "exec"

    CATEGORY = "WAS Suite/Number"

    def exec(self, minimum, maximum, seed, number_type='integer'):

        # Set Generator Seed
        random.seed(seed)

        # Return random number
        if number_type:
            if number_type == 'integer':
                number = random.randint(minimum, maximum)
            elif number_type == 'float':
                number = random.uniform(minimum, maximum)
            elif number_type == 'bool':
                number = random.random()
            else:
                return

        # Return number
        return (number, float(number), int(number))
        
    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()
    
def io_file_list(dir='',pattern='*.txt'):
    res=[]
    for filename in glob.glob(os.path.join(dir,pattern)):
        res.append(filename)
    return res
def io_file_get_txt(loc):
    res=''
    with open(loc) as f:
        res = f.read()
        f.close()
    return res

class IoUtilFileListGet:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "", "multiline": False}),
                "pattern": ("STRING", {"default": "*.txt", "multiline": False}),
                # "mode": ("STRING", {"default": "filename", "multiline": False}),
                "mode": (["filename", "abspath"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/IO"
    OUTPUT_NODE = True

    def exec(self, path='',pattern='*.txt',mode='filename'):
        text=io_file_list(path,pattern)
        if mode=='filename':
            text=list(map(os.path.basename,text))
        text='\n'.join(text)
        return list_2_tupe([text])
    
class IoUtilFileListGetText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "", "multiline": False}),
                "pattern": ("STRING", {"default": "*.txt", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/IO"
    OUTPUT_NODE = True

    def exec(self, path='',pattern='*.txt'):
        plist=io_file_list(path,pattern)
        text=[]
        for loc in plist:
            text.append(io_file_get_txt(loc))
        # to multi line
        text='\n'.join(text)
        return list_2_tupe([text])


"""pipe-util"""
class PipeUtilToBasicPipe:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                     "model": ("MODEL",),
                     "clip": ("CLIP",),
                     "vae": ("VAE",),
                     "positive": ("CONDITIONING",),
                     "negative": ("CONDITIONING",),
                     },
                }

    RETURN_TYPES = ("BASIC_PIPE", "MODEL", "CLIP", "VAE", "CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("basic_pipe", "model", "clip", "vae", "positive", "negative")
    FUNCTION = "doit"

    CATEGORY = "Ymc Suite/pipe-util"

    def doit(self, model, clip, vae, positive, negative):
        basic_pipe = (model, clip, vae, positive, negative)
        return basic_pipe,model, clip, vae, positive, negative

"""img-util"""
class ImgUtilGetImageSize:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_size"
    CATEGORY = "Ymc Suite/img-util"

    def get_size(self, image):
        _, height, width, _ = image.shape
        return (width, height)

class ImgUtilSwitchInputImage:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_a": ("IMAGE",),
                "image_b": ("IMAGE",),
                "boolean_number": ("NUMBER",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_input_switch"
    CATEGORY = "Ymc Suite/img-util"

    def image_input_switch(self, image_a, image_b, boolean_number=1):

        if int(round(boolean_number)) == 1:
            return (image_a, )
        else:
            return (image_b, )

"""conditioning-util"""
class ConditioningUtilInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning_a": ("CONDITIONING",),
                "conditioning_b": ("CONDITIONING",),
                "boolean_number": ("NUMBER",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "conditioning_input_switch"

    CATEGORY = "Ymc Suite/conditioning-util"

    def conditioning_input_switch(self, conditioning_a, conditioning_b, boolean_number=1):

        if int(round(boolean_number)) == 1:
            return (conditioning_a, )
        else:
            return (conditioning_b, ) 

"""xyz-util"""             
re_int = re.compile(r"\s*([+-]?\s*\d+)\s*")
re_range = re.compile(r"\s*([+-]?\s*\d+)\s*-\s*([+-]?\s*\d+)(?:\s*\(([+-]\d+)\s*\))?\s*")
re_range2 = re.compile(r"\s*([+-]?\s*\d+)\s*-\s*([+-]?\s*\d+)(?:\s*\[([+-]\d+)\s*\])?\s*")

re_float = re.compile(r"\s*([+-]?\s*\d+(?:.\d*)?)\s*")
re_range_float = re.compile(r"\s*([+-]?\s*\d+(?:.\d*)?)\s*-\s*([+-]?\s*\d+(?:.\d*)?)(?:\s*\(([+-]\d+(?:.\d*)?)\s*\))?\s*")
re_range_float2 = re.compile(r"\s*([+-]?\s*\d+(?:.\d*)?)\s*-\s*([+-]?\s*\d+(?:.\d*)?)(?:\s*\[([+-]\d+)\s*\])?\s*")

def xyz_generate_floats(batch_count, first_float, last_float):
    if batch_count > 1:
        interval = (last_float - first_float) / (batch_count - 1)
        return [round(first_float + i * interval, 3) for i in range(batch_count)]
    else:
        return [first_float] if batch_count == 1 else []

def xyz_generate_ints(batch_count, first_int, last_int):
    if batch_count > 1:
        interval = (last_int - first_int) / (batch_count - 1)
        values = [int(first_int + i * interval) for i in range(batch_count)]
    else:
        values = [first_int] if batch_count == 1 else []
    values = list(set(values))  # Remove duplicates
    values.sort()  # Sort in ascending order
    return values

def xyz_gen_frange(start, end, step):
    x = float(start)
    end = float(end+0.1)
    step = float(step)
    while x < end:
        yield x
        x += step

def xyz_parse_int(input: str):
    m = re_int.fullmatch(input)
    if m is not None:
        return int(m.group(1))
    
    m = re_range.fullmatch(input)
    if m is not None:
        start, end, step = m.group(1), m.group(2), m.group(3)
        if step is None:
            step = 1
        return list(range(int(start), int(end) + 1, int(step)))

    m = re_range2.fullmatch(input)
    if m is not None:
        start, end, count = m.group(1), m.group(2), m.group(3)
        if count is None:
            count = 1
        return xyz_generate_ints(int(count),int(start),int(end))
    if m is None:
        raise ValueError(f'failed to process: {input}')
    
def xyz_parse_float(input: str):
    m = re_float.fullmatch(input)
    if m is not None:
        return float(m.group(1))
        
    m = re_range_float.fullmatch(input)
    if m is not None:
        start, end, step = m.group(1), m.group(2), m.group(3)
        if step is None:
            step = 1.0
        return list(xyz_gen_frange(float(start), float(end), float(step)))
    
    m = re_range_float2.fullmatch(input)
    if m is not None:
        start, end, count = m.group(1), m.group(2), m.group(3)
        if count is None:
            count = 1
        return xyz_generate_floats(int(count),float(start),float(end))
    
    if m is None:
        raise ValueError(f'failed to process: {input}')


def xyz_parse(input: str, cont: Union[Callable[[str],Any],None]):
    vs = [ x.strip() for x in input.split(',') ]
    if cont is not None:
        new_vs = []
        for v in vs:
            new_v = cont(v)
            if isinstance(new_v, list):
               new_vs += new_v
            else:
                new_vs.append(new_v)
        vs = new_vs
    return vs    

def xyz_float2str(v,):
    return '{:.2f}'.format(v)

def xyz_get_n_float(s,n=0):
   fstr=str(s)
   a,b,c=fstr.partition('.')
   if n==0:
       return ''.join([a])
   c=(c+"0"*n)[:n]
   return ".".join([a,c])

class XyzUtilKVTxtToOther:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "v": ("STRING", {"default": "", "multiline": False}),
                # "name": ("STRING", {"default": "steps", "multiline": False}),
                "k": ("STRING", {"default": "Steps", "multiline": False}),
                "namepreset": (["none","no-shortname","empty-shortname","Steps", "CFG Scale","Denoise"],),
                "shortname": ("STRING", {"default": "", "multiline": False}),
                # "keepndecimal": ("STRING", {"default": "0", "multiline": False}),
                "keepndecimal": ("INT", {"default": 1, "min": 0, "max": 8}),
            }
        }

    # RETURN_TYPES = ("INT","INT","INT","STRING","XY")
    # RETURN_NAMES = ('s','e','count','gridAnnotion','X or Y')
    RETURN_TYPES = ("INT","STRING","XY")
    RETURN_NAMES = ('count','row of col text','X or Y')
    FUNCTION = "exec"
    CATEGORY = "Ymc Suite/xyz-util"
    OUTPUT_NODE = True

    def exec(self, v='',k='Steps',namepreset='none',shortname='',keepndecimal=1):
        intkl=['Steps','Clip Skip','custom']
        floatkl=['CFG Scale','Denoise',"custom-float"]
        # use name preset
        name=namepreset if not (namepreset in ['none','no-shortname',"empty-shortname"]) else k
        # name="Steps" if name=='' else name


        txtl=[]
        il=[]
        tl=[]
        if name in intkl:
            tl=xyz_parse(v,xyz_parse_int)
            txtl=list(map(str,tl)) 
            il=list(map(int,tl))
            
        if name in floatkl:
            tl=xyz_parse(v,xyz_parse_float)
            txtl=list(map(str,tl)) 
            # 
            # if keepndecimal!='':
            #     dc=int(keepndecimal)

            if keepndecimal>0:
                for index,value in enumerate(txtl):
                    txtl[index]=xyz_get_n_float(value,keepndecimal)
            il=list(map(float,txtl))

            print(tl)
            print(il)
            print(txtl)

        # gen x or y key for image grid
        kname=name
        if shortname !="" and not(namepreset in ['none','no-shortname','empty-shortname']):
            kname=shortname
        if (namepreset in ["empty-shortname"]):
             kname=""
        if kname !="":
            kname=kname+':'
        rowOfColTxt=''+kname+';'.join(txtl)
        # s=il[0]
        # e=il[-1]
        count=len(il)

        dset=(name, il)
        # return list_2_tupe([s,e,count,gridAnnotion,dset])
        return list_2_tupe([count,rowOfColTxt,dset])
    
# class XyzUtilTxtToFloat:
#     @classmethod
#     def INPUT_TYPES(s):
#         return {
#             "required": {
#                 "text": ("STRING", {"default": "", "multiline": False}),
#                 "name": ("STRING", {"default": "steps", "multiline": False}),
#             }
#         }

#     RETURN_TYPES = ("FLOAT","FLOAT","FLOAT","STRING","DICT")
#     RETURN_NAMES = ('s','e','count','gridAnnotion','DICT')
#     FUNCTION = "exec"
#     CATEGORY = "Ymc Suite/xyz-util"
#     OUTPUT_NODE = True

#     def exec(self, text='',name='steps'):
#         tl=xyz_parse(text,xyz_parse_float)
#         il=list(map(float,tl.copy()))
#         # tl=list(map(str,tl))
#         gridAnnotion=name+':'+';'.join(tl)
#         s=il[0]
#         e=il[-1]
#         count=len(il)
#         dset=(name, il)
#         return list_2_tupe([s,e,count,gridAnnotion,dset])
    
# feat(core): rename 'Save Text File' to io-text-save for issue 3
    # https://github.com/YMC-GitHub/ymc-node-suite-comfyui/issues/3

# NODE MAPPING
NODE_CLASS_MAPPINGS = {
    "io-text-save": WAS_Text_Save,
    # "io-image-save": WAS_Image_Save,
    "cutoff-region-util": CutoffRegionUtil,
    "pipe-util-to-basic-pipe": PipeUtilToBasicPipe,
    "canvas-util-cal-size": CanvasUtilCalSize,
    # "img-util-get-image-size": ImgUtilGetImageSize,
    # "img-util-switch-input-image": ImgUtilSwitchInputImage,
    # "conditioning-util-input-switch": ConditioningUtilInputSwitch,
    "hks-util-cal-denoise-step": HksUtilCalDenoiseStep,
    "io-util-file-list-get": IoUtilFileListGet,
    "io-util-file-list-get-text": IoUtilFileListGetText,
    "text-preset-colors": CutoffRegionUtilColorTextList,
    "text-util-prompt-join": TextUtilPromptJoin,    
    "text-util-prompt-del":TextUtilPromptDel,
    "text-util-prompt-std":TextUtilPromptStd,
    "text-util-prompt-unweight":TextUtilPromptUnweight, 
    "text-util-prompt-dup":TextUtilPromptDup, 
    "text-util-prompt-adv-dup":TextUtilPromptAdvDup, 
    "text-util-prompt-shuffle":TextUtilPromptShuffle,
    "text-util-prompt-search":TextUtilPromptSearch,
    "text-util-prompt-adv-search":TextUtilPromptAdvSearch,
    "text-util-prompt-add-prompt":TextUtilPromptAdd,
    "text-util-path-list": TextUtilPathList,
    "text-util-join-text": TextUtilJoinText,
    "text-util-search-text": TextUtilSearchText,
    "text-util-random-text": TextUtilRandomText,
    "text-util-loop-text": TextUtilLoopText,
    "text-util-switch-text":TextUtilSwitchText,
    # "text-util-show-text": TextUtilTextShow,
    "xyz-util-txt-to-int": XyzUtilKVTxtToOther,
    "number-util-random-num": NumberUtilRandomNum,
    "region-util-get-pad-out-location-by-size": RegionUtilGetPadOutLocationBySize,
    "region-util-get-crop-location-from-center-size-text": RegionUtilGetCropLocationFromCenterSizeText,
    "region-util-get-by-center-and-size": RegionUtilGetCropLocationByCenter,
    "region-util-get-by-lt": RegionUtilGetCropLocationByLT
}    
NODE_DISPLAY_NAME_MAPPINGS = {
    "io-text-save": 'save text file',
    # "io-image-save": WAS_Image_Save,
    "pipe-util-to-basic-pipe": 'to basic pipe',
    "canvas-util-cal-size": 'cal size',
    # "img-util-get-image-size": 'get image size',
    # "img-util-switch-input-image": 'switch input img',
    # "conditioning-util-input-switch": 'switch input conditioning',
    "hks-util-cal-denoise-step": 'cal denoise step',
    "cutoff-region-util": 'gen region text',
    "io-util-file-list-get-text": 'get multi line text of file list',
    "io-util-file-list-get": 'get file list',
    "text-preset-colors": 'base colors',
    "text-util-prompt-join": 'join prompt',
    "text-util-prompt-del": 'del prompt',
    "text-util-prompt-std": 'std prompt',
    "text-util-prompt-unweight": 'unweight prompt',
    "text-util-prompt-dup": 'dup prompt', 
    "text-util-prompt-adv-dup":'dup prompt (adv)', 
    "text-util-prompt-shuffle":'shuffle prompt',
    "text-util-prompt-search":'search propmt',
    "text-util-prompt-adv-search":'search prompt (adv)',
    "text-util-prompt-add-prompt":'add prompt',
    "text-util-path-list": 'path preset list',
    "text-util-join-text": 'join text',
    "text-util-search-text": 'search text and replace',
    "text-util-random-text": 'get random text',
    "text-util-loop-text": 'get random or loop text',
    "text-util-switch-text":'switch text',
    # "text-util-show-text": 'show text',
    "xyz-util-txt-to-int": 'txt to int',
    "number-util-random-num": 'random number',
    "region-util-get-pad-out-location-by-size": 'get pad out location by size',
    "region-util-get-crop-location-from-center-size-text": 'get region by center and size (from text)',
    "region-util-get-by-center-and-size": 'get region by center and size',
    "region-util-get-by-lt": 'get region by left top'
}
