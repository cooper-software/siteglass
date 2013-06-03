import re
import os, os.path
from siteglass.js import JSBuilder
from siteglass import data


class AMDBuilder(JSBuilder):
    
    name = 'amd'
    statement_pattern = re.compile('(require|define)\s*\(\s*([\'"][^\'"]+[\'"]\s*,\s*)?(\[\s*[^\]]+\])')
    names_pattern = re.compile('[\'"]([^\'"]+)[\'"]')
    nameless_define_pattern = re.compile('define\(\s*(function|\[|[a-zA-Z_])')
    
    def process_content(self, path, content):
        base_path = self.config.get('global.amd.basePath')
        if not base_path:
            base_path = os.path.dirname(path)
        content = self.resolve_requires(base_path, path, content)
        almond = self.get_text_file_contents(data.get('almond.js'))
        return almond + content
        
    def resolve_requires(self, base_path, path, content, visited=None):
        if visited is None:
            visited = {}
        content = self.fix_nameless_defines(path, content)
        names = []
        for match in self.statement_pattern.finditer(content):
            for name in self.names_pattern.findall(match.group(3)):
                if name not in visited:
                    names.append(name)
                    visited[name] = 1
        contents = [content]
        for name in names:
            if not name.endswith('.js'):
                name += '.js'
            require_path = self.resolve_path(base_path, name)
            require_content = self.get_text_file_contents(require_path)
            contents.append(
                # Note we are using the path of the requiring file here.
                # This is to keep all path resolution relative to the file
                # that was passed as "main"
                self.resolve_requires(base_path, require_path, require_content, visited)
            )
            
        return ';'.join(contents)
        
    def resolve_path(self, base_path, name):
        paths = self.config.get('global.amd.paths')
        if paths:
            for k,v in paths.items():
                if name.startswith(k):
                    name = v + name[len(k):]
        return os.path.join(base_path, name)
        
    def fix_nameless_defines(self, path, content):
        path = os.path.splitext(path.split(os.sep)[-1])[0]
        return self.nameless_define_pattern.sub('define("%s", \g<1>' % path, content)