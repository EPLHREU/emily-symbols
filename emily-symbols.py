# Emily's Symbol Dictionary
import re

# define your starters here
#                standard  custom
uniqueStarters = ["SKWH", "#SKWH"]

# define if attachment keys define where "space"s or "attachment"s lie
attachmentMethod = "space"

LONGEST_KEY = 1

# variant format = ['', 'E', 'U', 'EU']
# if no variants exist, then a single string can be used for the symbol and the variant specifier keys will be valid but ignored
symbols = {
    uniqueStarters[0]: { # standard
        # more computer function-y symbols
        "FG"    : ["{#Tab}", "{#Backspace}", "{#Delete}", "{#Escape}"],
        "RPBG"  : ["{#Up}", "{#Left}", "{#Right}", "{#Down}"],
        "FRPBG" : ["{#Page_Up}", "{#Home}", "{#End}", "{#Page_Down}"],
        "FRBG"  : ["{#AudioPlay}", "{#AudioPrev}", "{#AudioNext}", "{#AudioStop}"],
        "FRB"   : ["{#AudioMute}", "{#AudioLowerVolume}", "{#AudioRaiseVolume}", "{#Eject}"],
        ""      : ["", "{*!}", "{*?}", "{#Space}"],
        "FL"    : ["{*-|}", "{*<}", "{<}", "{*>}"],

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
    uniqueStarters[1]: { # custom
        # add your own strokes here (or above, or wherever else you like)!
        ""       : "test"
    }
}


def lookup(chord):

    # normalise stroke from embedded number, to preceding hash format
    stroke = chord[0]
    if any(k in stroke for k in "1234506789"):  # if chord contains a number
        stroke = list(stroke)
        numbers = ["O", "S", "T", "P", "H", "A", "F", "P", "L", "T"]
        for key in range(len(stroke)):
            if stroke[key].isnumeric():
                stroke[key] = numbers[int(stroke[key])]  # set number key to letter
                numberFlag = True
        stroke = ["#"] + stroke
        stroke = "".join(stroke)

    # the regex decomposes a stroke into the following groups/variables:
    # starter                #STKPWHR
    # attachments                         AO
    # capitalisation                             */-
    # variants                                          EU
    # pattern                                                  FRPBLG
    # repetitions                                                         TS
    #                                       (unused: DZ)
    match = re.fullmatch(r'([#STKPWHR]*)([AO]*)([*-]?)([EU]*)([FRPBLG]*)([TS]*)', stroke)

    if match is None:
        raise KeyError
    (starter, attachments, capitalisation, variants, pattern, repetitions) = match.groups()

    if starter not in uniqueStarters:
        raise KeyError
    if len(chord) != 1:
        raise KeyError
    assert len(chord) <= LONGEST_KEY

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

    if pattern not in symbols[starter]:
        raise KeyError

    # extract symbol entry from the 'symbols' dictionary, with variant specification if available
    selection = symbols[starter][pattern]
    if type(selection) == list:
        selection = selection[variant]
    output = selection

    # repeat the symbol the specified number of times
    output = output * repeat

    # attachment space to either end of the symbol string to avoid escapement,
    # but prevent doing this for retrospective add/delete spaces, since it'll
    # mess with these macros
    if selection not in ["{*!}", "{*?}"]:
        output = " " + output + " "

    # add appropriate attachment as specified (again, prevent doing this 
    # for retrospective add/delete spaces)
    if selection not in ["{*!}", "{*?}"]:
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
