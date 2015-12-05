import sys
from .core import Toolbox


def main():
    t = Toolbox()
    t.prepare()
    t.execute(sys.argv[1:])
    t.shutdown()