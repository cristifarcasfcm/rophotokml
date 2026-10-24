// Construiește www/ : index.html + Leaflet local (fără CDN) -> aplicația funcționează și fără internet (în afară de hărți)
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const www = path.join(root, 'www');
const lib = path.join(www, 'lib');
const leaf = path.join(root, 'node_modules', 'leaflet', 'dist');

fs.rmSync(www, { recursive: true, force: true });
fs.mkdirSync(path.join(lib, 'images'), { recursive: true });
fs.copyFileSync(path.join(root, 'index.html'), path.join(www, 'index.html'));
fs.copyFileSync(path.join(leaf, 'leaflet.js'), path.join(lib, 'leaflet.js'));
fs.copyFileSync(path.join(leaf, 'leaflet.css'), path.join(lib, 'leaflet.css'));
for (const f of fs.readdirSync(path.join(leaf, 'images'))) {
  fs.copyFileSync(path.join(leaf, 'images', f), path.join(lib, 'images', f));
}
console.log('www/ gata:', fs.readdirSync(www).join(', '));
