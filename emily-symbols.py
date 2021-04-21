# Emily's Symbol Dictionary
import re

uniqueStarters = ["SKWH", "STWH"]

# define if attachment keys define where "space"s or "attachment"s lie
attachmentMethod = "space"

LONGEST_KEY = 1

# variant format = ['', 'E', 'U', 'EU']
# if no variants exist, then a single string can be used for the symbol and the variant specifier keys will be valid but ignored
symbols = {
    "SKWH": {
        # more computer function-y symbols
        "FG"    : ["{#Tab}", "{#Backspace}", "{#Delete}", "{#Escape}"],             
        "RPBG"  : ["{#Up}", "{#Left}", "{#Right}", "{#Down}"],                      
        "FRPBG" : ["{#Page_Up}", "{#Home}", "{#End}", "{#Page_Down}"],              
        "FRBG"  : ["{#AudioPlay}", "{#AudioPrev}", "{#AudioNext}", "{#AudioMute}"], 
        ""      : ["", "{*!}", "{*?}", "{#Space}"],                                 

        # typable symbols
        "FR"     : ["!", "¬", "↦", "¡"],  
        "FP"     : ["\"", "“", "”", "„"], 
        "FRLG"   : ["#", "©", "®", "™"],  
        "RPBL"   : ["$", "¥", "€", "£"],  
        "FRPB"   : ["%", "‰", "‱", "φ"],  
        "FBG"    : ["&", "∩", "∧", "∈"],  
        "F"      : ["'", "‘", "’", "‚"],  
        "FPL"    : ["(", "[", "<", "\{"], 
        "RBG"    : [")", "]", ">", "\}"], 
        "L"      : ["*", "∏", "§", "×"],  
        "G"      : ["+", "∑", "¶", "±"],  
        "B"      : [",", "∪", "∨", "∉"],  
        "PL"     : ["-", "−", "–", "—"],
        "R"      : [".", "•", "·", "…"],  
        "RP"     : ["/", "⇒", "⇔", "÷"],  
        "LG"     : [":", "∋", "∵", "∴"],  
        "RB"     : [";", "∀", "∃", "∄"],  
        "PBLG"   : ["=", "≡", "≈", "≠"],  
        "FPB"    : ["?", "¿", "∝", "‽"],  
        "FRPBLG" : ["@", "⊕", "⊗", "∅"],  
        "FB"     : ["\\", "Δ", "√", "∞"], 
        "RPG"    : ["^", "«", "»", "°"],  
        "BG"     : ["_", "≤", "≥", "µ"],  
        "P"      : ["`", "⊂", "⊃", "π"],  
        "PB"     : ["|", "⊤", "⊥", "¦"],  
        "FPBG"   : ["~", "⊆", "⊇", "˜"],  
        "FPBL"   : ["↑", "←", "→", "↓"]   
    },
    "STWH": {
        ""       : "test"
    }
}


def lookup(key):

    # decompose stroke. DZ are unused
    match = re.fullmatch(r'([#STKPWHR]*)([AO]*)([*-]?)([EU]*)([FRPBLG]*)([TS]*)', key[0])
    if match is None:
        raise KeyError

    (starter, attachments, capitalisation, variants, selection, repetitions) = match.groups()
    if starter not in uniqueStarters:
        raise KeyError
    if len(key) != 1:
        raise KeyError
    assert len(key) <= LONGEST_KEY

    # calculate the attachment method, and remove attachment specifier keys
    attach = [(attachmentMethod == "space") ^ ('A' in attachments),
              (attachmentMethod == "space") ^ ('O' in attachments)]

    # detect if capitalisation is required, and remove specifier key
    capital = capitalisation == '*'

    # calculate the variant number, and remove variant specifier keys
    variant = 0
    if 'E' in variants:
        variant = variant + 1
    if 'U' in variants:
        variant = variant + 2

    # calculate the repetition, and remove repetition specifier keys
    repeat = 1
    if 'S' in repetitions:
        repeat = repeat + 1
    if 'T' in repetitions:
        repeat = repeat + 2

    if selection not in symbols[starter]:
        raise KeyError

    # extract symbol entry from the 'symbols' dictionary, with variant specification if available
    output = symbols[starter][selection]
    if type(output) == list:
        output = output[variant]

    # repeat the symbol the specified number of times
    output = output * repeat

    # attachment space to either end of the symbol string to avoid escapement,
    # but prevent doing this for retrospective add/delete spaces, since it'll
    # mess with these macros
    if output not in ["{*!}", "{*?}", "{#Space}"]:
        output = " " + output + " "

    # add appropriate attachment as specified
    if attach[0]:
        output = "{^}" + output
    if attach[1]:
        output = output + "{^}"

    # cancel out some formatting when using space attachment 
    if attachmentMethod == "space":
        if not attach[0]:
            output = "{}" + output
        if not attach[1]:
            output = output + "{}" 

    # apply capitalisation 
    if capital:
        output = output + "{-|}"

    # all done :D
    return output
