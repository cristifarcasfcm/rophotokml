# iOS → App Store: pași (o singură dată)

Proiectul: `ios/` (Capacitor 8, Swift Package Manager, iOS 15+, **doar iPhone**). Bundle ID: `ro.rophotokml.app`.
Apple cere **Xcode 26 / SDK iOS 26** pentru încărcări (din 28.04.2026) — workflow-ul `ios-release.yml` verifică asta.
Build-ul rulează pe macOS în GitHub Actions; **nu ai nevoie de Mac** (doar pentru capturi, folosește un iPhone).

## 1. Cont Apple Developer Program
99 USD/an (individual sau organizație, D-U-N-S). Fără el nu se poate publica nici TestFlight.

## 2. În developer.apple.com
- Certificates, IDs & Profiles → **Identifiers → +** → App IDs → Bundle ID explicit `ro.rophotokml.app` (fără capabilități speciale).
- **Devices:** înregistrează cel puțin un iPhone (UDID) — necesar semnării automate din CI.
- Notează **Team ID** (Membership details).

## 3. În App Store Connect
- Apps → **+ New App**: iOS, nume `ROPhotoKml`, limba RO, Bundle ID `ro.rophotokml.app`, SKU `rophotokml-001`.
- Users and Access → Integrations → **App Store Connect API → Team Keys → +**, rol **Admin** (necesar pentru semnarea gestionată în cloud). Descarcă fișierul `AuthKey_XXXX.p8` (se poate descărca o singură dată) și notează *Key ID* și *Issuer ID*.
```bash
base64 -w0 AuthKey_XXXX.p8     # macOS: base64 -i AuthKey_XXXX.p8
```

## 4. GitHub → Settings → Secrets and variables → Actions
| Secret | Valoare |
|---|---|
| `ASC_KEY_ID` | Key ID |
| `ASC_ISSUER_ID` | Issuer ID |
| `ASC_KEY_P8_BASE64` | conținut `.p8` în base64 |
| `APPLE_TEAM_ID` | Team ID (10 caractere) |

## 5. Prima versiune
1. Actions → **iOS - build semnat + TestFlight / App Store** → Run workflow (sau `git tag v1.0.0 && git push --tags`).
2. După 10–30 min build-ul apare în App Store Connect → TestFlight (procesare Apple). Adaugă testeri interni, testează pe iPhone.
3. App Store → versiunea 1.0 → alege build-ul → completează metadatele (`store/ios/listing.md`) → **Submit for Review**.

`CURRENT_PROJECT_VERSION` (build) = numărul rulării din Actions (strict crescător); versiunea afișată = tag-ul `vX.Y.Z`.

## 6. Formulare App Store Connect
- **Privacy Policy URL:** `https://cristifarcasfcm.github.io/rophotokml/privacy.html` · **Support URL:** `.../support.html`
- **App Privacy (nutrition label):** *Data Collected → Location → Precise Location* · Linked to user: **Nu** · Used for tracking: **Nu** · Purpose: **App Functionality**. Restul: *Data Not Collected*. (Coordonatele merg către OpenStreetMap Nominatim; fișierele/pozele nu pleacă din telefon.)
- **Age Rating:** chestionarul actualizat (2026) → toate „None/No” → 4+ (selectează „fără acces nerestricționat la web”).
- **Export compliance:** deja declarat în `Info.plist` (`ITSAppUsesNonExemptEncryption = false`, doar HTTPS).
- **Capturi iPhone:** 6,9" (1320×2868 sau 1290×2796) — minim 1, recomandat 4–5. Nu se cer capturi iPad (aplicație doar iPhone).
- **Notes for Review:** vezi `store/ios/listing.md` (include fișierul `sample-parcels.kml`).
- **Trader status (UE/DSA):** completează datele de contact afișate public.

## 7. Risc de respingere: Guideline 4.2 (funcționalitate minimă / „web wrapper”)
Argumente incluse în notele de recenzie: cameră + GPS + busolă + salvare în Fotografii (plugin nativ), asociere nativă cu fișiere `.kml` („Deschide cu”), funcționare cu date locale persistente. Dacă totuși refuză, răspunde în Resolution Center cu aceste puncte.

## Alternativă: distribuție doar pentru colegi
**Custom App** (Apple Business Manager) sau **Unlisted App Distribution** — fără listare publică, același build.
