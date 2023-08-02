from __future__ import annotations

def generate_dropdown_option(options:list|dict, all:bool=False)->list[dict]:
    
    if type(options) is list :
        dict_options = [{"label": i, "value": i} for i in options]
    elif type(options) is dict :
        dict_options = [{"label": options[i], "value": i} for i in options]
    else :
        raise TypeError

    

    if all == True:
        dict_options.append({"label": "All", "value": "All"})

    return dict_options