from siteglass.mergemin import MergeMinBuilder
from siteglass.jsmin import minify


class JSBuilder(MergeMinBuilder):
    
    name = 'js'
    
    def minify(self, contents):
        return minify(';'.join(contents).encode(self.config.get('global.encoding', 'utf-8')))
        