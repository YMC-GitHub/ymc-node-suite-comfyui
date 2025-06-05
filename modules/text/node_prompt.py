import re
import random

from yors_pano_list_util import ListDelExclude,ListFillOne,ListToTupe,ListShuffle

# use current_category and current_function from con.py in current directory
# from .conf import CURRENT_CATEGORY,CURRENT_FUNCTION

# feat(core): use ymc suite/text as category
CURRENT_CATEGORY="ymc suite/text"
CURRENT_FUNCTION="exec"

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


# feat(core): NodePromptAdd - prompt add some text
class NodePromptAdd:
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
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - add"

    OUTPUT_NODE = True
    def exec(self, text='',toadd='',action='add2head'):
        # if action =="add2head":
        #     return list_2_tupe([tags_head(text,prev)])
        # if action =="add2tail":
        #     return list_2_tupe([tags_tail(text,prev)])
        if 'none' in action:
            return ListToTupe([text])
        prev=toadd
        if 'del' in action:
            prev=tags_ignore(text,toadd)
        if 'add2head' in action:
            prev=tags_head(text,prev)
        if 'add2tail' in action:
            prev=tags_tail(text,prev)
        return ListToTupe([prev])
        
# feat(core): NodePromptAdvAdd - prompt add some text (adv)
class NodePromptAdvSearch:
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


    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - search (adv)"

    OUTPUT_NODE = True
    def exec(self, text='',search='',action='none',replace=''):
        if action == "none":
            return ListToTupe([text])
        
        if action == "search":
            return ListToTupe([tags_search(text,search)])
        searchedtags=tags_search(text,search)
        if action =="replace":
            return ListToTupe([tags_replace(text,searchedtags,replace)])
        if action =="del":
            return ListToTupe([tags_ignore(text,searchedtags)])
        if action =="move2head":
            return ListToTupe([tags_head(text,searchedtags)])
        if action =="move2tail":
            return ListToTupe([tags_tail(text,searchedtags)])

# feat(core): NodePromptSearch - prompt search some text
class NodePromptSearch:
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


    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - search"

    OUTPUT_NODE = True
    def exec(self, text='',search=''):
        return ListToTupe([tags_search(text,search)])

# feat(core): NodePromptDup - prompt dup some text
class NodePromptDup:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)


    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - dup"

    OUTPUT_NODE = True
    def exec(self, text):
        return ListToTupe([tags_dup(text)])

# feat(core): NodePromptAdvDup - prompt dup some text (adv)
class NodePromptAdvDup:
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

    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - dup (adv)"

    OUTPUT_NODE = True
    def exec(self, text):
        a=''
        res=[]
        textl=text.split("\n")
        for line in textl:
            res.append(tags_dup(line))
        a='\n'.join(res)

        tags_dup(tags_onelineify(text))
        return ListToTupe([tags_dup(tags_onelineify(a)),a])
    
# feat(core): NodePromptShuffle - prompt shuffle some text
class NodePromptShuffle:
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


    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - shuffle"

    OUTPUT_NODE = True

    def exec(self, text='',keep_n_token='0',seed=0):
        random.seed(seed)
        textl=tags_listify(tags_onelineify(text))
        el=ListShuffle(textl,int(keep_n_token))
        return ListToTupe([','.join(el)])

# feat(core): NodePromptDel - prompt del some text
class NodePromptDel:
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

    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - del"

    OUTPUT_NODE = True

    def exec(self, search='',todel='',action='yes'):
        # https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
        if 'no' in action:
            return ListToTupe([search]) 
        ca=tags_ignore(search,tags_unweight(todel))
        return ListToTupe([ca])
    
# feat(core): NodePromptStd - prompt std
class NodePromptStd:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)

    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - std"

    OUTPUT_NODE = True

    def exec(self, text):
        return ListToTupe([tags_std(text)])
    
# feat(core): NodePromptInput - prompt input
class NodePromptInput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"default": "","multiline":True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('text',)

    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - input"

    OUTPUT_NODE = True

    def exec(self, text=''):
        return ListToTupe([tags_std(text)])

# feat(core): NodePromptUnweight - prompt unweight    
class NodePromptUnweight:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"forceInput":False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('STRING',)

    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - unweight"

    OUTPUT_NODE = True

    def exec(self, text):
        return ListToTupe([tags_unweight(text)])

# feat(core): NodePromptJoin - prompt join
class NodePromptJoin:
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

    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - join"

    OUTPUT_NODE = True

    def exec(self, a,b,c,d,e,f,g):
        vl=[a,b,c,d,e,f,g]
        vs = (",").join(vl)
        vs=tags_std(vs)
        # vs = vs.replace("  ", " ").replace(" ,", ",").replace(", ", ",").replace(",,", ",").replace(",,", ",")
        return {"ui": {"text": (vs,)}, "result": (vs,)}



class AnyType(str):
  """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

  def __ne__(self, __value: object) -> bool:
    return False

any_type = AnyType("*")


default_prompt1='''Swing
                                                Slide
                                                Climbing frame
                                                Sandbox
                                                See-saw
                                                Merry-go-round
                                                Jungle gym
                                                Trampoline
                                                Monkey bars
                                                Rocking horse
                                                Playhouse
                                                Hopscotch
                                                Balance beam
                                                Spring rider
                                                Water play area
                                                Ball pit
                                                Tunnel
                                                Zip line
                                                Basketball hoop
                                                Bicycle rack
                                                Spinner
                                                Climbing wall
                                                Rope ladder
                                                Tetherball
                                                Flying fox
                                                Swinging bridge
                                                Spiral slide
                                                Water sprinkler
                                                Pedal go-kart
                                                Miniature golf course
                                                '''
default_prompt1="\n".join([p.strip() for p in default_prompt1.split('\n') if p.strip()!=''])

# refer comfyui-mixlab-nodes
# feat(core): NodePromptRandom - prompt random
class NodePromptRandom:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "max_count": ("INT", {"default": 9, "min": 1, "max": 1000}),
                # "image_field": ("IMAGE",),
                "mutable_prompt": ("STRING", 
                         {
                            "multiline": True, 
                            "default": default_prompt1
                          }),
                "immutable_prompt": ("STRING", 
                         {
                            "multiline": True, 
                            "default": 'sticker, Cartoon, ``'
                          }),
                "random_sample": (["enable", "disable"],),
                # "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                },
            "optional":{
                    "seed": (any_type,  {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                }
            }
    
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - random"

    
    RETURN_TYPES = ("STRING",)

    # CATEGORY = "♾️Mixlab/Prompt"

    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True

    def exec(self,max_count,mutable_prompt,immutable_prompt,random_sample,seed=0):
        
        # Split the text into an array of words
        words1 = mutable_prompt.split("\n")

        # Split the text into an array of words
        words2 = immutable_prompt.split("\n")

        # progress bar
        # pbar = comfy.utils.ProgressBar(len(words1)*len(words2))
        
        # Select a random word from the array
        # random_word = random.choice(words)

        prompts=[]
        for w1 in words1:
            w1=w1.strip()
            for w2 in words2:
                w2=w2.strip()
                if '``' not in w2:
                    if w2=="":
                        w2='``'
                    else:
                        w2=w2+',``'
                if w1!='' and w2!='':
                    prompts.append(w2.replace('``', w1))
                # pbar.update(1)
        
        if len(prompts)==0:
            prompts.append(immutable_prompt)

        if random_sample=='enable':
            # random - get x-count element in array
            prompts = random.sample(prompts, min(max_count,len(prompts)))
        else:
            prompts = prompts[:min(max_count,len(prompts))]

        prompts= [elem.strip() for elem in prompts if elem.strip()]

        # return (new_prompt)
        return {"ui": {"prompts": prompts}, "result": (prompts,)}

def addWeight(text, weight=1):
    if weight == 1:
        return text
    else:
        return f"({text}:{round(weight,3)})"

# feat(core): NodePromptWeight - prompt add weight
class NodePromptWeight:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                
                "prompt_keyword": ("STRING", 
                         {
                            "multiline": False, 
                            "default": '',
                            "dynamicPrompts": False
                          }),

                "weight":("FLOAT", {"default": 1, "min": -3,"max": 3,"step": 0.01,"display": "slider"}),

                # "min_value":("FLOAT", {
                #         "default": -2, 
                #         "min": -10, 
                #         "max": 0xffffffffffffffff,
                #         "step": 0.01, 
                #         "display": "number"  
                #     }),
                # "max_value":("FLOAT", {
                #         "default": 2, 
                #         "min": -10, 
                #         "max": 0xffffffffffffffff,
                #         "step": 0.01, 
                #         "display": "number"  
                #     }),
              
                }
            }

    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "prompt - add weight"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    # FUNCTION = "run"
    # CATEGORY = "♾️Mixlab/Prompt"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)
    OUTPUT_NODE = False

    def exec(self,prompt_keyword,weight):
        # if weight < min_value:
        #     weight= min_value
        # elif weight > max_value:
        #     weight= max_value
        p=addWeight(prompt_keyword,weight)
        return (p,)