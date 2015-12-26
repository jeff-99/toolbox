import sys
from toolbox.core import Toolbox


def main():
    toolbox = Toolbox()
    toolbox(sys.argv[1:])


if __name__ == '__main__':
    main()
