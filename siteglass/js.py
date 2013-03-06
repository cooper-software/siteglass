from siteglass.mergemin import MergeMinBuilder
from jsmin import jsmin


class JSBuilder(MergeMinBuilder):
    
    name = 'js'
    
    def minify(self, contents):
        return jsmin(';'.join(contents))
        