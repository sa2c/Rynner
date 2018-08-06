import pystache

renderer = pystache.Renderer()


class Template:
    @classmethod
    def from_file(self, path):
        with open(path, 'r') as f:
            content = f.read()
        return Template(content)

    def __init__(self, template_string):
        self.template_string = template_string

    def render(self, args):
        renderer.render(self.template_string, args)
