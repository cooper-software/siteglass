from siteglass.builder import Builder

class MergeMinBuilder(Builder):
    
    name = 'abstractmergemin'
    
    def build(self):
        options_list = self.config.get(self.name)
        if options_list:
            for options in options_list:
                self.do_one(options)
        
    def do_one(self, options):
        self.options = options
        source = options['source']
        target = options.get('target', source)
        print "%s -> %s" % (source, target)
        contents = []
        for p in self.get_paths(source):
            content = self.process_content(p, self.get_text_file_contents(p))
            contents.append(content)
        self.put_text_file_contents(target, self.minify(contents))
        
    def process_content(self, path, content):
        return content
        
    def minify(self, contents):
        raise NotImplementedError