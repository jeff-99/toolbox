__author__ = 'jeff'
import os
import re
from toolbox.cli \
    import main

class Parser(object):
    def __init__(self, template_dir, dest_dir, args):
        self.template_dir = template_dir
        self.dest_dir = dest_dir
        self.args = args

    def _parse_line(self, line):
        pattern = r'{{(.*?)}}'

        match = re.search(pattern,line)
        if match is not None:
            key = match.group(1)
            try:
                name = self.args[key]
            except KeyError:
                raise AttributeError('Template variable {} was not set in the provided args'.format(key))
            key_pattern = r'{{(' + key + ')?}}'
            line = re.sub(key_pattern, name,line,0)

        return line

    def _parse_path(self,path):
        return self._parse_line(path)

    def _parse_file(self,fp):
        new_data = []
        with open(fp, 'r') as f:
            data = f.readlines()
            for line in data:
                new_data.append(self._parse_line(line))

        return "".join(new_data)

    def parse(self):
        dir_content = []
        for cur_path, dirs, files in os.walk(self.template_dir):

            new_path = re.sub(self.template_dir, self.dest_dir, cur_path)

            path = self._parse_path(new_path)
            file_paths = [self._parse_path(fp) for fp in files]
            file_contents = [self._parse_file(os.path.join(cur_path,fp)) for fp in files]

            dir_content.append((path, file_paths, file_contents))

        return dir_content
