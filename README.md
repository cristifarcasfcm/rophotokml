# ROPhotoKml

Fotografii georeferențiate pe parcele KML (GPS, busolă, EXIF). Aplicație web (HTML/JS/Leaflet) împachetată cu **Capacitor 8** pentru Android și iOS.

## Structură
```
index.html                 aplicația (sursă unică pentru ambele platforme)
scripts/build-web.js       construiește www/ (index.html + Leaflet local)
scripts/generate_assets.py iconițe, splash, grafice magazine (Android + iOS)
scripts/configure_ios.py   Info.plist, iPhone-only, privacy manifest (idempotent)
android/                   proiect nativ Android (targetSdk 36, AAB semnat din CI)
ios/                       proiect nativ iOS (SPM, iOS 15+, Xcode 26)
docs/                      privacy.html, support.html  → GitHub Pages (/docs)
store/android/             SETUP.md, listing.md, icon-512, feature graphic
store/ios/                 SETUP.md, listing.md, icon-1024
store/sample-parcels.kml   fișier de test pentru recenzori
.github/workflows/         android-debug, android-release, ios-release
```

## Dezvoltare
```bash
npm ci
npm run sync          # build web + cap sync (ambele platforme)
npx cap open android  # Android Studio (JDK 21)
npx cap open ios      # Xcode 26 (doar macOS)
```
Cerințe: Node 22+, JDK 21, Android Studio Otter+, Xcode 26+.

## Publicare
- Android: `store/android/SETUP.md` → workflow **Android - AAB semnat** → Google Play
- iOS: `store/ios/SETUP.md` → workflow **iOS - build semnat + TestFlight** → App Store
- Versiune: `git tag v1.0.0 && git push --tags` (build/versionCode = numărul rulării CI)

## Note tehnice
- Hărțile Google (tile-uri directe) sunt dezactivate (`ENABLE_GOOGLE_TILES = false` în `index.html`) — nu sunt permise de termenii Google Maps Platform. Rămân Esri și OpenStreetMap, cu atribuire afișată.
- Android 16: butonul Back vine prin plugin-ul `App` (predictive back); `onBackPressed()` a fost eliminat.
- iOS: pozele se salvează în Fotografii prin `@capacitor-community/media` (EXIF păstrat); KML se deschide prin „Deschide cu” (`appUrlOpen`).
- Dacă modifici iconița: `python3 scripts/generate_assets.py` și comite rezultatele.
