import sys
from .core import Toolbox, UnknownPlugin


def main():
    t = Toolbox()
    t.prepare()

    try:
        t.execute(sys.argv[1:])
    except UnknownPlugin:
        return

    t.shutdown()