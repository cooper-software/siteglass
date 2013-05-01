import shutil
import os.path
from siteglass.builder import Builder

class CopyBuilder(Builder):
    
    def build(self):
        paths = self.config.get('copy')
        if paths:
            for src, dst in paths.items():
                print "%s -> %s" % (src,dst)
                self.do_one(self.get_abspath(src),self.get_abspath(dst))
                
    def do_one(self, src, dst):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)