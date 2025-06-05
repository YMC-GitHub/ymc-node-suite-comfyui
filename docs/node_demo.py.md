CURRENT_CATEGORY="ymc/suite"
CURRENT_FUNCTION="exec"

class TextInput:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "text": ("STRING",{"multiline": True,"default": ""}),
                  },
                }
    
    RETURN_TYPES = ("STRING",) 
    CATEGORY = CURRENT_CATEGORY
    FUNCTION = CURRENT_FUNCTION
    NODE_DESC = "text - input with multiline input"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def exec(self,text):
       
        return (text,)
    