(function () {
  "use strict";

  var input = document.getElementById("search-input");
  var resultsContainer = document.getElementById("search-results");
  var status = document.getElementById("search-status");

  if (!input || !resultsContainer || !status) {
    return;
  }

  var indexUrl = resultsContainer.getAttribute("data-index-url") || "/index.json";
  var minChars = parseInt(resultsContainer.getAttribute("data-min-chars") || "2", 10);
  var maxResults = parseInt(resultsContainer.getAttribute("data-max-results") || "30", 10);
  var threshold = parseFloat(resultsContainer.getAttribute("data-threshold") || "0.36");

  var fuse = null;
  var searchData = [];

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function escapeRegExp(value) {
    return String(value || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function normalizeWhitespace(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function setStatus(message, isError) {
    status.textContent = message;
    status.classList.toggle("search-status--error", Boolean(isError));
  }

  function queryTerms(query) {
    return normalizeWhitespace(query)
      .split(" ")
      .filter(function (term) {
        return term.length > 1;
      })
      .slice(0, 8);
  }

  function highlightText(text, query) {
    var highlighted = escapeHtml(text);
    var terms = queryTerms(query);

    terms.forEach(function (term) {
      var matcher = new RegExp("(" + escapeRegExp(term) + ")", "gi");
      highlighted = highlighted.replace(matcher, "<mark>$1</mark>");
    });

    return highlighted;
  }

  function updateSearchQueryInUrl(query) {
    if (!window.history || !window.history.replaceState) {
      return;
    }

    var nextUrl = new URL(window.location.href);
    if (query) {
      nextUrl.searchParams.set("q", query);
    } else {
      nextUrl.searchParams.delete("q");
    }
    window.history.replaceState({}, "", nextUrl.toString());
  }

  function createSnippet(item, matchInfo, query) {
    var source = normalizeWhitespace(item.summary || item.content || "");
    if (!source) {
      return "";
    }

    var match = null;
    if (Array.isArray(matchInfo)) {
      match = matchInfo.find(function (entry) {
        return (
          (entry.key === "content" || entry.key === "summary") &&
          Array.isArray(entry.indices) &&
          entry.indices.length > 0
        );
      });
    }

    var start = 0;
    var end = Math.min(source.length, 220);
    if (match) {
      start = Math.max(0, match.indices[0][0] - 80);
      end = Math.min(source.length, match.indices[0][1] + 140);
    }

    var snippet = source.slice(start, end);
    if (start > 0) {
      snippet = "... " + snippet;
    }
    if (end < source.length) {
      snippet = snippet + " ...";
    }

    return highlightText(snippet, query);
  }

  function renderResults(query, matches) {
    if (!matches.length) {
      resultsContainer.innerHTML = "";
      setStatus("Ничего не найдено.");
      return;
    }

    var html = matches
      .map(function (result) {
        var item = result.item || {};
        var link = item.permalink || "#";
        var title = highlightText(normalizeWhitespace(item.title || "Без названия"), query);
        var snippet = createSnippet(item, result.matches, query);
        var dateBlock = item.date
          ? '<p class="search-result__meta">' + escapeHtml(item.date) + "</p>"
          : "";
        var snippetBlock = snippet
          ? '<p class="search-result__snippet">' + snippet + "</p>"
          : "";

        return (
          '<article class="search-result">' +
          '<h2 class="search-result__title"><a href="' +
          escapeHtml(link) +
          '">' +
          title +
          "</a></h2>" +
          dateBlock +
          snippetBlock +
          "</article>"
        );
      })
      .join("");

    resultsContainer.innerHTML = html;
    setStatus("Найдено: " + matches.length + ".");
  }

  function runSearch(rawQuery) {
    var query = normalizeWhitespace(rawQuery);
    updateSearchQueryInUrl(query);

    if (!query) {
      resultsContainer.innerHTML = "";
      setStatus("Введите поисковый запрос.");
      return;
    }

    if (query.length < minChars) {
      resultsContainer.innerHTML = "";
      setStatus("Введите минимум " + minChars + " символа.");
      return;
    }

    if (!fuse) {
      setStatus("Индекс еще загружается...");
      return;
    }

    var matches = fuse.search(query, { limit: maxResults });
    renderResults(query, matches);
  }

  function debounce(fn, timeoutMs) {
    var timer = null;
    return function () {
      var args = arguments;
      window.clearTimeout(timer);
      timer = window.setTimeout(function () {
        fn.apply(null, args);
      }, timeoutMs);
    };
  }

  function configureFuse(data) {
    fuse = new Fuse(data, {
      includeMatches: true,
      ignoreLocation: true,
      minMatchCharLength: Math.max(minChars, 2),
      threshold: threshold,
      keys: [
        { name: "title", weight: 0.4 },
        { name: "summary", weight: 0.2 },
        { name: "content", weight: 0.35 },
        { name: "tags", weight: 0.05 }
      ]
    });
  }

  function start() {
    if (typeof window.Fuse === "undefined") {
      setStatus("Fuse.js не загрузился. Проверьте доступ к CDN.", true);
      return;
    }

    input.disabled = true;
    setStatus("Загрузка индекса...");

    fetch(indexUrl, { credentials: "same-origin" })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("HTTP " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        searchData = Array.isArray(data) ? data : [];
        configureFuse(searchData);
        input.disabled = false;

        var initialQuery = new URLSearchParams(window.location.search).get("q") || "";
        if (initialQuery) {
          input.value = initialQuery;
          runSearch(initialQuery);
        } else {
          setStatus("Индекс загружен. Введите запрос.");
        }
      })
      .catch(function (error) {
        input.disabled = false;
        setStatus("Не удалось загрузить индекс: " + error.message, true);
      });
  }

  input.addEventListener("input", debounce(function (event) {
    runSearch(event.target.value);
  }, 140));

  start();
})();
