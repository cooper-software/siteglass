import shutil
import os.path
from siteglass.builder import Builder

class CopyBuilder(Builder):
    
    def build(self):
        paths = self.config.get('copy')
        if paths:
            for src, dst in paths.items():
                self.do_one(src,dst)
                
    def do_one(self, src, dst):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)