import os
import sys

if os.path.dirname(__file__) == "":
    path = "./.."
else:
    path = os.path.dirname(__file__) + "/.."

sys.path.append(path)
