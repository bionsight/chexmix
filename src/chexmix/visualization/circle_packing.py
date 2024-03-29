import json
import uuid
from string import Template

from chexmix.visualization import js
import pkg_resources
from IPython.display import HTML, Javascript, display


def init():
    display(js.require('https://d3js.org/d3.v5.min.js'))


def inject_chart_js(data, height=932, width=932):
    js_file = pkg_resources.resource_filename(__name__, 'circle_packing.js')

    unique_id = str(uuid.uuid4())
    display(HTML(f"<div id={unique_id} style='height: {height}px;width: {width}px;'></div>"))

    with open(js_file, 'r', encoding='utf-8') as f:
        circle_packing_template = Template(f.read())
        js_data = json.dumps(data)
        cp_template = circle_packing_template.substitute(id=unique_id, width=width, height=height, data=js_data)
        display(Javascript(cp_template))


def form_data(node, normalize_func):
    node = normalize_func(node)
    node['children'] = [form_data(n, normalize_func) for n in node['children']]
    return node


def draw(node, normalize_func=None, **kwargs):
    if normalize_func is not None:
        node = form_data(node, normalize_func)

    return inject_chart_js(node, **kwargs)
