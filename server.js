const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
    // Clean up url path (ignores query parameters like ?hash=...)
    const host = req.headers.host || `localhost:${PORT}`;
    const parsedUrl = new URL(req.url, `http://${host}`);
    let safePath = parsedUrl.pathname;
    
    // Default root path to bus.html
    if (safePath === '/' || safePath === '') {
        safePath = '/bus.html';
    }

    const fileLoc = path.join(__dirname, safePath);

    fs.stat(fileLoc, (err, stats) => {
        if (err || !stats.isFile()) {
            // Fall back to bus.html for unmatched routes (enables routing)
            const fallbackLoc = path.join(__dirname, 'bus.html');
            fs.readFile(fallbackLoc, (fallbackErr, content) => {
                if (fallbackErr) {
                    res.writeHead(404, { 'Content-Type': 'text/plain' });
                    res.end('404 Not Found');
                } else {
                    res.writeHead(200, { 'Content-Type': 'text/html' });
                    res.end(content);
                }
            });
            return;
        }

        // Determine correct content type
        const ext = path.extname(fileLoc).toLowerCase();
        const contentType = MIME_TYPES[ext] || 'application/octet-stream';

        fs.readFile(fileLoc, (readErr, content) => {
            if (readErr) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('500 Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': contentType });
                res.end(content);
            }
        });
    });
});

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running at http://0.0.0.0:${PORT} (accessible externally)`);
    console.log('Press Ctrl+C to stop the server.');
});
