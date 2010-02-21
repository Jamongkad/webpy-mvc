import re, os, sys
from mako.template import Template
from mako.lookup import TemplateLookup

directories = ['./views']

[directories.append(dirpath) for dirpath, dirnames, filenames in os.walk(os.path.abspath('./modules'))
    if re.search('(?<=views)', dirpath)]

mylookup = TemplateLookup(directories, output_encoding='utf-8')

def render(templatename, **kwa):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwa)
