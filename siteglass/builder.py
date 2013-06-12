from glob import glob
import os
import os.path
import hashlib

class Builder(object):
    
    def __init__(self, config, versioned_files_map=None):
        self.config = config
        self.busted_paths = []
        self.versioned_files_map = {} if versioned_files_map is None else versioned_files_map
        
    def run(self):
        self.build()
        self.finish()
        
    def setup(self):
        pass
        
    def build(self):
        raise NotImplementedError
        
    def finish(self):
        self.rewrite_busted_paths()
        
    def get_paths(self, glob_or_list):
        if isinstance(glob_or_list, basestring):
            glob_or_list = [glob_or_list]
        paths = []
        for path in glob_or_list:
            for p in glob(self.get_abspath(path)):
                paths.append(p)
        return paths
        
    def get_text_file_contents(self, path):
        return open(path, 'rb').read().decode(
            self.config.get('global.encoding', 'utf-8'))
        
    def get_binary_file_contents(self, path):
        return open(path, 'rb').read()
        
    def put_text_file_contents(self, path, contents, versioned=True):
        versioned_path = self.get_versionized_path(path, contents) if versioned else path
        abs_versioned_path = self.get_abspath(versioned_path)
        self.create_dirs_for_file(abs_versioned_path)
        open(abs_versioned_path, 'wb').write(
            contents.encode(self.config.get('global.encoding', 'utf-8'))
        )
        if versioned:
            self.busted_paths.append((path, versioned_path))
        
    def rewrite_busted_paths(self):
        if not self.busted_paths:
            return
        rewrite = self.config.get('global.cache_bust.versioning.rewrite')
        if not rewrite:
            return
        relative_to = self.get_paths(self.config.get('global.cache_bust.versioning.relative_to', []))
        if relative_to:
            relative_to = [self.get_abspath(p) for p in relative_to]
        for path in self.get_paths(rewrite):
            contents = self.get_text_file_contents(path)
            bases = relative_to if relative_to else [os.path.dirname(path)]
            for old_path, new_path in self.busted_paths:
                old_abs_path = os.path.abspath(old_path)
                new_abs_path = os.path.abspath(new_path)
                prefix = ''
                for b in bases:
                    if old_abs_path.startswith(b):
                        prefix = b
                        break
                rel_old_path = old_abs_path[len(prefix):]
                rel_new_path = new_abs_path[len(prefix):]
                contents = contents.replace(rel_old_path, rel_new_path)
            self.put_text_file_contents(path, contents, False)
        
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
        if self.config.get('global.cache_bust.versioning.method') == 'lookup':
            self.versioned_files_map[path] = version
            return path
        else:
            name, ext = os.path.splitext(path)
            return '%s.%s%s' % (name, version, ext)
        
    def get_abspath(self, path):
        if os.path.isabs(path):
            return path
        return os.path.join(self.config['global.base_path'], path)