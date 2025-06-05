import glob
import hashlib
# import json
# import numpy as np
# from numba import jit
import os
from pathlib import Path
from yors_pano_list_util import ListDelExclude,ListFillOne,ListToTupe,ListShuffle

# feat(core): use ymc suite/text/io as category
CURRENT_CATEGORY="ymc suite/text/io"
CURRENT_FUNCTION="exec"

def pyioReadDirectory(dir='',pattern='*.txt'):
    """
    pyio - get path at dir and pattern
    """
    res=[]
    for filename in glob.glob(os.path.join(dir,pattern)):
        res.append(filename)
    return res

def pyioReadAsText(loc):
    """
    pyio - read text at location
    """
    res=''
    with open(loc) as f:
        res = f.read()
        f.close()
    return res

def pyioGetFilesInDir(input_dir):
    """
    files = pyioGetFilesInDir(input_dir)
    """
    return [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]


def pyioParseFilename(filename:str):
    """
    pyioParseFilename('config.txt')
    """
    name, suffix = os.path.splitext(filename)
    return (name, suffix)

def pyioGetFilename(filename:str):
    """
    pyioGetFilename('config.txt')
    """
    name, suffix = os.path.splitext(filename)
    return name

def pyioPlibParseFilename(filename:str):
    """
    pyioPlibParseFilename('config.txt')
    """
    p=Path(filename)
    return (p.suffix, p.stem)

def StrmFromList(txtl:list[str],eof:str='\n'):
    """
    strm - from text list

    StrmFromList(fileAbsPathList)
    """
    return eof.join(txtl)


# feat(core): NodePyioFilenameListDetect - pyio - detect filename list
class NodePyioFilenameListDetect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "", "multiline": False}),
                "pattern": ("STRING", {"default": "*.txt", "multiline": False}),
                # "mode": ("STRING", {"default": "filename", "multiline": False}),
                "mode": (["filename", "abspath","filename-no-ext"],),
            }
        }

    RETURN_TYPES = ("STRING",'INT')
    RETURN_NAMES = ('STRING','count')
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "pyio - detect filename list"

    OUTPUT_NODE = True

    def exec(self, path='',pattern='*.txt',mode='filename'):

        fileAbsPathList=pyioReadDirectory(path,pattern)
        resl = fileAbsPathList
        if mode=='filename':
            fileNameList=list(map(os.path.basename,fileAbsPathList))
            resl=fileNameList
        if mode=='filename-no-ext':
            filenameNoExtList=list(map(pyioGetFilename,fileNameList))
            resl=filenameNoExtList


        # resl='\n'.join(resl)
        # fileAbsPathListStrm = StrmFromList(fileAbsPathList)
        # fileNameListStrm = StrmFromList(fileNameList)
        # filenmeWithoutSuffixList=StrmFromList(filenameNoExtList)
        return ListToTupe([StrmFromList(resl),len(resl)])
    
# feat(core): NodePyioFilenameListOutmDetect - pyio - detect filename list (outm)
class NodePyioFilenameListOutmDetect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "", "multiline": False}),
                "pattern": ("STRING", {"default": "*.txt", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING","INT")
    RETURN_NAMES = ('absPath','name','nameNoExt','count')
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    NODE_DESC = "pyio - detect filename list (outm)"

    OUTPUT_NODE = True

    def exec(self, path='',pattern='*.txt'):

        absPathList=pyioReadDirectory(path,pattern)

        nameList=list(map(os.path.basename,absPathList))

        nameNoExtList=list(map(pyioGetFilename,nameList))
        
        return ListToTupe([StrmFromList(absPathList),StrmFromList(nameList),StrmFromList(nameNoExtList),len(absPathList)])
    
# feat(core): IoUtilFileListGetText - io - get file list and read as text
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
    FUNCTION = CURRENT_FUNCTION
    CATEGORY = CURRENT_CATEGORY
    OUTPUT_NODE = True

    def exec(self, path='',pattern='*.txt'):
        plist=pyioReadDirectory(path,pattern)
        text=[]
        for loc in plist:
            text.append(pyioReadAsText(loc))
        # to multi line
        text='\n'.join(text)
        return ListToTupe([text])