import re

def target_type_detection(target):

    if target == '*':
        return glob

    #commas can be present in regex too
    #make sure its infact a list, this is a regex representing a list with atleast 2 items 
    #single item list should be returned as a glob so it ensures 2 items with a mandatory comma atleast
    if re.fullmatch(r'\s*([A-Za-z0-9_.]+)\s*,\s*([A-Za-z0-9_.]+)\s*(,\s*[A-Za-z0-9_.]+\s*)*', target): 
        return 'list'
        

    else: 

        #compound may have grain or regex parts so need to make sure its not compound first
        if ' and ' in target or ' or ' in target or ' not ' in target:
            return 'compound'
        
        else: 

            if re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}", target): #regex can have '.' too so just that wont work
                return 'ipcidr'

            elif ':' in target:
                return 'grain'

            elif target.startswith('group'):
                return 'nodegroup'

            elif any(char in target for char in ['*', '+', '?', '.', '^', '$', '[', ']', '{', '}', '(', ')', '|']):
                return 'regex'

            else: 
                return 'glob'
    



if __name__=="__main__":
    target = 'minand'
    print(target_type_detection(target))
  