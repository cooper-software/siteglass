from siteglass.mergemin import MergeMinBuilder
from cssmin import cssmin
import re
import os.path
import base64
import urllib

class CSSBuilder(MergeMinBuilder):
    
    name = 'css'
    import_pattern = re.compile('@import\s+url\([\'"]?([^\)]+)[\'"]?\);?')
    asset_types = [
        {
            'pattern': re.compile('url\\([\'"]?([^\'"\\)]+)[\'"]?\\)\\s+format\\([\'"]?woff[\'"]?\\)'),
            'mime': 'application/x-font-woff',
        },
        {
            'pattern': re.compile('url\\([\'"]?([^\'"\)]+?\.svg)[\'"]?\\)'),
            'mime': 'image/svg+xml'
        },
        {
            'pattern': re.compile('url\\([\'"]?([^\'"\)]+?\.png)[\'"]?\\)'),
            'mime': 'image/png'
        },
        {
            'pattern': re.compile('url\\([\'"]?([^\'"\)]+?\.jpg)[\'"]?\\)'),
            'mime': 'image/jpeg'
        }
    ]
    
    def process_content(self, path, content):
        if self.options.get('resolve_imports', True):
            content = self.resolve_imports(path, content)
        if self.options.get('inline_assets', True):
            content = self.inline_assets(path, content)
        return content
        
    def resolve_imports(self, path, content):
        paths = {}
        for statement, import_path in self.get_matches(self.import_pattern, path, content):
            if paths.get(import_path):
                continue
            paths[import_path] = 1
            import_contents = self.get_text_file_contents(import_path)
            import_contents = self.adjust_asset_paths(import_path, path, import_contents)
            import_contents = self.resolve_imports(import_path, import_contents)
            content = content.replace(statement, import_contents)
        return content
        
    def adjust_asset_paths(self, old_path, new_path, content):
        old_base_path = os.path.dirname(old_path)
        new_base_path = os.path.dirname(new_path)
        if old_base_path == new_base_path:
            return content
        for type in self.asset_types:
            for statement, path in self.get_matches(type['pattern'], old_path, content):
                asset_path = os.path.abspath(path)
                content = content.replace(
                    os.path.relpath(asset_path, old_base_path),
                    os.path.relpath(asset_path, new_base_path)
                )
        return content
    
    def inline_assets(self, base_path, content):
        for type in self.asset_types:
            for statement, path in self.get_matches(type['pattern'], base_path, content):
                asset_content = self.get_binary_file_contents(path)
                encoded_content = urllib.quote(base64.encodestring(asset_content))
                new_statement = u'url(data:%s;base64,%s)' % (type['mime'], encoded_content)
                content = content.replace(statement, new_statement)
        return content
        
    def get_matches(self, pattern, path, content):
        if self.options.get('relative_to') == 'target':
            base_path = self.options.get('target', os.path.dirname(path))
        else:
            base_path = os.path.dirname(os.path.abspath(path))
        for match in pattern.finditer(content):
            yield match.group(0), os.path.join(base_path, match.group(1))
        
    def minify(self, contents):
        return cssmin(''.join(contents))
        