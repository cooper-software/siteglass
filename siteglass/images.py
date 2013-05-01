import subprocess
import shutil
import os.path
from distutils.spawn import find_executable
from siteglass.builder import Builder

SUPPORTS_PNG = find_executable('optipng') is not None
SUPPORTS_JPEG = find_executable('optipng') is not None

class ImagesBuilder(Builder):
    
    types = {
        'jpeg': {
            'is_supported': SUPPORTS_JPEG,
            'unsupported_error': 'Cannot optimize JPGs without jpegoptim.',
            'command': 'jpegoptim -f --strip-all %(path)s'
        },
        'png': {
            'is_supported': SUPPORTS_PNG,
            'unsupported_error': 'Cannot optimize PNGs without optipng.',
            'command': 'optipng -force -o7 %(path)s'
        }
    }
    
    extension_aliases = {
        'jpg': 'jpeg'
    }
    
    def build(self):
        options_list = self.config.get('images')
        if options_list:
            for options in options_list:
                self.do_one(options)
        
    def do_one(self, options):
        source = options['source']
        target = options.get('target', None)
        
        for path in self.get_paths(source):
            if target:
                target_path = os.path.join(target, os.path.basename(path))
            else:
                target_path = path
            self.optimize(path, target_path)
        
    def optimize(self, source, target):
        basename, ext = os.path.splitext(source)
        
        if not ext:
            return
        
        ext = ext[1:]
        
        if ext in self.extension_aliases:
            ext = self.extension_aliases[ext]
        
        type = self.types.get(ext)
        
        if not type:
            raise RuntimeError, "Unsupported image type '%s'" % ext
        
        if not type['is_supported']:
            raise RuntimeError, type['unsupported_error']
        
        if target != source:
            self.create_dirs_for_file(target)
            shutil.copy(source, target)
        
        command = type['command'] % { 'path': target }
        subprocess.call(command, shell=True)