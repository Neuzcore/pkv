// Erstattung – Beihilfe & PKV · Service Worker
// WICHTIG: Cache-Version bei JEDEM Deploy hochzählen, sonst laden Clients alte Assets.
const CACHE = 'erstattung-v1.1.0';

const ASSETS = [
  './pkv.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // API-Aufrufe NIE abfangen/cachen – sonst kommt der Worker nie durch.
  if (url.hostname.endsWith('workers.dev')) return;
  // Google Fonts ebenfalls durchlassen (werden vom Browser gecacht).
  if (url.hostname.includes('fonts.googleapis.com') || url.hostname.includes('fonts.gstatic.com')) return;
  if (e.request.method !== 'GET') return;

  // App-Shell: cache-first mit Netzwerk-Aktualisierung
  e.respondWith(
    caches.match(e.request).then(cached => {
      const net = fetch(e.request).then(res => {
        if (res && res.status === 200 && url.origin === location.origin) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return res;
      }).catch(() => cached);
      return cached || net;
    })
  );
});
