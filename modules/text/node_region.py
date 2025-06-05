
from yors_pano_list_util import ListDelExclude,ListFillOne,ListToTupe,ListShuffle
# CURRENT_CATEGORY="Ymc Suite/region-util"
CURRENT_CATEGORY="ymc suite/text"
CURRENT_FUNCTION="exec"

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

def region_burn_corp_location_as_square(w=256, h=256):
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
    return ListToTupe(intl)
    
def region_burn_corp_location_from_lt_and_size(left=0, top=0, w=256, h=256):
    cx=left+w/2
    cy=top+h/2

    right=cx+w/2
    bottom=cy+h/2
    floatl=[left,top,right,bottom,cx,cy,w,h]
    intl=list(map(int,floatl))
    return ListToTupe(intl)
    

REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES=['left','top','right','bottom','cx','cy','w','h']
REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES_COUNT=len(REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES)
# feat(core): NodeRegionCropLocationBurnNumz - num - burn crop location (center & size)
class NodeRegionCropLocationBurnNumz:
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
    RETURN_TYPES = ListToTupe(ListFillOne('INT',REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES_COUNT))
    RETURN_NAMES = ListToTupe(REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "num - burn crop location (center & size)"
    OUTPUT_NODE = True

    def exec(self, cx=128, cy=128, w=256, h=256):
        intl=region_get_location_from_center_size(cx,cy,w,h)
        return ListToTupe(intl)
    
# feat(core): NodeRegionCropLocationBurnTxtz - txt - burn crop location (center & size)
class NodeRegionCropLocationBurnTxtz:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "cxcy": ("STRING", {"default": '128,128', "multiline": False}),
                "size": ("STRING", {"default": '256,256', "multiline": False}),
            }
        }
    RETURN_TYPES = ListToTupe(ListFillOne('INT',REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES_COUNT))
    RETURN_NAMES = ListToTupe(REGION_GET_CROP_LOCATION_BY_CENTER_RETURN_NAMES)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "txt - burn crop location (cxcy & size)"
    OUTPUT_NODE = True

    def exec(self, cxcy='128,128',size='256,256'):
        cx,cy=region_intify(region_listfy(cxcy))
        w,h=region_intify(region_listfy(size))
        intl=region_get_location_from_center_size(cx,cy,w,h)
        return ListToTupe(intl)
    
REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES=['left','top','right','bottom','cx','cy','w','h']
REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES_COUNT=len(REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES)
# feat(core): NodeRegionCropLocationBurnLtwh - int - burn crop location (lt & size)
class NodeRegionCropLocationBurnLtwh:
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
    RETURN_TYPES = ListToTupe(ListFillOne('INT',REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES_COUNT))
    RETURN_NAMES = ListToTupe(REGION_GET_CROP_LOCATION_BY_LT_RETURN_NAMES)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "int - burn crop location (lt & size)"

    OUTPUT_NODE = True

    def exec(self, left=0, top=0, w=256, h=256):
        return region_burn_corp_location_from_lt_and_size(left,top,w,h)

REGION_LOCATION_RETURN_NAMES=['left','top','right','bottom']
# feat(core): NodeRegionPaddingSquareLocationBurn - int - burn padding location as square (size)
class NodeRegionPaddingSquareLocationBurn:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "w": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
                "h": ("INT", {"default":256, "max": 10000000, "min":0, "step":1}),
            }
        }
    RETURN_TYPES = ListToTupe(ListFillOne('INT',len(REGION_LOCATION_RETURN_NAMES)))
    RETURN_NAMES = ListToTupe(REGION_LOCATION_RETURN_NAMES)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "int - burn padding location as square (size)"
    OUTPUT_NODE = True

    def exec(self, w=256, h=256):
        return region_burn_corp_location_as_square(w,h)
