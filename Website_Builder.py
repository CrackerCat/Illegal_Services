import re
import shutil
import textwrap
import datetime
import subprocess
from pathlib import Path
from urllib.parse import urlparse


def encode_unicode_encoding(string: str, type: str):
    if type == "path":
        replacements = {
            '\\\\': 'U+005C',
            '\\/': 'U+002F',
        }
    else:
        replacements = {
            '\\': 'U+005C',
            '/': 'U+002F',
        }
    replacements.update({
        ':': 'U+003A',
        '*': 'U+002A',
        '?': 'U+003F',
        '"': 'U+0022',
        '<': 'U+003C',
        '>': 'U+003E',
        '|': 'U+007C',
    })
    for chars, replacement in replacements.items():
        string = string.replace(chars, replacement)
    return string

def decode_unicode_encoding(string: str, type: str):
    if type == "path":
        replacements = {
            'U+005C': '\\\\',
            'U+002F': '\\/',
        }
    else:
        replacements = {
            'U+005C': '\\',
            'U+002F': '/',
        }
    replacements.update({
        'U+003A': ':',
        'U+002A': '*',
        'U+003F': '?',
        'U+0022': '"',
        'U+003C': '<',
        'U+003E': '>',
        'U+007C': '|',
    })
    for chars, replacement in replacements.items():
        string = string.replace(chars, replacement)
    return string

def encode_html_entity_encoding(string: str):
    replacements = {
        '&': '&amp;',
        '"': '&quot;',
        '\'': '&#39;',
        '<': '&lt;',
        '>': '&gt;',
        ' ': '&nbsp;',
    }
    for chars, replacement in replacements.items():
        string = string.replace(chars, replacement)
    return string

def decode_html_entity_encoding(string: str):
    replacements = {
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': '\'',
        '&lt;': '<',
        '&gt;': '>',
    }
    for chars, replacement in replacements.items():
        string = string.replace(chars, replacement)
    return string

def encode_url_encoding(string: str):
    replacements = {
        '%': '%25',
        ' ': '%20',
        '[': '%5B',
        ']': '%5D',
        '{': '%7B',
        '}': '%7D',
        '^': '%5E',
        '`': '%60',
        '#': '%23',
    }
    for chars, replacement in replacements.items():
        string = string.replace(chars, replacement)
    return string

def decode_url_encoding(string: str):
    replacements = {
        '%25': '%',
        '%20': ' ',
        '%5B': '[',
        '%5D': ']',
        '%7B': '{',
        '%7D': '}',
        '%5E': '^',
        '%60': '`',
        '%23': '#',
    }
    for chars, replacement in replacements.items():
        string = string.replace(chars, replacement)
    return string

def write_html_header() -> None:
    display_pathbar = _folder_path = ""
    for folder in bookmark_path__html_href_path.split("/"):
        if _folder_path:
            _folder_path += f"/{folder}"
        else:
            _folder_path = folder
        html_text = encode_html_entity_encoding(decode_url_encoding(decode_unicode_encoding(folder, "folder")))
        display_pathbar += f'<a href="/Illegal_Services/{_folder_path}/index.html">{html_text}</a> > '
    display_pathbar += "index.html"
    with open(bookmark_path__windows_index_path__str, "a+", encoding="utf-8", newline="\r\n") as file:
        text = f"""
            <!DOCTYPE html>
            <html lang="en-US">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <meta name="description" content="Illegal Services Bookmarks">
                <meta name="keywords" content="Illegal, Services, Bookmarks, website">
                <meta name="author" content="IB_U_Z_Z_A_R_Dl">
                <title class="notranslate">IS Bookmarks - Illegal Services</title>
                <link rel="shortcut icon" href="/Illegal_Services/icons/favicon.ico" type="image/x-icon">
                <link rel="icon" href="/Illegal_Services/icons/favicon.ico" type="image/x-icon">
                <link rel="stylesheet" href="/Illegal_Services/css/styles.css">
                <link rel="stylesheet" href="/Illegal_Services/css/is_bookmarks.css">
                <link rel="stylesheet" href="/Illegal_Services/plugins/font-awesome-4.7.0/css/font-awesome.min.css">
            </head>

            <body>
                <nav class="navbar">
                    <ul>
                        <li><a href="/Illegal_Services/index.html"><i class="fa fa-home"></i><span class="navbar-item-text">Home</span></a></li>
                        <li><a href="/Illegal_Services/credits.html"><i class="fa fa-handshake-o"></i><span class="navbar-item-text">Credits</span></a></li>
                        <li><a href="/Illegal_Services/tutorial.html"><i class="fa fa-life-ring"></i><span class="navbar-item-text">Tutorial</span></a></li>
                        <li><a href="/Illegal_Services/faq.html"><i class="fa fa-question-circle"></i><span class="navbar-item-text">FAQ</span></a></li>
                        <li><a href="/Illegal_Services/downloads.html"><i class="fa fa-cloud-download"></i><span class="navbar-item-text">Downloads</span></a></li>
                        <li class="navbar-item-active"><a href="/Illegal_Services/Bookmarks%20Toolbar/Illegal%20Services/index.html"><i class="fa fa-bookmark-o"></i><span class="navbar-item-text">IS Bookmarks</span></a></li>
                        <li><div id="google-translate-element"></div></li>
                    </ul>
                </nav>

                <div class="search-or-request-container">
                    <div class="search-or-request">
                        <h4>Search a link or folder in IS database:
                            <br>
                            <br>
                            <input type="text" name="search_link" id="search-link-input" placeholder="https://example.com/">
                            <button type="submit" id="search-link-button">Search</button>
                        </h4>
                    </div>
                    <div class="search-or-request">
                        <h4>Request a link to be added in IS database:
                            <br>
                            <br>
                            <input type="text" name="request_link" id="request-link-input" placeholder="https://example.com/">
                            <button type="submit" id="request-link-button">Request</button>
                        </h4>
                    </div>
                </div>

                <div class="pathbar notranslate">
                    {display_pathbar}
                </div>

                <div class="vertical-menu notranslate">
        """
        text = textwrap.dedent(text).removeprefix("\n")
        file.write(text)
        file.close()
    if not (bookmark_path__windows_index_path__path.exists() and bookmark_path__windows_index_path__path.is_file()):
        print(f'ERROR (write_html_header): "{bookmark_path__windows_index_path__path}"')
        input()
        exit(0)
    if not (bookmark_path__windows_path__path.exists() and bookmark_path__windows_path__path.is_dir()):
        print(f'ERROR (write_html_header): "{bookmark_path__windows_path__path}"')
        input()
        exit(0)

def write_footer() -> None:
    with open(windows_href_path__str, "a+", encoding="utf-8", newline="\r\n") as file:
        text = """
                </div>

                <div class="counter">
                    <script src="/Illegal_Services/js/counter.js"></script>
                    <noscript>
                        <div class="javascript-disabled">
                            <img src="/Illegal_Services/icons/no_js.png" alt="no_js.png">
                            JavaScript disabled in your browser;<br>
                            can't display the counter informations.
                        </div>
                    </noscript>
                </div>

                <div id="overlay-container">
                    <div id="overlay">
                        <button id="overlay-close-button">Close</button>
                        <div id="overlay-content">
                            <!-- JavaScript overlay content goes here -->
                        </div>
                    </div>
                </div>

                <footer>
                    <a href="https://illegal-services.github.io/Illegal_Services/" target="_blank"><img src="/Illegal_Services/svgs/internet.svg" alt="Website" title="https://illegal-services.github.io/Illegal_Services/"></a>
                    <a href="https://github.com/Illegal-Services/Illegal_Services" target="_blank"><img src="/Illegal_Services/svgs/github.svg" alt="GitHub" title="https://github.com/Illegal-Services/Illegal_Services"></a>
                    <a href="https://t.me/illegal_services_forum" target="_blank"><img src="/Illegal_Services/svgs/telegram.svg" alt="Telegram forum" title="https://t.me/illegal_services_forum"></a>
                    <a href="https://t.me/illegal_services" target="_blank"><img src="/Illegal_Services/svgs/telegram.svg" alt="Telegram channel" title="https://t.me/illegal_services"></a>
                    <br>
                    © 2020-2023 IB_U_Z_Z_A_R_Dl. All rights reserved.
                </footer>

                <script src="/Illegal_Services/js/translations.js"></script>
                <script src="/Illegal_Services/js/ISbookmarks.js" type="module"></script>
            </body>

            </html>
        """
        text = textwrap.dedent(text).removeprefix("\n")
        file.write(text)
        file.close()
    if not (windows_href_path__path.exists() and windows_href_path__path.is_file()):
        print(f'ERROR (write_footer): "{bookmark_folder__href}" "{bookmark_folder__text}"')
        input()
        exit(0)

def create_folder_or_path(folder_or_path: Path):
    if not (folder_or_path.exists() and folder_or_path.is_dir()):
        folder_or_path.mkdir(parents=False, exist_ok=False)
    if not (folder_or_path.exists() and folder_or_path.is_dir()):
        print(f'ERROR (create_folder_or_path): "{folder_or_path}"')
        input()
        exit(0)
    return folder_or_path


links_counter = 0

for file_or_folder in [Path(R"Bookmarks Toolbar"), Path(R"js/counter.js")]:
    if file_or_folder.exists():
        if file_or_folder.is_dir():
            shutil.rmtree(file_or_folder)
        elif file_or_folder.is_file():
            file_or_folder.unlink()
    if file_or_folder.exists():
        input()
        exit(0)

bookmarks_db = subprocess.check_output([
    R"D:\Git\Illegal_Services\bookmarks_parser.exe",
    "--extended-parsing",
    "--folders-path",
    "--quoting-style",
    "'",
    R"D:\Git\Illegal_Services\IS.bookmarks.html"
]).decode().splitlines(keepends=False)

is_first_folder__flag = False
for bookmark in bookmarks_db:
    parts = re.findall(r"'(.*?)'", bookmark)

    bookmark_type = str(parts[0])
    bookmark_depth = str(parts[1])
    bookmark_path = str(parts[2])

    #print(bookmark)
    #print(parts)

    if (
        bookmark_type == "PATH"
        and bookmark_depth == "0"
        and bookmark_path == ""
    ):
        is_first_folder__flag = True
        bookmark_path = str(parts[3])
    bookmark_path__windows_path__str = encode_unicode_encoding(decode_html_entity_encoding(bookmark_path), "path")
    bookmark_path__windows_path__path = Path(bookmark_path__windows_path__str)
    bookmark_path__windows_index_path__str = f"{bookmark_path__windows_path__str}/index.html"
    bookmark_path__windows_index_path__path = Path(bookmark_path__windows_index_path__str)
    bookmark_path__html_href_path = encode_url_encoding(decode_url_encoding(bookmark_path__windows_path__str))
    bookmark_path__html_href_text = encode_html_entity_encoding(bookmark_path__windows_path__str)
    if not (bookmark_path__windows_path__path.exists() and bookmark_path__windows_path__path.is_dir()):
        create_folder_or_path(bookmark_path__windows_path__path)
        write_html_header()
    if is_first_folder__flag is True:
        is_first_folder__flag = None
        continue

    if bookmark_type == "LINK":
        bookmark_link = str(parts[3])
        bookmark_link_title = str(parts[4])
        links_counter += 1
        bookmark_link_hostname = urlparse(bookmark_link).netloc
        bookmark_link_title__text = encode_html_entity_encoding(decode_html_entity_encoding(bookmark_link_title))

        match = re.search(r"^(.*)( \| \(untrusted(?:\: .*))$", bookmark_link_title)
        if match:
            bookmark_link_title__html_text = f'{match.group(1)}<span style="color: #ff0000">{match.group(2)}</span>'
        else:
            bookmark_link_title__html_text = bookmark_link_title__text

        with open(bookmark_path__windows_index_path__str, "a+", encoding="utf-8", newline="\r\n") as file:
            file.write(f'            <a href="{bookmark_link}" target="_blank" title="{bookmark_link}"><img src="https://external-content.duckduckgo.com/ip3/{bookmark_link_hostname}.ico" alt="favicon">{bookmark_link_title__html_text}</a>\n')
            file.close()
        if not (bookmark_path__windows_index_path__path.exists() and bookmark_path__windows_index_path__path.is_file()):
            print(f'ERROR (WRITE_LINK_INDEX): "{bookmark_link}" "{bookmark_folder__text}" "{bookmark_link_title__text}"')
            input()
            exit(0)

    elif bookmark_type == "PATH":
        bookmark_folder = str(parts[3])
        bookmark_folder__href = f"{encode_url_encoding(encode_unicode_encoding(decode_html_entity_encoding(bookmark_folder), 'folder'))}/index.html"
        bookmark_folder__text = encode_html_entity_encoding(decode_html_entity_encoding(bookmark_folder))
        with open(bookmark_path__windows_index_path__str, "a+", encoding="utf-8", newline="\r\n") as file:
            file.write(f'            <a href="{bookmark_folder__href}"><i class="fa fa-folder-o"></i>{bookmark_folder__text}</a>\n')
            file.close()
        if not (bookmark_path__windows_index_path__path.exists() and bookmark_path__windows_index_path__path.is_file()):
            print(f'ERROR (WRITE_PATH_INDEX): "{bookmark_folder__href}" "{bookmark_folder__text}"')
            input()
            exit(0)

    elif bookmark_type == "HR":
        with open(bookmark_path__windows_index_path__str, "a+", encoding="utf-8", newline="\r\n") as file:
            file.write("            <hr>\n")
            file.close()
        if not (bookmark_path__windows_index_path__path.exists() and bookmark_path__windows_index_path__path.is_file()):
            print(f'ERROR (WRITE_HR_INDEX): "{bookmark_path__windows_index_path__str}"')
            input()
            exit(0)
    else:
        print(True)
        input()
        exit(0)

folder_path = Path(R"Bookmarks Toolbar")
for file_path in folder_path.glob("**/*.html"):
    if not (file_path.exists() and file_path.is_file()):
        continue

    windows_href_path__path = file_path
    windows_href_path__str = str(file_path)
    if windows_href_path__str:
        write_footer()

js_conter__path = Path(R"js/counter.js")
create_folder_or_path(js_conter__path.parent.resolve())
with open(R"js/counter.js", "w", encoding="utf-8") as file:
    file.write(f'document.write("Updated: {datetime.date.today().strftime("%d/%m/%Y")}&nbsp;&nbsp;|&nbsp;&nbsp;{links_counter} links indexed.")')
    file.close()
if not (js_conter__path.exists() and js_conter__path.is_file()):
    print(f'ERROR (write_js_conter): "{bookmark_path__windows_index_path__path}"')
    input()
    exit(0)

exit(0)
