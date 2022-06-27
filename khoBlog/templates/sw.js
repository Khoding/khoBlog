const VERSION = "{{ version }}";
const staticCachePrefix = "static";
const staticCacheName = `${staticCachePrefix}-${VERSION}`;
const dynamicCacheName = "dynamic";
const appShell = [
    "{{ icon_url }}",
    "{{ manifest_url }}",
    "{{ style_url }}",
    "{{ home_url }}",
    "{{ offline_url }}",
].map((partialUrl) => `${location.protocol}//${location.host}${partialUrl}`);
const maxNumberItemsDynamicCache = 5;
const urlsToCacheTimes = new Map();
// In milliseconds.
const networkWaitTime = 2000;

self.addEventListener("install", (event) => {
    console.log("[SW] Installing SW version:", VERSION);
    event.waitUntil(
        caches.open(staticCacheName).then((cache) => {
            console.log("[SW] Caching app shell");
            cache.addAll(appShell);
        })
    );
});

self.addEventListener("activate", (event) => {
    console.log("[SW] Cleaning old cache shell");
    event.waitUntil(
        caches
            .keys()
            .then((keys) =>
                Promise.all(
                    keys
                        .filter(
                            (key) =>
                                key !== staticCacheName &&
                                key.startsWith(staticCachePrefix)
                        )
                        .map((key) => caches.delete(key))
                )
            )
    );
});

self.addEventListener("fetch", (event) => {
    // Let the browser do its default thing
    // for non-GET requests.
    if (event.request.method !== "GET") {
        return;
    }

    event.respondWith(networkThenCache(event));
});

function networkThenCache(event) {
    // Always get the app shell from the cache.
    if (appShell.includes(event.request.url)) {
        console.log(
            "[SW] Requested file from app shell, serving from the cache."
        );
        return getFromCache(event);
    }

    return Promise.race([
        tryToFetchAndSaveInCache(event, dynamicCacheName),
        new Promise((resolve, reject) => setTimeout(reject, networkWaitTime)),
    ]).then(
        (response) => response,
        () => getFromCache(event).catch(() => provideOfflineFallback(event))
    );
}

function getFromCache(event) {
    return caches.match(event.request).then((response) => {
        console.log(`[SW] Requesting ${event.request.url}.`);
        // If we have the response in the cache, we return it.
        // If not, we try to fetch it.
        if (response) {
            console.log(
                `[SW] Served response to ${event.request.url} from the cache.`
            );
            return response;
        }

        return Promise.reject();
    });
}

function tryToFetchAndSaveInCache(event, cacheName) {
    return fetchAndSaveInCache(event, cacheName).catch((err) => {
        console.warn(
            "[SW] Network request failed, app is probably offline",
            err
        );
        return provideOfflineFallback(event).catch((err) =>
            console.warn(
                "[SW] failed to get response from network and cache.",
                err
            )
        );
    });
}

function fetchAndSaveInCache(event, cacheName) {
    console.log(`[SW] Fetching ${event.request.url}`);
    return fetch(event.request).then((res) => {
        const requestSucceeded = res.status >= 200 && res.status <= 300;
        const cacheHeader = res.headers.get("cache-control") || [];
        const mustNotCache = cacheHeader.includes("no-cache");
        if (!requestSucceeded) {
            console.log("[SW] Request failed.");
            return res;
        } else if (mustNotCache) {
            console.log("[SW] The page must not be cached.");
            return res;
        }

        return caches.open(cacheName).then((cache) => {
            // We can read a response only once. So if we don't clone it here,
            // we won't be able to see anything in the browser.
            cache.put(event.request.url, res.clone()).then(() => {
                urlsToCacheTimes.set(event.request.url, Date.now());
                return trimCache(
                    cache,
                    maxNumberItemsDynamicCache,
                    urlsToCacheTimes
                );
            });

            return res;
        });
    });
}

function trimCache(cache, maxItems, cacheTimeInfos) {
    if (cacheTimeInfos.size <= maxItems) {
        console.log("[SW] Nothing to trim from the cache.");
        return Promise.resolve();
    }

    // We sort all entries by descending dates.
    // We keep a slice of the maxItems more recent items.
    const urlsToKeep = Array.from(cacheTimeInfos.entries())
        .sort((a, b) => a[1] - b[1])
        .reverse()
        .slice(0, maxItems)
        .map(([url, _]) => url);

    console.log("[SW] Keeping in cache", urlsToKeep);
    return cache
        .keys()
        .then((keys) => {
            const deletions = keys.map((key) => {
                if (urlsToKeep.includes(key.url)) {
                    return Promise.resolve();
                }

                console.log(`[SW] Removing ${key.url} from the cache.`);
                cacheTimeInfos.delete(key.url);
                return cache.delete(key);
            });
            return Promise.all(deletions);
        })
        .then(() => console.log("[SW] Done trimming cache."))
        .catch(() => console.log("[SW] Error while trimming cache."));
}

function provideOfflineFallback(event) {
    return caches.open(staticCacheName).then((cache) => {
        // If the request expects an HTML response, we display the offline page.
        if (event.request.headers.get("accept").includes("text/html")) {
            return cache.match("/offline/");
        }

        return Promise.reject();
    });
}
