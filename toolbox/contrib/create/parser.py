__author__ = 'jeff'
import os
import re
from .renderer import ALIASES


class Parser(object):
    def __init__(self, template_dir, dest_dir, args):
        self.template_dir = template_dir
        self.dest_dir = dest_dir
        self.args = args

    def resolve_key(self, match):
        """
        Resolve the matched key and process it's value based on the supplied renderer
        :param match:
        :return:
        :rtype: str
        """
        args = match.group(1).split('|')
        key = args[0]
        processor_funcs = args[1:]

        value = self.args.get(key, '')
        for func_name in processor_funcs:
            # get renderer func or use to string func
            value = ALIASES.get(func_name, str)(value)

        return value

    def _parse_line(self, line):
        """
        finds variable names from the provided line and calls the resolve_key method with eventual matches
        It replaces the match with the resolved value and returns the line
        :param line:
        :return:
        """
        pattern = r'{{(.*?)}}'
        line = re.sub(pattern, self.resolve_key, line)

        return line

    def _parse_path(self, path):
        return self._parse_line(path)

    def _parse_file(self, fp):
        new_data = []
        with open(fp, 'r') as f:
            data = f.readlines()
            for line in data:
                new_data.append(self._parse_line(line))

        return "".join(new_data)

    def parse(self):
        """
        Walk the template dir, read the template files and parse them replacing variables in the files with values
        given in the context dictionary.
        Return a list of directories and files with their parsed content basically the output of os.walk.

        :return:
        """
        dir_content = []
        for cur_path, dirs, files in os.walk(self.template_dir):

            new_path = cur_path.replace(self.template_dir, self.dest_dir)

            path = self._parse_path(new_path)
            file_paths = [self._parse_path(fp) for fp in files]
            file_contents = [self._parse_file(os.path.join(cur_path, fp))
                             for fp in files]

            dir_content.append((path, file_paths, file_contents))

        return dir_content
