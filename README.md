# ROPhotoKml — Aplicație Control pe Teren APIA Maramureș

**Autor:** Cristian Farcaș — Inspector Serviciul de Control pe Teren, APIA Maramureș  
**Soluție tehnică:** Web App offline / Android APK nativ (prin Capacitor 6) + QGIS GIS workflow

---

## 1. Ce a fost optimizat și modificat în ultima versiune

1. **Inscripționarea fotografiilor pe 6 rânduri clare și aerisite (Zero Suprapunere)**
   - Textul imprimat pe fotografie folosește un layout pe 6 linii orizontale independente, aliniate la stânga și protejate la lățime (`maxW`), fără să se mai suprapună vreodată pe ecran:
     - **Linia 1 (Auriu #FAC775 - Mare):** Valoarea atributului `name_calc` sau „Câmpul 1” (ex. `RO008793211, 14, a`), **fără denumirea etichetei**.
     - **Linia 2 (Auriu deschis #FDE68A):** Atributul 2 selectat din meniul de jos sau următorul atribut disponibil din parcelă.
     - **Linia 3 (Alb #FFFFFF):** Coordonate GPS (`47.662180°, 23.511820°`).
     - **Linia 4 (Alb #FFFFFF):** Altitudine ; Acuratețe ; Orientare (`Alt: 239m ; Acc: ±4m ; Dir: 190° S`).
     - **Linia 5 (Alb #FFFFFF):** Data și ora fotografierii (`30.07.2026 13:18:25`).
     - **Linia 6 (Albastru #93C5FD):** Localitatea și adresa unde a fost făcută fotografia (`BAIA MARE | saliste ieud-pasca-zetye`).

2. **Hărți de fundal avansate (Google & ESRI Satelit Hybrid, Drumuri)**
   - Apăsând pe butonul **Strat** (stânga-jos), se deschide fereastra **Model Hartă de Fundal**, unde puteți alege instantaneu între 5 modele profesionale:
     - 🛰️ **Google Satelit Hybrid** *(Satelit Google + localități și drumuri)*
     - 🗺️ **Google Drumuri (Roadmap)** *(Străzi, drumuri și granițe)*
     - 🌍 **ESRI Satelit Hybrid** *(Satelit ESRI + etichete locuri și granițe)*
     - 🛰️ **ESRI Satelit Simplu** *(Doar imagini satelitare ESRI)*
     - 🗺️ **OpenStreetMap** *(Hartă liberă drumuri)*
   - Alegerea este reținută automat pentru sesiunile viitoare.

3. **Cameră foto stabilă (fără blocare la deschidere)**
   - Funcția de cameră utilizează rezoluția ideală `1920x1080` (Full HD) pe encoderul Android și eliberează corect resursele la închidere sau comutare.

4. **Interfața de deschidere („creat de Cristian Farcas”)**
   - Textul de pornire și subtitlul afișat sunt: **`GPS · KML · creat de Cristian Farcas`**.

5. **Icoană de filtrare și căutare avansată în toate atributele (Filtru stânga)**
   - Butonul **Filtru** din stânga permite căutarea oricărei fracțiuni de text (RO, nume fermier, număr cerere, cultură etc.) în toate parcelele din KML.

6. **Iconiță personalizată pentru aplicație pe telefon (`icon-*.png`)**
   - Scriptul **`generate_icons.py`** (plasat în rădăcina proiectului pe GitHub) generează iconițe native Android (obiectiv foto + poligon KML verde-emerald + pin GPS roșu), care se integrează automat în APK la compilarea cu GitHub Actions.

---

## 2. Structura fișierelor din proiect (GitHub)

```
/
├── index.html                     # Aplicația web completă (HTML + CSS + JS, Leaflet, KML Parser, Foto EXIF)
├── MainActivity.java              # Codul Java nativ pentru Capacitor Bridge (Android Intent + Stocare DCIM)
├── write_main.py                  # Script de build pentru copierea MainActivity.java și a iconițelor în Android
├── generate_icons.py              # Script Python pentru generarea iconițelor aplicației în toate rezoluțiile
├── capacitor.config.json          # Configurare Capacitor 6
├── package.json                   # Dependențe NPM
├── privacy.html                   # Politica de confidențialitate
├── README.md                      # Documentație proiect
└── .github/
    └── workflows/
        └── build-apk.yml          # Workflow automat GitHub Actions pentru compilarea APK Android
```

---

## 3. Instrucțiuni de lucru

### A. Căutare după orice atribut (Birou / Teren)
- Apăsați butonul **Filtru** din stânga.
- Tastați orice parte din ID-ul RO, din numele fermierului sau din cerere.
- Alegeți parcela dorită din rezultate: harta o centrează automat pe ecran.

### B. Fotografiere cu 6 rânduri independente și EXIF
- Deschideți **Camera** -> realizați fotografia.
- Verificați pre-vizualizarea pe 6 rânduri clare, aliniate la stânga (fără suprapuneri).
- Apăsați **Salvează**: poza ajunge în folderul **`DCIM/ROPhotoKml/`** din telefon, având inscripționat textul pe imagine și coordonatele GPS în metadatele **EXIF**.
