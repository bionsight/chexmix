from IPython.display import Javascript

# See https://github.com/twosigma/beakerx/issues/6747


def require(src, src_type='text/javascript'):
    js_template = """
        var script = document.createElement('script');
        script.type = '{src_type}';
        script.src = '{src}';
        document.head.appendChild(script);
    """
    return Javascript(js_template.format(src=src, src_type=src_type))


def link(href, rel, src_type):
    js_template = """
        var link = document.createElement('link');
        link.type = '{src_type}';
        link.rel = '{rel}';
        link.href = '{href}';
        document.head.appendChild(link);
    """
    return Javascript(js_template.format(href=href, rel=rel, src_type=src_type))


def link_css(css_src):
    return link(href=css_src, rel='stylesheet', src_type='text/css')
