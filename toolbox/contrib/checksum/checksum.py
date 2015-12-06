import hashlib
from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import RegistryMixin, ConfigMixin


class ChecksumPlugin(ConfigMixin,RegistryMixin, ToolboxPlugin):

    name = 'checksum'
    description = 'Calculate or compare the checksum of a file'

    def prepare_parser(self, parser):
        parser.add_argument("-f","--file",help="file to get checksum of")
        parser.add_argument("-m","--method", help="hashing method")
        parser.add_argument("-c","--checksum",help="given checksum")
        parser.set_defaults(method="sha1")

    def execute(self, args):
        config = self.get_config()

        if args.file:
            with open(args.file,"rb") as inf:
                data = inf.read()
                if args.checksum:
                    print(validate_checksum(data,args.checksum,args.method))
                else:
                    print(calc_checksum(data,args.method))

def validate_checksum(data,checksum,method):
    if data is not None:
        if method == "sha1":
            return hashlib.sha1(data).hexdigest() == checksum
        elif method == "md5":
            return hashlib.md5(data).hexdigest() == checksum

def calc_checksum(data,method):
    if method == "sha1":
        return hashlib.sha1(data).hexdigest()
    elif method == "md5":
        return hashlib.md5(data).hexdigest()


