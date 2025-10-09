from PySide6.QtWidgets import *
from PySide6.QtCore import *

STYLEGLOBAL = """
            * {
                background-color: hsl(200, 20%, 90% );
                color: hsl(200, 30%, 10%);
                font-size: 14px;
                  }
"""


BACKGROUND_HIGHLIGHT = "* { background-color: hsl(200,80%,90%); }"
BACKGROUND_SEMIHIGHLIGHT = "* { background-color: hsl(200,50%,90%); }"
BACKGROUND_PLAIN = "* { background-color: hsl(200,10%, 90%); }"


TEXT_HIGHLIGHT = " * { font-size:16px; color: hsl(200,30%, 10%) }"
TEXT_SEMIHIGHLIGHT = "* { font-size:15px; color: hsl(200, 30%, 30%); }"
TEXT_PLAIN = "* { font-size:14px; color: hsl(200, 30%, 50%); }"
TEXT_SEMIHIDDEN = "* { font-size:14px; color: hsl(200, 30%, 70%); }"

