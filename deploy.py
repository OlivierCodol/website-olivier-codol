
# http://localhost:63342/website-olivier-codol/docs/index.html
import os
import shutil
import datetime
import copy


# function to get file content
def readfile(filename):
    pointer = open(filename, 'r')
    content = pointer.read()
    pointer.close()
    return content


# find a snippet between a start landmark and an end landmark
def find_content_snippet(content, start_snippet, end_snippet):
    start_pos = content.find(start_snippet) + len(start_snippet)
    truncated_content = content[start_pos:]
    relative_end_pos = truncated_content.find(end_snippet)
    end_pos = relative_end_pos + start_pos
    content_snippet = content[start_pos:end_pos]
    if content.find(start_snippet) == -1:
        content_snippet = ""
    return content_snippet


# get directory paths
script_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(script_dir, 'src')
compil_dir = os.path.join(script_dir, 'docs')
template_dir = os.path.join(script_dir, 'template')


##########################
# BLOG LIST CREATION
##########################


files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(src_dir + "\\blogposts")) for f in fn]
ix = len(src_dir) + 1

bloglist = readfile(template_dir + '/bloglist-header.html')
bloglist_entry = readfile(template_dir + '/bloglist-entry.html')

for source_file in files:

    # find post title, creation and modification date, and relative path
    blog_content = readfile(source_file)
    title = find_content_snippet(blog_content, """ id="blogpost-title">""", "<")
    mtime = find_content_snippet(blog_content, """Posted on """, ".")
    ctime = find_content_snippet(blog_content, """Last modified on """, ".")
    if mtime:
        mtime = "posted on " + str(datetime.datetime.strptime(mtime, "%A %d %B %Y").date())
    if ctime:
        ctime = "last modified on " + str(datetime.datetime.strptime(ctime, "%A %d %B %Y").date())
    rel_path = source_file[ix:]

    bloglist_entry_new = copy.deepcopy(bloglist_entry)
    bloglist_entry_new = bloglist_entry_new.replace("insert-path-here", rel_path)
    bloglist_entry_new = bloglist_entry_new.replace("insert-title-here", title)
    bloglist_entry_new = bloglist_entry_new.replace("posted on insert-creation-date-here", mtime)
    bloglist_entry_new = bloglist_entry_new.replace("last modified on insert-modification-date-here", ctime)

    # create entry
    bloglist = bloglist + bloglist_entry_new

# add footer
bloglist = bloglist + readfile(template_dir + '/bloglist-footer.html')

# write final page
fp = open(src_dir + "\\blog.html", 'r+')
fp.truncate(0)  # erase all previous content
fp.seek(0)
fp.write(bloglist)
fp.close()

##########################
# END OF BLOG LIST CREATION
##########################


##########################
# FULL WEBSITE CREATION
##########################


# get template (static) contents
header = readfile(template_dir + '/header.html')
navgtn = readfile(template_dir + '/navigation.html')
footer = readfile(template_dir + '/footer.html')
blog_header = readfile(template_dir + '/blogpost-header.html')
blog_footer = readfile(template_dir + '/blogpost-footer.html')


# get list of files to compile
files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(src_dir)) for f in fn]
ix = len(src_dir) + 1


for source_file in files:

    file = source_file[ix:]
    if file == "index-content.html":
        file = "index.html"
    compil_file = os.path.join(compil_dir, file)

    # this highlights the navigation tab on the corresponding page
    navitem_old_not = """li class="nav-item not-selected"><a class="nav-link" href=" """[:-1]
    navitem_old_pre = """li class="nav-item"><a class="nav-link" href=" """[:-1]
    navitem_old_suf = """ " data-no="1">"""[1:]
    navitem_old = navitem_old_pre + file + navitem_old_suf
    navitem_new_pre = """li class="nav-item selected"><a class="nav-link" href=" """[:-1]
    navitem_new = navitem_new_pre + file + navitem_old_suf

    # create subdirectories if non-existent
    os.makedirs(os.path.dirname(compil_file), exist_ok=True)
    shutil.copy(source_file, compil_file)
    print(source_file + ' -> ' + compil_file)

    fp = open(compil_file, 'r+')
    source = fp.read()

    # this rewrites href and src paths for files in subdirectories
    relative_path = "../" * file.count("\\")
    href_flag = """href=" """[:-1]
    src_flag = """src=" """[:-1]
    navgtn_new = navgtn.replace(navitem_old, navitem_new)
    navgtn_new = navgtn_new.replace(navitem_old_pre, navitem_old_not)
    header_new = header.replace(href_flag + "css", href_flag + relative_path + "css")
    navgtn_new = navgtn_new.replace(href_flag, href_flag + relative_path).replace(src_flag, src_flag + relative_path)
    source_new = source.replace(src_flag, src_flag + relative_path)
    footer_new = footer.replace(src_flag, src_flag + relative_path)

    # add blogpost header if page is a blog post
    if file[:file.find("\\")] == "blogposts":
        source_new = blog_header + source_new + blog_footer

    # write final page
    fp.seek(0)
    page = header_new + navgtn_new + source_new + footer_new
    fp.write(page)
    fp.close()

##########################
# ENF OF FULL WEBSITE CREATION
##########################
