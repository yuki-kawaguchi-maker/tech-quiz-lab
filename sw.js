/* Tech Quiz Lab service worker */
"use strict";

var CACHE_VERSION = "tq-cache-v7";

var PRECACHE_URLS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_VERSION).then(function (cache) {
      return cache.addAll(PRECACHE_URLS);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys
          .filter(function (key) { return key !== CACHE_VERSION; })
          .map(function (key) { return caches.delete(key); })
      );
    })
  );
  self.clients.claim();
});

function isNetworkFirstDataRequest(url) {
  return url.pathname.indexOf("/data/questions/") !== -1
    || url.pathname.indexOf("/data/lessons/") !== -1
    || /\/data\/curriculum\.json$/.test(url.pathname);
}

function isAppShellRequest(url) {
  return url.pathname.slice(-1) === "/"
    || /\/index\.html$/.test(url.pathname)
    || /\/manifest\.json$/.test(url.pathname);
}

function networkFirst(event) {
  event.respondWith(
    fetch(event.request)
      .then(function (response) {
        var copy = response.clone();
        caches.open(CACHE_VERSION).then(function (cache) { cache.put(event.request, copy); });
        return response;
      })
      .catch(function () {
        return caches.match(event.request);
      })
  );
}

self.addEventListener("fetch", function (event) {
  var url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin) {
    return;
  }

  if (isNetworkFirstDataRequest(url)) {
    /* 問題データ・レッスンデータはnetwork-first: 最新データを優先し、取得失敗時はキャッシュにフォールバック */
    networkFirst(event);
    return;
  }

  if (isAppShellRequest(url)) {
    /* index.html・manifest.jsonはnetwork-first: デプロイ直後の初回起動から新版を反映する
       (cache-firstだと1回目の起動は旧版のまま表示されてしまうため) */
    networkFirst(event);
    return;
  }

  /* それ以外(icons等)はcache-first */
  event.respondWith(
    caches.match(event.request).then(function (cached) {
      if (cached) return cached;
      return fetch(event.request).then(function (response) {
        var copy = response.clone();
        caches.open(CACHE_VERSION).then(function (cache) { cache.put(event.request, copy); });
        return response;
      });
    })
  );
});
