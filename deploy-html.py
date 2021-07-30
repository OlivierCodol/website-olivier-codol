
# http://localhost:63342/website-ocodol/compiled/index.html

import os
import pypandoc
import shutil

script_dir = os.path.dirname(os.path.realpath(__file__))
src_md_dir = os.path.join(script_dir, 'src-markdown')
src_html_dir = os.path.join(script_dir, 'src-html')
compil_dir = os.path.join(script_dir, 'docs')
template_dir = os.path.join(script_dir, 'template')

fp = open(template_dir + '/header.html', 'r')
header = fp.read()
fp.close()

fp = open(template_dir + '/navigation.html', 'r')
navigation = fp.read()
fp.close()

fp = open(template_dir + '/footer.html', 'r')
footer = fp.read()
fp.close()

for file in os.listdir(src_html_dir):
    source_file = src_html_dir + '/' + file
    compil_file = compil_dir + '/' + file  # .replace('.md', '.html')
    if compil_file[-18:] == "index-content.html":
        compil_file = compil_file[:-18] + "index.html"

    # pypandoc.convert_file(source_file, 'html', outputfile=compil_file)
    shutil.copy(source_file, compil_file)
    print(source_file + ' -> ' + compil_file)

    fp = open(compil_file, 'r+')
    source = fp.read()
    fp.seek(0)
    page = header + navigation + source + footer
    fp.write(page)
    fp.close()

