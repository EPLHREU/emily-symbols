# Emily's Symbol Dictionary


uniqueStarter = "SKWH"

# 4 : unique starter
# 2 : attachment
# 1 : capital
# 2 : variant
# 6 : symbol (@)
# 2 : duplication
LONGEST_KEY = 17 

# variant format = ['', 'E', 'U', 'EU']
# if no variants exist, then a single string can be used for the symbol and the variant specifier keys will be valid but ignored
symbols = {
        # more computer function-y symbols
        "FG"    : ["{#Tab}", "{#Backspace}", "{#Delete}", "{#Escape}"],             
        "RPBG"  : ["{#Up}", "{#Left}", "{#Right}", "{#Down}"],                      
        "FRPBG" : ["{#Page_Up}", "{#Home}", "{#End}", "{#Page_Down}"],              
        "FRBG"  : ["{#AudioPlay}", "{#AudioPrev}", "{#AudioNext}", "{#AudioMute}"], 
        ""      : ["", "{*!}", "{*?}", "{#Space}"],                                      

        # typable symbols
        "FR"     : ["!", "¡", "¡", "¬"],  
        "FP"     : ["\"", "“", "”", "„"], 
        "FRLG"   : ["#", "©", "®", "™"],  
        "RPBL"   : ["$", "¥", "€", "£"],  
        "FRPB"   : ["%", "‰", "‰", "‰"],  
        "FBG"    : "&",                   
        "F"      : ["'", "‘", "’", "‚"],  
        "FPL"    : ["(", "[", "<", "\{"], 
        "RBG"    : [")", "]", ">", "\}"], 
        "L"      : ["*", "×", "×", "×"],  
        "G"      : ["+", "§", "¶", "±"],  
        "B"      : ",",                   
        "PL"     : ["-", "–", "—", "—"],  
        "R"      : [".", "•", "•", "…"],  
        "RP"     : ["/", "÷", "÷", "÷"],  
        "LG"     : ":",                   
        "RB"     : ";",                   
        "PBLG"   : "=",                   
        "FPB"    : ["?", "¿", "¿", "¿"],  
        "FRPBLG" : "@",                   
        "FB"     : "\\",                  
        "RPG"    : ["^", "«", "»", "°"],  
        "BG"     : ["_", "µ", "µ", "µ"],  
        "P"      : "`",                   
        "PB"     : ["|", "¦", "¦", "¦"],  
        "FPBG"   : ["~", "˜", "˜", "˜"]   
}


def lookup(key):

    # filter irrelevant strokes
    if not key[0].startswith(uniqueStarter):
        raise KeyError
    if not len(key) == 1:
        raise KeyError
    assert len(key) <= LONGEST_KEY

    # nicely format the stroke for string manipulation
    stroke = str(key[0][len(uniqueStarter):])

    # support a blank stroke with no symbol
    if len(stroke) == 0:
        stroke = "-"

    # ensure that the uniqueStarter doesn't contain any trailing letters, therefor the next letter must be from the middle bank
    middleBank = ['A', 'O', 'E', 'U', "-", "*"]
    if stroke[0] not in middleBank:
        raise KeyError

    # remove a "-" if present, as all keys from this point on are unique
    stroke = stroke.replace("-", '')

    # calculate the attachment method, and remove attachment specifier keys
    attach = [False, False]
    if 'A' in stroke:
        attach[0] = True
        stroke = stroke.replace('A', '')
    if 'O' in stroke:
        attach[1] = True
        stroke = stroke.replace('O', '')

    # detect if capitalisation is required, and remove specifier key
    capital = False
    if "*" in stroke:
        capital = True
        stroke = stroke.replace("*", '')

    # calculate the variant number, and remove variant specifier keys
    variant = 0
    if 'E' in stroke:
        variant = variant + 1
        stroke = stroke.replace('E', '')
    if 'U' in stroke:
        variant = variant + 2
        stroke = stroke.replace('U', '')

    # calculate the repetition, and remove repetition specifier keys
    repeat = 1
    if 'S' in stroke:
        repeat = repeat + 1
        stroke = stroke.replace('S', '')
    if 'T' in stroke:
        repeat = repeat + 2
        stroke = stroke.replace('T', '')

    if not stroke in symbols:
        raise KeyError
    
    # extract symbol entry from the 'symbols' dictionary, with variant specification if available
    output = ""
    entry = symbols[stroke]
    if type(entry) == list:
        output = entry[variant]
    else:
        output = entry

    # repeat the symbol the specified number of times
    output = output * repeat

    # attachment space to either end of the symbol string to avoid escapement
    output = " " + output + " "

    # add appropriate attachment as specified
    if attach[0]:
        output = "{^}" + output
    if attach[1]:
        output = output + "{^}"

    # apply capitalisation 
    if capital:
        output = output + "{-|}"

    # all done :D
    return output
