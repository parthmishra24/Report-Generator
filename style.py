from questionary import Style

custom_style = Style([
    ("qmark", "fg:#00afaf"),         # question mark
    ("question", "bold fg:#ffffff"), # actual question text
    ("answer", "fg:#5fff5f bold"),   # submitted answer
    ("pointer", "fg:#5f87ff bold"),  # > pointer
    ("highlighted", "fg:#ffffaf"),   # highlighted item
    ("selected", "fg:#ffffff bg:#444444"),  # selected from list
    ("instruction", "fg:#808080"),   # instructions like "press enter"
    ("text", "fg:#ffffff"),          # regular text input
    ("disabled", "fg:#606060 italic") # disabled options
])