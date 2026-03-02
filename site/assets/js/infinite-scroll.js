(function () {
  var FEED_SELECTOR = ".articles.h-feed";
  var ITEM_SELECTOR = "article.post-list.h-feed, .post-short-list.h-entry";
  var NEXT_LINK_SELECTOR = ".pagination .right.pagination-item a";
  var OBSERVER_MARGIN = "1200px 0px";
  var STATUS_LOADING = "Загружаю записи...";
  var STATUS_DONE = "Все доступные записи загружены";
  var STATUS_ERROR = "Не удалось подгрузить записи. Попробуйте обновить страницу.";

  function toAbsoluteUrl(url) {
    if (!url) {
      return "";
    }

    try {
      return new URL(url, window.location.href).toString();
    } catch (error) {
      return "";
    }
  }

  function getNextUrl(scope) {
    if (!scope || !scope.querySelector) {
      return "";
    }

    var link = scope.querySelector(NEXT_LINK_SELECTOR);
    if (!link) {
      return "";
    }

    return toAbsoluteUrl(link.getAttribute("href"));
  }

  function getItemKey(item) {
    if (!item || !item.querySelector) {
      return "";
    }

    var permalink = item.querySelector(".post-title a");
    if (!permalink) {
      return "";
    }

    return toAbsoluteUrl(permalink.getAttribute("href"));
  }

  function collectItems(scope) {
    if (!scope || !scope.querySelectorAll) {
      return [];
    }

    return Array.from(scope.querySelectorAll(ITEM_SELECTOR));
  }

  function updateStatus(node, message, isError) {
    if (!node) {
      return;
    }

    node.textContent = message || "";
    node.classList.toggle("infinite-scroll-status--error", !!isError);
  }

  function dispatchItemsAppended(feed, items) {
    if (!items.length) {
      return;
    }

    document.dispatchEvent(
      new CustomEvent("magicdpd:items-appended", {
        detail: {
          container: feed,
          items: items
        }
      })
    );
  }

  function init() {
    var feed = document.querySelector(FEED_SELECTOR);
    if (!feed) {
      return;
    }

    var pagination = feed.querySelector(".pagination");
    if (!pagination) {
      return;
    }

    var initialNextUrl = getNextUrl(feed);
    if (!initialNextUrl) {
      return;
    }

    var status = document.createElement("p");
    status.className = "infinite-scroll-status";
    status.setAttribute("aria-live", "polite");

    var sentinel = document.createElement("div");
    sentinel.className = "infinite-scroll-sentinel";
    sentinel.setAttribute("aria-hidden", "true");

    pagination.insertAdjacentElement("afterend", status);
    status.insertAdjacentElement("afterend", sentinel);
    document.documentElement.classList.add("infinite-scroll-enabled");

    var seenItems = new Set();
    collectItems(feed).forEach(function (item) {
      var key = getItemKey(item);
      if (key) {
        seenItems.add(key);
      }
    });

    var isLoading = false;
    var nextUrl = initialNextUrl;

    function loadNextPage() {
      if (isLoading || !nextUrl) {
        return;
      }

      isLoading = true;
      updateStatus(status, STATUS_LOADING, false);

      fetch(nextUrl, {
        headers: {
          Accept: "text/html"
        }
      })
        .then(function (response) {
          if (!response.ok) {
            throw new Error("HTTP " + response.status);
          }
          return response.text();
        })
        .then(function (html) {
          var parser = new DOMParser();
          var doc = parser.parseFromString(html, "text/html");
          var nextFeed = doc.querySelector(FEED_SELECTOR);
          if (!nextFeed) {
            throw new Error("Missing feed container");
          }

          var importedItems = [];
          collectItems(nextFeed).forEach(function (item) {
            var key = getItemKey(item);
            if (key && seenItems.has(key)) {
              return;
            }
            if (key) {
              seenItems.add(key);
            }

            var importedNode = document.importNode(item, true);
            feed.insertBefore(importedNode, pagination);
            importedItems.push(importedNode);
          });

          dispatchItemsAppended(feed, importedItems);
          nextUrl = getNextUrl(nextFeed);

          if (!nextUrl) {
            observer.disconnect();
            updateStatus(status, STATUS_DONE, false);
            return;
          }

          updateStatus(status, "", false);
        })
        .catch(function () {
          observer.disconnect();
          updateStatus(status, STATUS_ERROR, true);
        })
        .finally(function () {
          isLoading = false;
        });
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            loadNextPage();
          }
        });
      },
      {
        rootMargin: OBSERVER_MARGIN
      }
    );

    observer.observe(sentinel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
