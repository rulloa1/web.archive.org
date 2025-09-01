const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = Number(process.env.PORT) || 3000;
const ROOT = path.resolve(__dirname);

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.eot': 'application/vnd.ms-fontobject',
  '.otf': 'font/otf',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
};

function isPathInside(child, parent) {
  const rel = path.relative(parent, child);
  return !!rel && !rel.startsWith('..') && !path.isAbsolute(rel);
}

function send(res, status, headers, bodyStream) {
  res.writeHead(status, headers);
  if (bodyStream && typeof bodyStream.pipe === 'function') {
    bodyStream.pipe(res);
  } else {
    res.end(bodyStream || '');
  }
}

function notFound(res) {
  send(res, 404, { 'Content-Type': 'text/plain; charset=utf-8' }, '404 Not Found');
}

function serveFile(res, filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const type = MIME_TYPES[ext] || 'application/octet-stream';
  const stream = fs.createReadStream(filePath);
  stream.on('open', () => {
    send(res, 200, {
      'Content-Type': type,
      'Cache-Control': ext === '.html' ? 'no-cache' : 'public, max-age=3600',
    }, stream);
  });
  stream.on('error', () => notFound(res));
}

function tryIndex(filePath) {
  const indexPath = path.join(filePath, 'index.html');
  return fs.existsSync(indexPath) ? indexPath : null;
}

const server = http.createServer((req, res) => {
  try {
    const parsed = url.parse(req.url || '/');
    const decodedPath = decodeURIComponent(parsed.pathname || '/');
    const requestedPath = path.normalize(decodedPath).replace(/^\/+/, '');
    const absolutePath = path.join(ROOT, requestedPath);

    if (!isPathInside(absolutePath, ROOT)) {
      send(res, 403, { 'Content-Type': 'text/plain; charset=utf-8' }, '403 Forbidden');
      return;
    }

    let finalPath = absolutePath;
    if (!fs.existsSync(finalPath)) {
      // If path not found and looks like directory, try directory index
      if (!path.extname(finalPath)) {
        const idx = tryIndex(finalPath);
        if (idx) {
          finalPath = idx;
        }
      }
    }

    if (fs.existsSync(finalPath)) {
      const stat = fs.statSync(finalPath);
      if (stat.isDirectory()) {
        const idx = tryIndex(finalPath);
        if (idx) {
          serveFile(res, idx);
          return;
        }
        // If directory without index.html, list entries
        const entries = fs.readdirSync(finalPath, { withFileTypes: true });
        const list = entries.map(e => {
          const name = e.name + (e.isDirectory() ? '/' : '');
          const href = path.posix.join(decodedPath.replace(/\/$/, ''), name);
          return `<li><a href="${href}">${name}</a></li>`;
        }).join('');
        const html = `<!doctype html><meta charset="utf-8"><title>Index of ${decodedPath}</title><ul>${list}</ul>`;
        send(res, 200, { 'Content-Type': 'text/html; charset=utf-8' }, html);
        return;
      }
      serveFile(res, finalPath);
      return;
    }

    // Root fallback to index.html
    if (decodedPath === '/' && fs.existsSync(path.join(ROOT, 'index.html'))) {
      serveFile(res, path.join(ROOT, 'index.html'));
      return;
    }

    notFound(res);
  } catch (err) {
    send(res, 500, { 'Content-Type': 'text/plain; charset=utf-8' }, '500 Internal Server Error');
  }
});

server.listen(PORT, () => {
  // eslint-disable-next-line no-console
  console.log(`Static server running at http://localhost:${PORT}/`);
});
