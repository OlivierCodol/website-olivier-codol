
# http://localhost:63342/website-ocodol/compiled/index.html

import os
import pypandoc

# result = pypandoc.convert_file('src/index.md', 'html')
# print(result)

source_dir = 'src'
compil_dir = 'docs'
template_dir = 'template'

fp = open(template_dir + '/header.html', 'r')
header = fp.read()
fp.close()

fp = open(template_dir + '/navigation.html', 'r')
navigation = fp.read()
fp.close()

fp = open(template_dir + '/footer.html', 'r')
footer = fp.read()
fp.close()

for file in os.listdir(source_dir):
    source_file = source_dir + '/' + file
    compil_file = compil_dir + '/' + file.replace('.md', '.html')

    pypandoc.convert_file(source_file, 'html', outputfile=compil_file)
    print(source_file + ' -> ' + compil_file)

    fp = open(compil_file, 'r+')
    source = fp.read()
    fp.seek(0)
    page = header + navigation + source + footer
    fp.write(page)
    fp.close()

