
# http://localhost:63342/website-olivier-codol/docs/index.html
import os
import pypandoc
import shutil


# function to get file content
def readfile(filename):
    fp = open(filename, 'r')
    content = fp.read()
    fp.close()
    return content


# get directory paths
script_dir = os.path.dirname(os.path.realpath(__file__))
src_md_dir = os.path.join(script_dir, 'src-markdown')
src_html_dir = os.path.join(script_dir, 'src')
compil_dir = os.path.join(script_dir, 'docs')
template_dir = os.path.join(script_dir, 'template')

# get template (static) contents
header = readfile(template_dir + '/header.html')
navgtn = readfile(template_dir + '/navigation.html')
footer = readfile(template_dir + '/footer.html')
blog_header = readfile(template_dir + '/blogpost-header.html')
blog_footer = readfile(template_dir + '/blogpost-footer.html')

# get list of files to compile
files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(src_html_dir)) for f in fn]
ix = len(src_html_dir) + 1


for filepath in files:

    file = filepath[ix:]
    source_file = os.path.join(src_html_dir, file)
    if file == "index-content.html":
        file = "index.html"
    compil_file = os.path.join(compil_dir, file)

    # this highlights the navigation tab on the corresponding page
    navitem_old_pre = """li class="nav-item"><a class="nav-link" href=" """
    navitem_old_suf = """ " data-no="1">"""
    navitem_old = navitem_old_pre[:-1] + file + navitem_old_suf[1:]
    navitem_new_pre = """li class="nav-item selected"><a class="nav-link" href=" """
    navitem_new = navitem_new_pre[:-1] + file + navitem_old_suf[1:]

    # create subdirectories if non-existent
    os.makedirs(os.path.dirname(compil_file), exist_ok=True)

    # convert markdown files if needed
    if file[-3:] == ".md":
        compil_file = compil_file.replace('.md', '.html')
        pypandoc.convert_file(source_file, 'html', outputfile=compil_file)
    else:
        shutil.copy(source_file, compil_file)
    print(source_file + ' -> ' + compil_file)

    fp = open(compil_file, 'r+')
    source = fp.read()

    # this rewrites href and src paths for files in subdirectories
    relative_path = "../" * file[:file.rfind("\\") + 1].count("\\")
    href_flag = """href=" """[:-1]
    src_flag = """src=" """[:-1]
    header_new = header.replace(href_flag + "css", href_flag + relative_path + "css")
    navgtn_new = navgtn.replace(href_flag, href_flag + relative_path).replace(src_flag, src_flag + relative_path)
    source_new = source.replace(href_flag, href_flag + relative_path).replace(src_flag, src_flag + relative_path)
    footer_new = footer.replace(src_flag, src_flag + relative_path)
    navgtn_new = navgtn_new.replace(navitem_old, navitem_new)

    # add blogpost header if page is a blog post
    if file[:file.find("\\")] == "blogposts":
        source_new = blog_header + source_new + blog_footer

    # write final page
    fp.seek(0)
    page = header_new + navgtn_new + source_new + footer_new
    fp.write(page)
    fp.close()
