# Android → Google Play: pași (o singură dată)

Proiectul: `android/` (Capacitor 8, **targetSdk 36** — cerut de Google Play pentru aplicații noi/actualizări din 31.08.2026).
Pachet: `ro.rophotokml.app` · Format publicare: **AAB semnat** (nu APK).

## 1. Cheia de încărcare (upload key) — OBLIGATORIU, păstrează-o în siguranță
```bash
keytool -genkeypair -v -keystore upload.keystore -alias upload \
  -keyalg RSA -keysize 2048 -validity 10000
base64 -w0 upload.keystore > upload.keystore.b64      # macOS: base64 -i upload.keystore -o upload.keystore.b64
```
Fă o copie de siguranță a `upload.keystore` + parole (manager de parole / seif). **Nu o pune în git** (e în `.gitignore`).
Dacă o pierzi, recuperarea se face doar prin suport Google (Play App Signing păstrează cheia reală de semnare).

## 2. GitHub → Settings → Secrets and variables → Actions
| Secret | Valoare |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | conținutul `upload.keystore.b64` |
| `ANDROID_KEYSTORE_PASSWORD` | parola keystore |
| `ANDROID_KEY_ALIAS` | `upload` |
| `ANDROID_KEY_PASSWORD` | parola cheii |
| `PLAY_SERVICE_ACCOUNT_JSON` | *(opțional, pentru încărcare automată)* JSON cont de serviciu din Play Console → Setup → API access |

## 3. Cont Google Play Console
- Cont dezvoltator (taxă unică 25 USD), verificare identitate + adresă/telefon/e-mail (afișate public pentru dezvoltatori „trader” în UE).
- **Cont personal nou:** Google cere test închis (closed testing) cu un număr minim de testeri, mai multe zile consecutive, înainte de Producție — verifică cifrele curente în Play Console → Dashboard.
- **Distribuție doar pentru colegi?** Poți publica aplicația ca **privată (organizație, Managed Google Play)** — scutită de cerințele de test și de țintă API.

## 4. Creează aplicația și completează (Play Console)
1. Create app → nume `ROPhotoKml`, limba RO, App (nu joc), **Gratuită**.
2. **Policy → App content:**
   - Privacy policy URL: `https://cristifarcasfcm.github.io/rophotokml/privacy.html` (vezi „GitHub Pages” mai jos)
   - Ads: **Nu** · App access: *toate funcțiile accesibile fără cont* (adaugă instrucțiuni + `store/sample-parcels.kml`)
   - Target audience: **18+** (nu pentru copii) · Content rating: chestionar IARC → utilitar, fără conținut generat de utilizatori
   - Government apps: **nu declara afiliere** (aplicația nu este oficială APIA) — vezi nota din listing
   - **Data safety** (răspunsuri recomandate):
     - Date colectate: **Locație precisă** — Da; trimisă (HTTPS) către OpenStreetMap Nominatim; scop: *App functionality*; opțională (utilizatorul poate refuza permisiunea); nu e folosită pentru reclame/analytics.
     - Fotografii, fișiere, ID dispozitiv, contacte, plăți: **Nu sunt colectate**
     - Date criptate în tranzit: **Da** · Cerere de ștergere: *nu există cont/date pe servere proprii*
3. **Store listing:** texte din `store/android/listing.md`, iconiță `store/android/icon-512.png`, grafic `store/android/feature-graphic-1024x500.png`, **minim 2 capturi de ecran telefon** (făcute de pe dispozitiv; 1080×1920 sau mai mari).
4. **Permisiuni:** CAMERA, ACCESS_FINE/COARSE_LOCATION (doar în prim-plan). Nu se folosesc permisiuni de citire foto/video → fără formulare speciale.

## 5. Prima versiune
1. GitHub → Actions → **Android - AAB semnat pentru Google Play** → Run workflow (sau `git tag v1.0.0 && git push --tags`).
2. Descarcă artefactul `ROPhotoKml-release-aab` → Play Console → Testing → Internal/Closed → Create release → încarcă `app-release.aab` (acceptă Play App Signing).
   *Prima încărcare trebuie făcută manual; după aceea poți bifa `upload_to_play` în workflow.*
3. Testează pe telefon (link de testare internă) → promovează în Producție.

`versionCode` = numărul rulării din GitHub Actions (crește automat; Play cere valori strict crescătoare).

## GitHub Pages pentru politica de confidențialitate
Repo → Settings → Pages → Source: *Deploy from a branch* → `main` / folder `/docs`. URL-uri: `.../privacy.html`, `.../support.html`.
