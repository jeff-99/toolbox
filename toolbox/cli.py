import sys
from .core import Toolbox


def main():
    toolbox = Toolbox()
    toolbox(sys.argv[1:])