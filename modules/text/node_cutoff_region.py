# import random
from yors_pano_list_util import ListDelExclude,ListFillOne,ListToTupe,ListShuffle

# from .conf import CURRENT_CATEGORY,CURRENT_FUNCTION

CURRENT_CATEGORY="ymc suite/text"
CURRENT_FUNCTION="exec"

def StrSetUndefinedAsEmpty(text,deft:str=""):
    """
    target_text=StrSetUndefinedAsEmpty(target_text)

    when text is "undefined", return ""
    """
    if text == "undefined":
        return deft
    return text

# code(core): about shift + tap and  tap in vscode

def CutoffRegionTextBurn(main_text, target_text, weight):
    """
    CutoffRegionTextBurn(main_text,target_text,weight)

    burn region text
    """
    # Converted inputs are sent as the string of 'undefined' if not connected
    target_text = StrSetUndefinedAsEmpty(target_text)
    main_text = StrSetUndefinedAsEmpty(main_text)

    region_text = ""
    if weight is None or weight == "" or weight == "1.0":
        region_text = (" ").join(filter(None, [target_text, main_text]))
    else:
        # region_text = (" ").join(filter(None, ["(",target_text, main_text,":",weight,")"]))
        region_text = (" ").join(filter(None, [target_text, main_text]))
        region_text = ("").join(filter(None, ["(", region_text, ":", weight, ")"]))
    # return {"ui": {"text": (region_text,)}, "result": (region_text,)}
    return region_text, target_text, weight


# feat(core): NodeCutoffRegionTextBurn - cutoff - region text burn
class NodeCutoffRegionTextBurn:
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
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "cutoff - region text burn"

    OUTPUT_NODE = True

    def exec(self, main_text,target_text,weight):
        return CutoffRegionTextBurn(main_text,target_text,weight)


TEXT_BASE_COLORS=['red','orange','yellow','green','cyan','blue','purple','black','white','pink','custom']
TEXT_BASE_COLORS_COUNT=len(TEXT_BASE_COLORS)


def CutoffColorTextPreset(custom:str="sliver"):
    """
    CutoffColorTextList(custom)

    color text preset will update the last one will custom
    """
    # return red,orange,yellow,green,cyan,blue,purple,black,white,pink,custom
    TEXT_BASE_COLORS_VALUE = TEXT_BASE_COLORS.copy()
    TEXT_BASE_COLORS_VALUE[TEXT_BASE_COLORS_COUNT-1]=custom
    return ListToTupe(TEXT_BASE_COLORS_VALUE)

# feat(core): NodeCutoffRegionColorTextPreset - cutoff - color preset of region text
class NodeCutoffRegionColorTextPreset:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "custom": ("STRING", {"default": "red", "multiline": False})
            }
        }

    # RETURN_TYPES = ("STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING",)
    RETURN_TYPES = ListToTupe(ListFillOne('STRING',TEXT_BASE_COLORS_COUNT))
    RETURN_NAMES = ListToTupe(TEXT_BASE_COLORS)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "cutoff - color preset of region text"    
    OUTPUT_NODE = True
    def exec(self, custom):
        # Converted inputs are sent as the string of 'undefined' if not connected
        custom=StrSetUndefinedAsEmpty(custom,"sliver")
        return CutoffColorTextPreset(custom)