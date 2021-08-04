
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
navgtn = fp.read()
fp.close()

fp = open(template_dir + '/footer.html', 'r')
footer = fp.read()
fp.close()

files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(src_html_dir)) for f in fn]
ix = len(src_html_dir) + 1

for filepath in files:

    file = filepath[ix:]
    source_file = os.path.join(src_html_dir, file)
    if file == "index-content.html":
        file = "index.html"
    compil_file = os.path.join(compil_dir, file)  # .replace('.md', '.html')

    navitem_old_pre = """li class="nav-item"><a class="nav-link" href=" """
    navitem_old_suf = """ " data-no="1">"""
    navitem_old = navitem_old_pre[:-1] + file + navitem_old_suf[1:]
    navitem_new_pre = """li class="nav-item selected"><a class="nav-link" href=" """
    navitem_new = navitem_new_pre[:-1] + file + navitem_old_suf[1:]

    relative_path = "../" * file[:file.rfind("\\") + 1].count("\\")
    href_flag = """href=" """[:-1]
    src_flag = """src=" """[:-1]

    # pypandoc.convert_file(source_file, 'html', outputfile=compil_file)
    os.makedirs(os.path.dirname(compil_file), exist_ok=True)
    shutil.copy(source_file, compil_file)
    print(source_file + ' -> ' + compil_file)

    fp = open(compil_file, 'r+')
    source = fp.read()
    header_new = header.replace(href_flag + "css", href_flag + relative_path + "css")
    navgtn_new = navgtn.replace(href_flag, href_flag + relative_path).replace(src_flag, src_flag + relative_path)
    source_new = source.replace(href_flag, href_flag + relative_path).replace(src_flag, src_flag + relative_path)
    footer_new = footer.replace(href_flag, href_flag + relative_path).replace(src_flag, src_flag + relative_path)
    navgtn_new = navgtn_new.replace(navitem_old, navitem_new)
    fp.seek(0)
    page = header_new + navgtn_new + source_new + footer_new
    fp.write(page)
    fp.close()
