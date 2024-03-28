# --------------------
# 🐍 Standard Python Libraries (Included by Default) 🐍
# These modules are part of the Python standard library and don't require additional installation.
# --------------------
import re
import sys
import shutil
import textwrap
import datetime
import subprocess
from pathlib import Path
from urllib.parse import urlparse


BOOKMARKS_TOOLBAR_PATH = Path("Bookmarks Toolbar")
JS_COUNTER_PATH = Path("js/counter.js")


def error(message: str):
    print(message, end="")
    input()
    sys.exit(1)


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
        display_pathbar += f'<a href="/Illegal_Services/{_folder_path}/index.html">{html_text}</a> &gt; '
    display_pathbar += "index.html"
    with bookmark_index_path__windows_path.open("a+", encoding="utf-8") as file:
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
                        <div class="h4-simulation">Search a link or folder in IS database:
                            <br>
                            <br>
                            <div class="input-container">
                                <input type="text" name="search_link" class="clearable-input" id="search-link-input" placeholder="https://example.com/">
                                <span class="clear-button" id="clear-search-link-input">&times;</span>
                            </div>
                            <button type="submit" id="search-link-button">Search</button>
                            <button type="button" id="search-link-history-button">
                                <i class="fa fa-history" aria-hidden="true"></i>
                            </button>
                        </div>
                    </div>
                    <div class="search-or-request">
                        <div class="h4-simulation">Request a link to be added in IS database:
                            <br>
                            <br>
                            <div class="input-container">
                                <input type="text" name="request_link" class="clearable-input" id="request-link-input" placeholder="https://example.com/">
                                <span class="clear-button" id="clear-request-link-input">&times;</span>
                            </div>
                            <button type="submit" id="request-link-button">Request</button>
                            <button type="button" id="request-link-history-button">
                                <i class="fa fa-history" aria-hidden="true"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <div class="pathbar notranslate">
                    {display_pathbar}
                </div>

                <div class="vertical-menu notranslate">
        """
        text = textwrap.dedent(text).removeprefix("\n")
        file.write(text)
    if not bookmark_index_path__windows_path.is_file():
        error(f'ERROR (write_html_header): "{bookmark_index_path__windows_path}"')


def write_html_footer(path: Path):
    with path.open("a+", encoding="utf-8") as file:
        text = """
                </div>

                <div class="counter">
                    <span id="counter-text">
                        <!-- JavaScript counter text goes here -->
                    </span>
                    <script src="/Illegal_Services/js/counter.js"></script>
                    <noscript>
                        <div class="javascript-disabled">
                            <img src="/Illegal_Services/icons/no_js.png" alt="no_js.png">
                            JavaScript disabled in your browser;<br>
                            can't display the counter informations.
                        </div>
                    </noscript>
                </div>

                <div class="visitors-counter">
                    <span id="visitors-counter-text">
                        <!-- JavaScript visitors counter text goes here -->
                    </span>
                    <script src="/Illegal_Services/js/visitors.js" type="module"></script>
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
                        <button type="button" id="overlay-close-button">Close</button>
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
                    © 2020-2024 IB_U_Z_Z_A_R_Dl. All rights reserved.
                </footer>

                <script src="/Illegal_Services/js/translations.js"></script>
                <script src="/Illegal_Services/js/ISbookmarks.js" type="module"></script>
            </body>

            </html>
        """
        text = textwrap.dedent(text).removeprefix("\n")
        file.write(text)
    if not path.is_file():
        error(f'ERROR (write_footer): "{bookmark_folder__href}" "{bookmark_folder__text}"')


def create_folder_or_path(folder_or_path: Path):
    if not folder_or_path.is_dir():
        folder_or_path.mkdir(parents=False, exist_ok=False)
    if not folder_or_path.is_dir():
        error(f'ERROR (create_folder_or_path): "{folder_or_path}"')
    return folder_or_path


links_counter = 0

for path in [BOOKMARKS_TOOLBAR_PATH, JS_COUNTER_PATH]:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()
    if path.exists():
        error(f'ERROR (shutil.rmtree()): "{path}"')

bookmarks_db = subprocess.check_output([
    Path("D:/Git/Illegal_Services/bookmarks_parser.exe"),
    "--extended-parsing",
    "--folders-path",
    "--quoting-style",
    "'",
    Path("D:/Git/Illegal_Services/GitHub/IS.bookmarks.html")
]).decode().splitlines(keepends=False)

is_first_folder__flag = False
for bookmark in bookmarks_db:
    parts = re.findall(r"'(.*?)'", bookmark)

    bookmark_type: str = parts[0]
    bookmark_depth: str = parts[1]
    bookmark_path: str = parts[2]

    #print(bookmark)
    #print(parts)

    if (
        bookmark_type == "PATH"
        and bookmark_depth == "0"
        and bookmark_path == ""
    ):
        is_first_folder__flag = True
        bookmark_path: str = parts[3]

    bookmark_path__unicode_encoded = encode_unicode_encoding(decode_html_entity_encoding(bookmark_path), "path")
    bookmark_path__windows_path = Path(bookmark_path__unicode_encoded)
    bookmark_index_path__windows_path = bookmark_path__windows_path / "index.html"

    bookmark_path__html_href_path = encode_url_encoding(decode_url_encoding(bookmark_path__unicode_encoded))
    bookmark_path__html_href_text = encode_html_entity_encoding(bookmark_path__unicode_encoded)
    if not bookmark_path__windows_path.is_dir():
        create_folder_or_path(bookmark_path__windows_path)
        write_html_header()
    if is_first_folder__flag is True:
        is_first_folder__flag = None
        continue

    if bookmark_type == "LINK":
        bookmark_link: str = parts[3]
        bookmark_link_title: str = parts[4]
        links_counter += 1
        bookmark_link_hostname = urlparse(bookmark_link).netloc
        bookmark_link_title__text = encode_html_entity_encoding(decode_html_entity_encoding(bookmark_link_title))

        match = re.search(r"^(.*)( \| \(untrusted(?:\: .*))$", bookmark_link_title)
        if match:
            bookmark_link_title__html_text = f'{match.group(1)}<span style="color: #ff0000">{match.group(2)}</span>'
        else:
            bookmark_link_title__html_text = bookmark_link_title__text

        with bookmark_index_path__windows_path.open("a+", encoding="utf-8") as file:
            file.write(f'            <a href="{bookmark_link}" target="_blank" title="{bookmark_link}"><img src="https://external-content.duckduckgo.com/ip3/{bookmark_link_hostname}.ico" alt="🌐">{bookmark_link_title__html_text}</a>\n')
        if not bookmark_index_path__windows_path.is_file():
            error(f'ERROR (WRITE_LINK_INDEX): "{bookmark_link}" "{bookmark_folder__text}" "{bookmark_link_title__text}"')

    elif bookmark_type == "PATH":
        bookmark_folder: str = parts[3]
        bookmark_folder__href = f"{encode_url_encoding(encode_unicode_encoding(decode_html_entity_encoding(bookmark_folder), 'folder'))}/index.html"
        bookmark_folder__text = encode_html_entity_encoding(decode_html_entity_encoding(bookmark_folder))
        with bookmark_index_path__windows_path.open("a+", encoding="utf-8") as file:
            file.write(f'            <a href="{bookmark_folder__href}"><i class="fa fa-folder-o"></i>{bookmark_folder__text}</a>\n')
        if not bookmark_index_path__windows_path.is_file():
            error(f'ERROR (WRITE_PATH_INDEX): "{bookmark_folder__href}" "{bookmark_folder__text}"')

    elif bookmark_type == "HR":
        with bookmark_index_path__windows_path.open("a+", encoding="utf-8") as file:
            file.write("            <hr>\n")
        if not bookmark_index_path__windows_path.is_file():
            error(f'ERROR (WRITE_HR_INDEX): "{bookmark_index_path__windows_path}"')
    else:
        error(f'ERROR (else:): "not LINK or PATH or HR"')

for path in BOOKMARKS_TOOLBAR_PATH.glob("**/*.html"):
    if not path.is_file():
        continue

    write_html_footer(path)

create_folder_or_path(JS_COUNTER_PATH.parent.resolve())
with JS_COUNTER_PATH.open("w", encoding="utf-8") as file:
    text = f"""
        document.addEventListener("DOMContentLoaded", function() {{
          const counterText = document.getElementById("counter-text");

          if (counterText) {{
            counterText.textContent = "Updated: {datetime.date.today().strftime("%d/%m/%Y")}  |  {links_counter} links indexed.";
          }}
        }});
    """
    text = textwrap.dedent(text).removeprefix("\n")
    file.write(text)
if not JS_COUNTER_PATH.is_file():
    error(f'ERROR (write_js_conter): "{JS_COUNTER_PATH}"')

sys.exit(0)
