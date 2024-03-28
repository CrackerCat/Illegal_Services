import "/Illegal_Services/plugins/DOMPurify-3.0.9/purify.min.js";
import { makeWebRequest } from "/Illegal_Services/js/makeWebRequest.js";

document.addEventListener("DOMContentLoaded", function () {
  const htmlSearchLinkInput = document.getElementById("search-link-input");
  const htmlSearchLinkButton = document.getElementById("search-link-button");
  const htmlSearchLinkHistoryButton = document.getElementById("search-link-history-button");
  const htmlRequestLinkInput = document.getElementById("request-link-input");
  const htmlRequestLinkButton = document.getElementById("request-link-button");
  const htmlRequestLinkHistoryButton = document.getElementById("request-link-history-button");
  const htmlClearSearchLinkInput = document.getElementById("clear-search-link-input");
  const htmlClearRequestLinkInput = document.getElementById("clear-request-link-input");
  const htmlOverlayContainer = document.getElementById("overlay-container");
  const htmlOverlayContent = document.getElementById("overlay-content");
  const htmlOverlayCloseButton = document.getElementById("overlay-close-button");

  let bookmarkDb;
  let previous_request;
  let isOverlayActive = false;

  let searchHistory = [];
  const searchHistoryCookie = getCookie("searchHistory");
  if (searchHistoryCookie === null) {
    searchHistory = [];
  } else {
    searchHistory = JSON.parse(searchHistoryCookie);
  }

  let requestHistory = [];
  const RequestHistoryCookie = getCookie("requestHistory");
  if (RequestHistoryCookie === null) {
    requestHistory = [];
  } else {
    requestHistory = JSON.parse(RequestHistoryCookie);
  }

  // Search or Request Event Listeners, it's a *bit* messy here lol
  htmlSearchLinkInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      htmlSearchLinkInput.blur();
      initializeSearchOrRequestLink("Search");
    }
  });
  htmlRequestLinkInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      htmlRequestLinkInput.blur();
      initializeSearchOrRequestLink("Request");
    }
  });
  htmlSearchLinkButton.addEventListener("click", () => {
    initializeSearchOrRequestLink("Search");
  });
  htmlRequestLinkButton.addEventListener("click", () => {
    initializeSearchOrRequestLink("Request");
  });

  htmlSearchLinkHistoryButton.addEventListener("click", () => {
    initializeSearchOrRequestLinkHistory("Search");
  });
  htmlRequestLinkHistoryButton.addEventListener("click", () => {
    initializeSearchOrRequestLinkHistory("Request");
  });

  htmlOverlayCloseButton.addEventListener("click", () => {
    hideOverlay();
  });
  // Close the overlay when clicking outside of the content area
  htmlOverlayContainer.addEventListener("click", (event) => {
    if (event.target === htmlOverlayContainer) {
      hideOverlay();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      hideOverlay();
    }
  });

  // Clear input Event Listeners stuff
  document.addEventListener("mousemove", function (event) {
    function checkAndToggleClearButton(inputElement, clearButton) {
      if (isMouseInside(inputElement, event)) {
        clearButton.style.display = inputElement.value === "" ? "none" : "block";
      } else {
        if (document.activeElement !== inputElement) {
          clearButton.style.display = "none";
        }
      }
    }

    checkAndToggleClearButton(htmlSearchLinkInput, htmlClearSearchLinkInput);
    checkAndToggleClearButton(htmlRequestLinkInput, htmlClearRequestLinkInput);
  });

  htmlSearchLinkInput.addEventListener("input", () => {
    htmlClearSearchLinkInput.style.display = htmlSearchLinkInput.value === "" ? "none" : "block";
  });
  htmlRequestLinkInput.addEventListener("input", () => {
    htmlClearRequestLinkInput.style.display = htmlRequestLinkInput.value === "" ? "none" : "block";
  });

  htmlSearchLinkInput.addEventListener("focusin", () => {
    htmlClearSearchLinkInput.style.display = htmlSearchLinkInput.value === "" ? "none" : "block";
  });
  htmlRequestLinkInput.addEventListener("focusin", () => {
    htmlClearRequestLinkInput.style.display = htmlRequestLinkInput.value === "" ? "none" : "block";
  });

  htmlSearchLinkInput.addEventListener("focusout", () => {
    htmlClearSearchLinkInput.style.display = "none";
  });
  htmlRequestLinkInput.addEventListener("focusout", () => {
    htmlClearRequestLinkInput.style.display = "none";
  });

  htmlClearSearchLinkInput.addEventListener("mousedown", () => {
    htmlSearchLinkInput.value = "";
    htmlSearchLinkInput.focus();
  });
  htmlClearRequestLinkInput.addEventListener("mousedown", () => {
    htmlRequestLinkInput.value = "";
    htmlRequestLinkInput.focus();
  });

  // Add an event listener that captures the Ctrl+A of only the overlay, when active.
  document.addEventListener("keydown", (event) => {
    if (isOverlayActive && event.ctrlKey && event.key === "a") {
      event.preventDefault(); // Prevent the default behavior of Ctrl+A

      // Create a range and select the content within the htmlOverlayContent element
      const range = document.createRange();
      range.selectNode(htmlOverlayContent);

      // Clear any existing selections
      window.getSelection().removeAllRanges();

      // Add the new range to the selection
      window.getSelection().addRange(range);
    }
  });

  function showOverlay() {
    isOverlayActive = true;
    htmlOverlayContainer.style.display = "flex";
    document.body.style.overflow = "hidden"; // Prevent scrolling on the background
  }

  function hideOverlay() {
    isOverlayActive = false;
    htmlOverlayContainer.style.display = "none";
    document.body.style.overflow = "auto"; // Allow scrolling on the background
    htmlOverlayContent.innerHTML = `
                <!-- JavaScript overlay content goes here -->
            `;
  }

  /**
   * @param {string} type
   */
  async function initializeSearchOrRequestLink(type) {
    if (!bookmarkDb) {
      bookmarkDb = fetchISdatabase();
    }

    const timestamp = getCurrentTime();

    if (type === "Search") {
      const formattedUserSearch = await handleSearchLink(bookmarkDb);
      searchHistory.push({ time: timestamp, search: formattedUserSearch.replace(";", "U+003B") });
      document.cookie = `searchHistory=${JSON.stringify(searchHistory)}; path=/Illegal_Services/Bookmarks%20Toolbar/; samesite=Strict; Secure`;
    } else if (type === "Request") {
      const [formattedUserRequest, status] = await handleRequestLink(bookmarkDb);
      requestHistory.push({ time: timestamp, status: status, request: formattedUserRequest.replace(";", "U+003B") });
      document.cookie = `requestHistory=${JSON.stringify(requestHistory)}; path=/Illegal_Services/Bookmarks%20Toolbar/; samesite=Strict; Secure`;
    }
  }

  /**
   * @param {string} type
   */
  function initializeSearchOrRequestLinkHistory(type) {
    if (type === "Search") {
      handleSearchLinkHistory();
    } else if (type === "Request") {
      handleRequestLinkHistory();
    }
  }

  function handleSearchLinkHistory() {
    let htmlOutput = "";
    htmlOutput += `
                <div class="search-or-request-history">
                    <h1>Search History</h2>`;
    if (searchHistory.length == 0) {
      htmlOutput += `
                    <h4>⚠️ You haven't searched for anything yet.</h4>`;
    } else {
      htmlOutput += `
                    <ul>`;
      for (let i = 0; i < searchHistory.length; i++) {
        const itemId = i + 1;
        htmlOutput += `
                        <li><span id="formatted-user-search-${itemId}"></span></li>`;
      }
      htmlOutput += `
                    </ul>`;
    }
    htmlOutput += `
                </div>
            </div>`;

    showOverlay();
    htmlOverlayContent.innerHTML = htmlOutput;

    for (let i = 0; i < searchHistory.length; i++) {
      const itemId = i + 1;
      const elementId = `formatted-user-search-${itemId}`;
      const element = document.getElementById(elementId);

      if (element) {
        element.textContent = `[${searchHistory[i].time}] - "${searchHistory[i].search.replace("U+003B", ";")}"`;
      }
    }
  }

  function handleRequestLinkHistory() {
    let htmlOutput = "";
    htmlOutput += `
                <div class="search-or-request-history">
                    <h1>Request History</h2>`;
    if (requestHistory.length == 0) {
      htmlOutput += `
                    <h4>⚠️ You haven't sent any request yet.</h4>`;
    } else {
      htmlOutput += `
                    <ul>`;
      for (let i = 0; i < requestHistory.length; i++) {
        const itemId = i + 1;
        htmlOutput += `
                        <li><span id="formatted-user-request-${itemId}"></span></li>`;
      }
      htmlOutput += `
                    </ul>`;
    }
    htmlOutput += `
                </div>
            </div>`;

    showOverlay();
    htmlOverlayContent.innerHTML = htmlOutput;

    for (let i = 0; i < requestHistory.length; i++) {
      const itemId = i + 1;
      const elementId = `formatted-user-request-${itemId}`;
      const element = document.getElementById(elementId);

      if (element) {
        element.textContent = `[${requestHistory[i].time} (${requestHistory[i].status})] - "${requestHistory[i].request.replace("U+003B", ";")}"`;
      }
    }
  }

  /**
   * @param {Promise<Array>} bookmarkDb
   */
  async function handleSearchLink(bookmarkDb) {
    const formattedUserSearch = sanitizeString(htmlSearchLinkInput.value.trim());
    const formattedUserSearchLowerCase = formattedUserSearch.toLowerCase();
    const isXssAttack = Boolean(DOMPurify.removed.length);

    const foldersResults = [];
    const linksResults = [];

    let htmlOutput = "";

    if (isXssAttack) {
      //console.log(DOMPurify.removed);
      htmlOutput += `
                <hr>
                <h1>
                    Nice try, hacker!
                    <br>
                    🕵️ Keep sprinkling your magic XSS dust, but this website's got a shield! 🛡️
                    <br>
                    😄😘😘
                </h1>
                <hr>`;
    } else {
      await processDatabase(bookmarkDb, (entry) => {
        if (entry.type === "FOLDER") {
          if (entry.title.toLowerCase().includes(formattedUserSearchLowerCase)) {
            foldersResults.push({
              path: formatPathLink(entry.path.slice(0, -1)),
              title: encodeHtmlEntityEncoding(entry.title),
            });
          }
        } else if (entry.type === "LINK") {
          if (entry.title.toLowerCase().includes(formattedUserSearchLowerCase) || entry.url.toLowerCase().includes(formattedUserSearchLowerCase)) {
            linksResults.push({
              path: formatPathLink(entry.path),
              title: encodeHtmlEntityEncoding(entry.title),
              url: formatLink(entry.url),
            });
          }
        }
      });

      if (foldersResults.length === 0 && linksResults.length === 0) {
        htmlOutput += `
                <hr>
                <h1>Search: "<span id="formatted-user-search"></span>" is not indexed in IS database.</h1>
                <hr>`;
      } else {
        htmlOutput = `
                <hr>
                <h1>Search: "<span id="formatted-user-search"></span>" was found indexed in IS database, in location(s):</h1>
                <hr>
                <br>`;
      }

      if (foldersResults.length !== 0) {
        htmlOutput += `
                <table>
                    <tbody>
                        <tr>
                            <th>HREF</th>
                            <th>NAME</th>
                        </tr>`;
        for (const entry of foldersResults) {
          htmlOutput += `
                        <tr>
                            <td>${entry.path}</td>
                            <td>${entry.title}</td>
                        </tr>`;
        }
        htmlOutput += `
                    </tbody>
                </table>`;
        if (linksResults.length !== 0) {
          htmlOutput += `
                <br>`;
        }
      }

      if (linksResults.length !== 0) {
        htmlOutput += `
                <table>
                    <tbody>
                        <tr>
                            <th>HREF</th>
                            <th>LINK</th>
                            <th>NAME</th>
                        </tr>`;
        for (const entry of linksResults) {
          htmlOutput += `
                        <tr>
                            <td>${entry.path}</td>
                            <td>${entry.url}</td>
                            <td>${entry.title}</td>
                        </tr>`;
        }
        htmlOutput += `
                    </tbody>
                </table>
            `;
      }
    }

    showOverlay();
    htmlOverlayContent.innerHTML = htmlOutput;

    if (!isXssAttack) {
      const element = document.getElementById("formatted-user-search");
      if (element) {
        element.textContent = formattedUserSearch;
      }
    }

    return formattedUserSearch;
  }

  /**
   * @param {Promise<Array>} bookmarkDb
   */
  async function handleRequestLink(bookmarkDb) {
    const formattedUserRequest = sanitizeString(htmlRequestLinkInput.value.trim());
    const formattedUserRequestLowerCase = formattedUserRequest.toLowerCase();
    const formattedUserRequestLink = encodeUrlEncoding(decodeUrlEncoding(formatUserInputToURL(formattedUserRequest)));
    const isXssAttack = Boolean(DOMPurify.removed.length);

    const linksMatchResults = [];
    const linksContainsResults = [];

    let htmlOutput = "";

    if (isXssAttack) {
      //console.log(DOMPurify.removed);
      htmlOutput += `
                <hr>
                <h1>
                    Nice try, hacker!
                    <br>
                    🕵️ Keep sprinkling your magic XSS dust, but this website's got a shield! 🛡️
                    <br>
                    😄😘😘
                </h1>
                <hr>`;
    } else {
      await processDatabase(bookmarkDb, (entry) => {
        if (entry.type === "LINK") {
          if (entry.url.toLowerCase().includes(formattedUserRequestLowerCase)) {
            if (entry.url.toLowerCase() === formattedUserRequestLowerCase) {
              linksMatchResults.push({
                path: formatPathLink(entry.path),
                title: encodeHtmlEntityEncoding(entry.title),
                url: formatLink(entry.url),
              });
            } else {
              linksContainsResults.push({
                path: formatPathLink(entry.path),
                title: encodeHtmlEntityEncoding(entry.title),
                url: formatLink(entry.url),
              });
            }
          }
        }
      });

      htmlOutput += `
                <h1>
                    <hr>
                    Thank you for contributing to IS database!
                    <br>
                    We will manually review your request as soon as possible.
                    <br>
                    <hr>
                </h1>`;

      if (linksMatchResults.length === 0 && linksContainsResults.length === 0) {
        // REMINDER: XSS injection is not possible inside an 'href' attribute.
        htmlOutput += `
                <div class="indexed-or-not">
                    Link: "<a href="${formattedUserRequestLink}"><span id="formatted-user-request-1"></span></a>" was not indexed in IS database.
                </div>`;
      } else {
        if (linksMatchResults.length > 0) {
          // REMINDER: XSS injection is not possible inside an 'href' attribute.
          htmlOutput += `
                <div class="indexed-or-not">
                    Link: "<a href="${formattedUserRequestLink}"><span id="formatted-user-request-2"></span></a>" was already indexed in IS database, in location(s):
                </div>
                <br>
                <table>
                    <tbody>
                        <tr>
                            <th>HREF</th>
                            <th>LINK</th>
                            <th>NAME</th>
                        </tr>`;
          for (const entry of linksMatchResults) {
            htmlOutput += `
                        <tr>
                            <td>${entry.path}</td>
                            <td>${entry.url}</td>
                            <td>${entry.title}</td>
                        </tr>`;
          }
          htmlOutput += `
                    </tbody>
                </table>`;
          if (linksContainsResults.length !== 0) {
            htmlOutput += `
                <br>`;
          }
        }

        if (linksContainsResults.length > 0) {
          // REMINDER: XSS injection is not possible inside an 'href' attribute.
          htmlOutput += `
                <div class="indexed-or-not">
                    Link: "<a href="${formattedUserRequestLink}"><span id="formatted-user-request-3"></span></a>" was also found indexed in IS database, in location(s):
                </div>
                <br>
                <table>
                    <tbody>
                        <tr>
                            <th>HREF</th>
                            <th>LINK</th>
                            <th>NAME</th>
                        </tr>`;
          for (const entry of linksContainsResults) {
            htmlOutput += `
                        <tr>
                            <td>${entry.path}</td>
                            <td>${entry.url}</td>
                            <td>${entry.title}</td>
                        </tr>`;
          }
          htmlOutput += `
                    </tbody>
                </table>
            `;
        }
      }
    }

    showOverlay();
    htmlOverlayContent.innerHTML = htmlOutput;

    if (!isXssAttack) {
      const elementIds = ["formatted-user-request-1", "formatted-user-request-2", "formatted-user-request-3"];
      elementIds.forEach((elementId) => {
        const element = document.getElementById(elementId);
        if (element) {
          element.textContent = formattedUserRequest;
        }
      });
    }

    if (previous_request === formattedUserRequestLowerCase) {
      return [formattedUserRequest, "ERROR: ALREADY_SENT_BEFORE"];
    }

    if (formattedUserRequestLowerCase === "") {
      return [formattedUserRequest, "ERROR: EMPTY_REQUEST"];
    }

    // The output displays the request along with it, so we should normally divide its value by 2.
    // BUT the user input starts glitching at precisely 159912 on Firefox and at approximately 33050 on Brave.
    // So to ensure consistency, I've reduced it down to 30000.
    if (formattedUserRequestLowerCase.length > 30000) {
      return [formattedUserRequest, "ERROR: REQUEST_USER_INPUT_EXCEEDS_MAX_CHARACTER_LIMIT"];
    }

    // I've figured that the Pipedream maximum's html body limit is set to 261873
    if (htmlOverlayContent.outerHTML.length > 261873) {
      return [formattedUserRequest, "ERROR: REQUEST_OUTPUT_EXCEEDS_MAX_CHARACTER_LIMIT"];
    }

    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    // TODO: 'formattedUserRequestLink' would be nice to investigate that later (can't see the link requested on xss attack page)
    const body = {
      html: htmlOverlayContent.outerHTML, // TODO: inject css in .outerHTML
    };

    const requestOptions = {
      method: "POST",
      headers,
      mode: "cors",
      body: JSON.stringify(body),
    };

    const response = await makeWebRequest("https://eowgt2c6txqik7b.m.pipedream.net", requestOptions);
    if (response.ok) {
      previous_request = formattedUserRequestLowerCase;
      return [formattedUserRequest, "SENT"];
    } else {
      return [formattedUserRequest, "ERROR: NETWORK_ERROR"];
    }
  }
});

/**
 * @param {object} element
 * @param {object} event
 */
function isMouseInside(element, event) {
  const rect = element.getBoundingClientRect();

  // prettier-ignore
  return (
    event.clientX >= rect.left &&
    event.clientX <= rect.right &&
    event.clientY >= rect.top &&
    event.clientY <= rect.bottom
  );
}

/**
 * Set the IS bookmarks database in an array.
 * @throws {error}
 */
async function fetchISdatabase() {
  const urlRawISDatabase = "/Illegal_Services/IS.bookmarks.json";

  const responseRawISDatabase = await makeWebRequest(urlRawISDatabase);
  if (!isResponseUp(responseRawISDatabase)) {
    throw new Error("Failed to retrieve the IS database.");
  }
  const responseText = (await responseRawISDatabase.text()).trim();
  const bookmarkDb = JSON.parse(responseText);

  if (
    // prettier-ignore
    !Array.isArray(bookmarkDb)
    || JSON.stringify(bookmarkDb[0]) !== '["FOLDER",0,"Bookmarks Toolbar"]'
  ) {
    throw new Error("Invalid bookmark database.");
  }

  return bookmarkDb;
}

/**
 * Function that parses the bookmark database and log each entries in a callback.
 * @param {Promise<Array>} bookmarkDb - The database that contains all the bookmarks to be created.
 * @param {Function} callback - The callback function to process each entry.
 */
async function processDatabase(bookmarkDb, callback) {
  bookmarkDb = await bookmarkDb;

  const path = [];

  for (const entry of bookmarkDb) {
    const [type, depth] = entry;

    if (path.length !== 0) {
      const depthToRemove = path.length - depth;

      if (depthToRemove > 0) {
        path.splice(-depthToRemove);
      }
    }

    if (type === "FOLDER") {
      const title = decodeHtmlEntityEncoding(entry[2]);
      path.push(title);
      await callback({
        type: type,
        path: path,
        title: title,
        url: null,
      });
    } else if (type === "LINK") {
      const title = decodeHtmlEntityEncoding(entry[3]);
      const url = entry[2];
      await callback({
        type: type,
        path: path,
        title: title,
        url: url,
      });
    } else if (type === "HR") {
      await callback({
        type: type,
        path: path,
        title: null,
        url: null,
      });
    }
  }
}

/**
 * @param {string} desiredCookieName
 */
function getCookie(desiredCookieName) {
  const cookiesString = document.cookie;
  if (cookiesString === "") {
    return null;
  }

  const cookiesObject = parseCookies(cookiesString);

  // Check if the desired cookie name exists in the cookiesObject
  if (Object.prototype.hasOwnProperty.call(cookiesObject, desiredCookieName)) {
    const cookieValue = cookiesObject[desiredCookieName];
    return cookieValue;
  } else {
    return null; // Cookie not found
  }
}

/**
 * @param {string} cookiesString
 */
function parseCookies(cookiesString) {
  const cookies = {};
  const cookiesArray = cookiesString.split(";");

  for (const cookie of cookiesArray) {
    const match = cookie.trim().match(/([^=]+)=(.*)/);
    const name = match[1];
    const value = match[2];

    cookies[name] = value;
  }

  return cookies;
}

/**
 * @param {string} string
 */
function sanitizeString(string) {
  const formattedString = string.replace(/[\u200E\u200F\u202A-\u202E]/gi, "");
  DOMPurify.sanitize(formattedString, { USE_PROFILES: { html: true } });
  return formattedString;
}

function getCurrentTime() {
  const currentTime = new Date();
  const timestamp = `${currentTime.getHours().toString().padStart(2, "0")}:${currentTime.getMinutes().toString().padStart(2, "0")}:${currentTime.getSeconds().toString().padStart(2, "0")}`;
  return timestamp;
}

/**
 * Function that checks if an HTTP response indicates that a resource is UP.
 * @param {Response | undefined} response - The HTTP response to be checked. Can be undefined if the web request failed.
 * @returns Returns `true` if the response indicates that the resource is UP; otherwise, returns `false`.
 */
function isResponseUp(response) {
  if (response === undefined) {
    return false;
  }

  if (response.ok) {
    return true;
  }

  return false;
}

/**
 * @param {string} string
 */
function encodeUnicodeEncoding(string) {
  const replacements = {
    "\\": "U+005C",
    "/": "U+002F",
    ":": "U+003A",
    "*": "U+002A",
    "?": "U+003F",
    '"': "U+0022",
    "<": "U+003C",
    ">": "U+003E",
    "|": "U+007C",
  };
  for (const chars in replacements) {
    const replacement = replacements[chars];
    string = string.split(chars).join(replacement);
  }
  return string;
}

/* eslint-disable no-unused-vars */
/**
 * @param {string} string
 */
function decodeUnicodeEncoding(string) {
  const replacements = {
    "U+005C": "\\",
    "U+002F": "/",
    "U+003A": ":",
    "U+002A": "*",
    "U+003F": "?",
    "U+0022": '"',
    "U+003C": "<",
    "U+003E": ">",
    "U+007C": "|",
  };
  for (const chars in replacements) {
    const replacement = replacements[chars];
    string = string.split(chars).join(replacement);
  }
  return string;
}
/* eslint-enable no-unused-vars */

/**
 * @param {string} string
 */
function encodeHtmlEntityEncoding(string) {
  const replacements = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&#39;",
    "<": "&lt;",
    ">": "&gt;",
    " ": "&nbsp;",
  };
  for (const chars in replacements) {
    const replacement = replacements[chars];
    string = string.split(chars).join(replacement);
  }
  return string;
}

/**
 * @param {string} string
 */
function decodeHtmlEntityEncoding(string) {
  const replacements = {
    "&amp;": "&",
    "&quot;": '"',
    "&#39;": "'",
    "&lt;": "<",
    "&gt;": ">",
  };
  for (const chars in replacements) {
    const replacement = replacements[chars];
    string = string.split(chars).join(replacement);
  }
  return string;
}

/**
 * @param {string} string
 */
function encodeUrlEncoding(string) {
  const replacements = {
    "%": "%25",
    " ": "%20",
    "[": "%5B",
    "]": "%5D",
    "{": "%7B",
    "}": "%7D",
    "^": "%5E",
    "`": "%60",
    "#": "%23",
  };
  for (const chars in replacements) {
    const replacement = replacements[chars];
    string = string.split(chars).join(replacement);
  }
  return string;
}

/**
 * @param {string} string
 */
function decodeUrlEncoding(string) {
  const replacements = {
    "%25": "%",
    "%20": " ",
    "%5B": "[",
    "%5D": "]",
    "%7B": "{",
    "%7D": "}",
    "%5E": "^",
    "%60": "`",
    "%23": "#",
  };
  for (const chars in replacements) {
    const replacement = replacements[chars];
    string = string.split(chars).join(replacement);
  }
  return string;
}

/**
 * @param {string} link
 */
function formatLink(link) {
  const href_link = encodeUrlEncoding(decodeUrlEncoding(link));
  const text_link = encodeHtmlEntityEncoding(decodeHtmlEntityEncoding(link));
  return `<a href="${href_link}">${text_link}</a>`;
}

/**
 * @param {Array} pathArray
 */
function formatPathLink(pathArray) {
  const href_link = encodeUrlEncoding(decodeUrlEncoding(pathArray.map((item) => encodeUnicodeEncoding(item)).join("/")));
  const text_link = encodeHtmlEntityEncoding(decodeHtmlEntityEncoding(pathArray.join("/")));
  return `<a href="/Illegal_Services/${href_link}/index.html">${text_link}</a>`;
}

/**
 * @param {string} userInput
 */
function formatUserInputToURL(userInput) {
  if (/^https?:\/\//.test(userInput)) {
    return userInput;
  } else {
    return `http://${userInput}`;
  }
}
