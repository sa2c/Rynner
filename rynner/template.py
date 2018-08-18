import pystache

renderer = pystache.Renderer()

class TemplateArgumentException(Exception):
    pass

class Template:
    @classmethod
    def from_file(self, path):
        with open(path, 'r') as f:
            content = f.read()
        return Template(content)

    def __init__(self, template_string):
        self.parsed = pystache.parse(template_string)

    def render(self, args):
        try:
            argset = set(args.keys())
        except:
            raise TemplateArgumentException('invalid type of template arguments')

        if argset == self.keys():
            return renderer.render(self.parsed, args)
        else:
            raise TemplateArgumentException(
                f'template arguments do not match {self.keys()} != {argset}')

    def keys(self):
        return {s.key for s in self.parsed._parse_tree if type(s) != str}
