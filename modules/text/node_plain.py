import random
from yors_pano_list_util import ListDelExclude,ListFillOne,ListToTupe,ListShuffle

from .conf import CURRENT_CATEGORY,CURRENT_FUNCTION

def TextListRandom(text:str, seed,char='|'):
    """
    item,seed = TextListRandom(text,seed,'|')

    TextListRandom(text,seed,',')
    """
    iteml = text.split(char)
    random.seed(seed)
    choice = random.choice(iteml)
    return ListToTupe([choice,seed])


def range_safe(i:int,s:int,e:int):
    '''
    ensure i is in [s,e]
    '''
    res=i
    if res <s:
        res=s
    if res >e:
        res=e
    return res

def range_safe_loop(i:int,s:int,e:int):
    '''
    ensure i is in [s,e] for loop
    '''
    res=i
    if res <s:
        res=s
    if res >=e:
        res = res % e
        res = s + res
    return res

def TextListLoop(text, seed,char='|'):
    iteml = text.split(char)
    # get loop index with de/cr seed
    length=len(iteml)
    index=range_safe_loop(seed-1,0,length)
    choice = iteml[index]
    # print(maxindex,seed,index,choice)
    return ListToTupe([choice,seed,str(index+1),length])



def TextReplace(text, find, replace):
    """
    text replace find with re.sub
    """
    import re
    result = re.sub(find, replace, text)
    return result



TEXT_LIST_RETURN_NAMES=['a','b','c','d','e','f','g']
TEXT_LIST_COUNT=len(TEXT_LIST_RETURN_NAMES)
TEXT_LIST_ADV_RETURN_NAMES=TEXT_LIST_RETURN_NAMES.copy()
TEXT_LIST_ADV_RETURN_NAMES.insert(0,"prefix")
# feat(core): NodePlainTextList - input text preset
class NodePlainTextList:
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
    RETURN_TYPES = ListToTupe(ListFillOne('STRING',TEXT_LIST_COUNT))
    RETURN_NAMES = ListToTupe(TEXT_LIST_RETURN_NAMES)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - input text preset"
    OUTPUT_NODE = True

    def exec(self, a,b,c,d,e,f,g):
        return ListToTupe([a,b,c,d,e,f,g])
    
# feat(core): NodePlainTextListAdv - input text preset - adv
class NodePlainTextListAdv:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
               "prefix": ("STRING",{"forceInput":False}),
                "a": ("STRING",{"forceInput":False}),
                "b": ("STRING",{"forceInput":False}),
                "c": ("STRING",{"forceInput":False}),
                "d": ("STRING",{"forceInput":False}),
                "e": ("STRING",{"forceInput":False}),
                "f": ("STRING",{"forceInput":False}),
                "g": ("STRING",{"forceInput":False}),
            }
        }
    RETURN_TYPES = ListToTupe(ListFillOne('STRING',TEXT_LIST_COUNT+1))
    RETURN_NAMES = ListToTupe(TEXT_LIST_ADV_RETURN_NAMES)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - input text preset - adv"
    OUTPUT_NODE = True

    def exec(self,prefix, a,b,c,d,e,f,g):
        joined = list(map(lambda x: prefix+x,[a,b,c,d,e,f,g]))
        import datetime
        # import time
        joined.insert(0,prefix)
        joined = list(map(lambda x: datetime.datetime.now().strftime(x),joined)) # replace time exp like %Y %M %D
        return ListToTupe(joined)  

# feat(core): NodePlainTextListJoinTextAdv - join text to text preset - adv
class NodePlainTextListJoinTextAdv:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
     
            },
            "optional": {
                "text": ("STRING",{"forceInput": True}),
                "a": ("STRING",{"forceInput":True}),
                "b": ("STRING",{"forceInput":True}),
                "c": ("STRING",{"forceInput":True}),
                "d": ("STRING",{"forceInput":True}),
                "e": ("STRING",{"forceInput":True}),
                "f": ("STRING",{"forceInput":True}),
                "g": ("STRING",{"forceInput":True}),
                "action": (["none","text-as-head","text-as-tail"],),
            }
        }
    RETURN_TYPES = ListToTupe(ListFillOne('STRING',TEXT_LIST_COUNT+1))
    RETURN_NAMES = ListToTupe(['text','a','b','c','d','e','f','g'])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - join text to text preset - adv"
    OUTPUT_NODE = True

    def exec(self,text, a,b,c,d,e,f,g,action="none"):
        joined=[]
        if "none" in action:
          joined = [a,b,c,d,e,f,g]
        elif "text-as-head" in action:
          joined = list(map(lambda x: text+x,[a,b,c,d,e,f,g]))
        elif "text-as-tail" in action:
          joined = list(map(lambda x: x+text,[a,b,c,d,e,f,g]))
        import datetime
        # import time
        joined.insert(0,text)
        joined = list(map(lambda x: datetime.datetime.now().strftime(x),joined)) # replace time exp like %Y %M %D
        return ListToTupe(joined)      

# feat(core): NodePlainTextJoin - join text
class NodePlainTextJoin:
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
    RETURN_TYPES = ListToTupe(ListFillOne('STRING',1))
    RETURN_NAMES = ListToTupe(['text'])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - join text"


    OUTPUT_NODE = True

    def exec(self, splitchar,a,b,c,d,e,f,g):
        # args to list
        ls=[a,b,c,d,e,f,g]
        # ignore none
        ls = list(filter(None, ls))
        # join with splitChar
        joinedtxt=splitchar.join(ls)
        return ListToTupe([joinedtxt])

# feat(core): NodePlainTextRandom - random text in list
class NodePlainTextRandom:
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
    RETURN_NAMES = ListToTupe(['text','seed'])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - random text in list"
    def exec(self, text, seed,char='|'):
        return TextListRandom(text,seed,char)
        
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")  
    
# feat(core): NodePlainTextLoop - get text in list (loop)
class NodePlainTextLoop:
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

    RETURN_TYPES = ("STRING",'INT','STRING','INT')
    RETURN_NAMES = ListToTupe(['text','seed','index','count'])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - get text in list (loop)"

    def exec(self, text, seed,char='|'):
        return TextListLoop(text, seed,char)
        
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

# feat(core): NodePlainTextReplace - replace text
class NodePlainTextReplace:
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
    RETURN_NAMES = ListToTupe(['text'])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - replace"


    def exec(self, text, find, replace,action='yes'):
        # feat(core): do nothing when action no
        if 'no' in action:
            return ListToTupe([text])
        # feat(core): replace text
        return ListToTupe([TextReplace(text, find, replace)])
    

def NumStrToNumInt(str:str="1",roundit:bool=True):
    """
    NumStrToNumInt(0.5)
    NumStrToNumInt(float(str))
    """
    if roundit == True:
        return int(round(str))
    return int(str)
    
def NumStrIsRoundToA(a='1', isRoundTo='1'):
    """
    NumStrIsRoundToA("0.8","1")
    NumStrIsRoundToA("0.4","1")
    """
    if NumStrToNumInt(a) == NumStrToNumInt(isRoundTo):
        return True
    else:
        return False
        
    
def BoolStr2BoolNum(str:str="true"):
    """
    BoolStr2BoolNum("TRUE")
    BoolStr2BoolNum("false")
    """
    # true,TRUE
    if str=="true":
        return 1
    else:
        return 0
    
# feat(core): NodeNumStrToNum - text to number
class NodeNumStrToNum:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": False}),
            }
        }

    # RETURN_TYPES = ('NUMBER',)
    RETURN_TYPES = ("NUMBER", "FLOAT", "INT")
    RETURN_NAMES = ListToTupe(["number", "float", "roundInt"])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - to number"
    
    def exec(self, text=''):
        strInt = int(text)
        strFlo = float(text)
        strRoundInt = int(round(strFlo))
        return ListToTupe([strInt,strFlo,strRoundInt])

# feat(core): NodeNumStrToBool - text to bool
class NodeNumStrToBool:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '1', "multiline": False}),
                "isRoundTo":("STRING", {"default": '1', "multiline": False}),
            }
        }

    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ListToTupe(["boolean"])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - is round to x"

    def exec(self, a='1', isRoundTo='1'):
        return ListToTupe([NumStrIsRoundToA(a,isRoundTo)])

# feat(core): NodePlainTextSwitchWithBool - text switch with bool
class NodePlainTextSwitchWithBool:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("STRING", {"default": '', "multiline": False}),
                "b": ("STRING", {"default": '', "multiline": False}),
                "boolean": ("BOOL",),
            }
        }

    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ListToTupe(["text"])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - switch a and b"

    def exec(self, a='', b='', boolean:bool=True):
        if boolean==True:
            return (a, )
        else:
            return (b, )
        
# feat(core): NodePlainTextSwitchWithText - text switch with text
class NodePlainTextSwitchWithText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("STRING", {"default": '', "multiline": False}),
                "b": ("STRING", {"default": '', "multiline": False}),
                "text": ("STRING", {"default": '1', "multiline": False}),
                "isRoundTo":("STRING", {"default": '1', "multiline": False}),
            }
        }

    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ListToTupe(["text"])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - switch a and b (isRoundTo)"
    def exec(self, a='', b='', text='1',isRoundTo='1'):
        if NumStrIsRoundToA(text,isRoundTo):
            return (a, )
        else:
            return (b, )
        
# class NodeTextShow:
#     @classmethod
#     def INPUT_TYPES(s):
#         return {"required": {
#             "text": ("STRING", {"forceInput": True}),
#         }}

#     # INPUT_IS_LIST = True
#     FUNCTION = CURRENT_FUNCTION
#     CATEGORY = CURRENT_CATEGORY
#     NODE_DESC = "plain - show text"
#     OUTPUT_NODE = True
#     RETURN_TYPES = ('STRING',)
#     # OUTPUT_IS_LIST = (True,)

#     def exec(self, text):
#         return {"ui": {"text": text}, "result": (text,)}
# refer: pythongosssss /ComfyUI-Custom-Scripts/py/show_text.py

# feat(core): NodeTextShow - show text
class NodeTextShow:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - show text"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)
    def exec(self, text, unique_id = None, extra_pnginfo=None):
        if unique_id and extra_pnginfo and "workflow" in extra_pnginfo[0]:
            workflow = extra_pnginfo[0]["workflow"]
            node = next((x for x in workflow["nodes"] if str(x["id"]) == unique_id[0]), None)
            if node:
                node["widgets_values"] = [text]
        return {"ui": {"text": text}, "result": (text,)}
    
# feat(core): NodeTextCalcSize - cacluate width and height
class NodeTextCalcSize:
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
    RETURN_TYPES = ListToTupe(ListFillOne('INT',2))
    RETURN_NAMES = ListToTupe(['w','h'])
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "plain - cacluate width and height"
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
        return ListToTupe(intl)