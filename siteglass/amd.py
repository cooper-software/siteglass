import re
import os.path
from siteglass.js import JSBuilder
from siteglass import data


class AMDBuilder(JSBuilder):
    
    name = 'amd'
    statement_pattern = re.compile('((require|define)\s*\(\s*\[\s*[^\]]+\])')
    names_pattern = re.compile('[\'"]([^\'"]+)[\'"]')
    
    def process_content(self, path, content):
        content = self.resolve_requires(path, content)
        almond = self.get_text_file_contents(data.get('almond.js'))
        return almond + content
        
    def resolve_requires(self, path, content, visited={}):
        base_path = os.path.dirname(path)
        names = []
        for match in self.statement_pattern.finditer(content):
            for name in self.names_pattern.findall(match.group(0)):
                if name not in visited:
                    names.append(name)
                    visited[name] = 1
        contents = [content]
        for name in names:
            if not name.endswith('.js'):
                name += '.js'
            require_path = os.path.join(base_path, name)
            require_content = self.get_text_file_contents(require_path)
            contents.append(
                # Note we are using the path of the requiring file here.
                # This is to keep all path resolution relative to the file
                # that was passed as "main"
                self.resolve_requires(path, require_content)
            )
            
        return ';'.join(contents)