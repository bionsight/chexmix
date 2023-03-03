from string import Template

import pkg_resources
from IPython.display import Javascript, display


def save(elem_id, filename):
    js_file = pkg_resources.resource_filename(__name__, 'svg.js')

    with open(js_file, 'r', encoding='utf-8') as f:
        js_template = Template(f.read())
        display(Javascript(js_template.substitute(svg_id=elem_id, filename=filename)))
