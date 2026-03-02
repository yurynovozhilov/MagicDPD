(function () {
  var SELECTOR = "article.post .js-link-preview[data-url]";
  var DEFAULT_API_ENDPOINT = "https://api.microlink.io/";
  var cache = new Map();

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function normalizeText(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function parseHostname(url) {
    try {
      return new URL(url).hostname.replace(/^www\./, "");
    } catch (error) {
      return url;
    }
  }

  function buildApiUrl(endpoint, targetUrl) {
    var normalizedEndpoint = endpoint || DEFAULT_API_ENDPOINT;
    var separator = normalizedEndpoint.indexOf("?") === -1 ? "?" : "&";
    return (
      normalizedEndpoint +
      separator +
      "url=" +
      encodeURIComponent(targetUrl) +
      "&screenshot=true"
    );
  }

  function getImageUrl(data) {
    if (!data) {
      return "";
    }

    if (typeof data.image === "string") {
      return data.image;
    }

    if (data.image && typeof data.image.url === "string") {
      return data.image.url;
    }

    if (typeof data.screenshot === "string") {
      return data.screenshot;
    }

    if (data.screenshot && typeof data.screenshot.url === "string") {
      return data.screenshot.url;
    }

    return "";
  }

  function getPublisher(data) {
    if (!data) {
      return "";
    }

    if (typeof data.publisher === "string") {
      return data.publisher;
    }

    if (data.publisher && typeof data.publisher.name === "string") {
      return data.publisher.name;
    }

    return "";
  }

  function buildCardHtml(url, fallbackText, data) {
    var title = normalizeText(data && data.title) || fallbackText || url;
    var description = normalizeText(data && data.description);
    var imageUrl = normalizeText(getImageUrl(data));
    var host = normalizeText(getPublisher(data)) || parseHostname(url);

    var imageBlock = "";
    if (imageUrl) {
      imageBlock =
        '<span class="link-preview__thumb-wrap">' +
        '<img class="link-preview__thumb" src="' +
        escapeHtml(imageUrl) +
        '" alt="" loading="lazy" referrerpolicy="no-referrer">' +
        "</span>";
    }

    var descriptionBlock = "";
    if (description) {
      descriptionBlock =
        '<span class="link-preview__description">' +
        escapeHtml(description) +
        "</span>";
    }

    return (
      '<a class="link-preview__card" href="' +
      escapeHtml(url) +
      '" target="_blank" rel="noopener noreferrer">' +
      imageBlock +
      '<span class="link-preview__body">' +
      '<span class="link-preview__title">' +
      escapeHtml(title) +
      "</span>" +
      descriptionBlock +
      '<span class="link-preview__host">' +
      escapeHtml(host) +
      "</span>" +
      "</span>" +
      "</a>"
    );
  }

  function fetchPreview(url, endpoint) {
    var key = endpoint + "|" + url;
    if (cache.has(key)) {
      return cache.get(key);
    }

    var request = fetch(buildApiUrl(endpoint, url), {
      headers: {
        Accept: "application/json"
      }
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("HTTP " + response.status);
        }
        return response.json();
      })
      .then(function (payload) {
        if (!payload || payload.status !== "success" || !payload.data) {
          throw new Error("Invalid preview payload");
        }
        return payload.data;
      });

    cache.set(key, request);
    return request;
  }

  function enhanceNode(node) {
    var url = normalizeText(node.dataset.url);
    if (!url) {
      return;
    }

    var fallbackText = normalizeText(node.dataset.text) || url;
    var endpoint = normalizeText(node.dataset.api) || DEFAULT_API_ENDPOINT;
    node.classList.add("link-preview--active");

    fetchPreview(url, endpoint)
      .then(function (data) {
        node.innerHTML = buildCardHtml(url, fallbackText, data);
      })
      .catch(function () {
        node.classList.add("link-preview--failed");
        node.innerHTML =
          '<span class="link-preview__status">Превью недоступно (' +
          escapeHtml(parseHostname(url)) +
          ")</span>";
      });
  }

  function init() {
    var nodes = document.querySelectorAll(SELECTOR);
    if (!nodes.length) {
      return;
    }

    nodes.forEach(enhanceNode);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
