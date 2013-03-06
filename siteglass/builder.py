from glob import glob
import os
import os.path
import hashlib

class Builder(object):
    
    def __init__(self, config):
        self.config = config
        
    def build(self):
        raise NotImplementedError
        
    def get_paths(self, glob_or_list):
        if isinstance(glob_or_list, basestring):
            return glob(glob_or_list)
        paths = []
        for g in glob_or_list:
            for p in glob(g):
                paths.append(p)
        return paths
        
    def get_text_file_contents(self, path):
        return open(path, 'rb').read().decode(
            self.config.get('global.encoding', 'utf-8'))
        
    def get_binary_file_contents(self, path):
        return open(path, 'rb').read()
        
    def put_text_file_contents(self, path, contents):
        path = self.get_versionized_path(path, contents)
        self.create_dirs_for_file(path)
        open(path, 'wb').write(
            contents.encode(self.config.get('global.encoding', 'utf-8'))
        )
        
    def put_binary_file_contents(self, path, contents):
        path = self.get_versionized_path(path, contents)
        self.create_dirs_for_file(path)
        open(path, 'wb').write(contents)
        
    def create_dirs_for_file(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
    def get_versionized_path(self, path, contents):
        if not self.config.get('global.cache_bust.enabled', False):
            return path
        version = self.config.get_version()
        if not version:
            version = hashlib.md5(contents).hexdigest()
        name, ext = os.path.splitext(path)
        return '%s.%s%s' % (name, version, ext)