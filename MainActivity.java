# Soluție completă pentru eroarea **`cp: cannot stat 'MainActivity.java': No such file or directory`**

Eroarea apăreze când script‑ul Bash încearcă să copie `MainActivity.java` dintr-un director unde nu există niciun fișier cu acest nume. Pentru a rezolva problema trebuie să:

1. **Verificați existența fișierului** în cadrul proiectului Android.
2. **Creadați sau mutați fișierul** în locul așteptat.
3. **Actualizați calea** în script dacă fișierul se află într‑un alt director.
4. **Verificați structura proiectului** generat de Capacitor/React/Other framework.

## 1. Verificați structura proiectului

Calea indicată în comanda este:

```
android/app/src/main/java/ro/rophotokml/app/MainActivity.java
```

În majoritatea proiectelor **Capacitor** (sau **React‑Capacitor**) structura este:

```
android/
 └─ app/
     └─ src/
         └─ main/
             └─ java/
                 └─ (pachetul tău, de ex.: ro/rophotokml/app/)
                     └─ MainActivity.java
```

Dacă nu găsiți `MainActivity.java` în acel folder, poate fi:

* **Numele pachetului este diferit** (de exemplu `com.getcapacitor.app`).
* **Fișierul a fost șters accidental**
* **Proiectul a fost creat cu alte setări (ex.: Angular, Vue)**

### Pasul de verificare rapid

Deschideți un terminal în rădăcina proiectului și rulați:

```bash
find android -type f -name "MainActivity.java"
```

Acesta va întoarce calea completă dacă fișierul există. Dacă nu afișează nimic, aceasta confirmă lipsa fișierului.

## 2. Crearea fișierului `MainActivity.java`

Există două approacţi:

### A. Crearea manuală (recomandată dacă doriţi să aveţi un `MainActivity` simplu)

Crearea unui fișier gol cu conţinutul necesar:

```bash
mkdir -p android/app/src/main/java/ro/rophotokml/app

cat > android/app/src/main/java/ro/rophotokml/app/MainActivity.java <<'EOF'
package ro.rophotokml.app;

// (Copieţi aici conţinutul complet din promptul anterior)
// Este important să păstraţi toate import‑urile și metoda onCreate.
// Dacă aţi modificat pachetul sau alte clase, adaptaţi-le conform necesităţii.
EOF
```

> **Notă**: În loc de `ro.rophotokml.app` puteţi folosi pachetul real al proiectului (de ex. `com.getcapacitor.app` dacă aţi schimbat în `AndroidManifest.xml`). Dacă pachetul este `com.getcapacitor.app`, schimbaţi toate aparţiţiile din codul de mai jos cu acest pachet.

### B. Copierea dintr‑o copie temporară (dacă aveţi backup)

Dacă aveţi o copie a proiectului anterior, copiaţi fișierul din acolo:

```bash
# Exemplu – dacă aveţi backup în directorul `backup/`
cp backup/android/app/src/main/java/ro/rophotokml/app/MainActivity.java \
   android/app/src/main/java/ro/rophotokml/app/
```

## 3. Executarea din nou comenzii `cp`

După ce aţi garantat existența fișierului, rulajul:

```bash
cp MainActivity.java android/app/src/main/java/ro/rophotokml/app/MainActivity.java
```

va funcţiona fără eroare.

> **Dacă comanda este parte dintr‑un script mai mare**, asiguraţi-vă că rulaţi scriptul din directorul rădăcină al proiectului, unde fişierul `MainActivity.java` este accesibil.

## 4. Cod complet și corect (pentru copiați în `MainActivity.java`)

Iată versiunea completă a fişierului, cu commentarii pentru a vă asigura că totul este în ordine. Copiaţi tot conţinutul în `android/app/src/main/java/ro/rophotokml/app/MainActivity.java`.

```java
package ro.rophotokml.app;

import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.content.ContentValues;
import android.content.ContentResolver;
import android.provider.MediaStore;
import android.util.Base64;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.File;
import java.io.FileOutputStream;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Adăugăm interfac şi interfac JavaScript
        getBridge().getWebView().addJavascriptInterface(new NativeBridge(), "AndroidApp");
        // Dăuim timp WebView‑ului să se iniţializeze înainte de manipularea Intent‑ului
        getBridge().getWebView().postDelayed(() -> handleIntent(getIntent()), 2000);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        getBridge().getWebView().postDelayed(() -> handleIntent(intent), 1000);
    }

    /**
     * Procesează Intent‑ul primit de la sistem (de ex. open KML, share photo etc.)
     */
    private void handleIntent(Intent intent) {
        if (intent == null) return;

        Uri data = intent.getData();
        // Dacă utilizatorul a selectat mai multe elemente
        if (data == null && intent.getClipData() != null) {
            data = intent.getClipData().getItemAt(0).getUri();
        }
        if (data == null) return;

        String action = intent.getAction();
        // Acceptă doar ACTION_VIEW (deschidere) sau ACTION_SEND (share)
        if (!Intent.ACTION_VIEW.equals(action) && !Intent.ACTION_SEND.equals(action)) return;

        try {
            final String fileName = getFileName(data);
            final String content = readTextFromUri(data);
            if (content == null || fileName == null) return;

            // Trimitem JavaScript la WebView cu datele
            getBridge().getWebView().post(() -> {
                // Escape‑im caracterele care pot rupe sintaxa JavaScript
                String escaped = content
                        .replace("\\", "\\\\")
                        .replace("'", "\\'")
                        .replace("\r", "")
                        .replace("\n", "\\n");
                String fnEsc = fileName.replace("'", "\\'");
                String js = "setTimeout(function(){if(typeof window.openKMLFromIntent==='function'){"
                        + "window.openKMLFromIntent('" + fnEsc + "','" + escaped + "');}},500);";
                getBridge().getWebView().evaluateJavascript(js, null);
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Extrage numele fişierului din Uri.
     * Funcționează pentru scheme `content://` (ex.: Gutsy) şi `file://`.
     */
    private String getFileName(Uri uri) {
        String result = null;
        if ("content".equals(uri.getScheme())) {
            try (Cursor cursor = getContentResolver()
                    .query(uri, null, null, null, null)) {
                if (cursor != null && cursor.moveToFirst()) {
                    int idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                    if (idx >= 0) result = cursor.getString(idx);
                }
            } catch (Exception ignored) {}
        }
        if (result == null) result = uri.getLastPathSegment();
        return result;
    }

    /**
     * Citim tot conţinţiul dintr‑un Uri ca String (UTF‑8).
     */
    private String readTextFromUri(Uri uri) {
        try (InputStream is = getContentResolver().openInputStream(uri)) {
            if (is == null) return null;
            BufferedReader reader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) sb.append(line).append("\n");
            return sb.toString();
        } catch (Exception e) { return null; }
    }

    /**
     * Reversă comportamentul back pe Android.
     * Dacă funcţia JavaScript `onAndroidBack` nu returnează "ok",
     * apoi se apelează metoda super.
     */
    @Override
    public void onBackPressed() {
        getBridge().getWebView().evaluateJavascript(
                "if(typeof window.onAndroidBack==='function'){window.onAndroidBack();'ok';}else{'no';}",
                val -> {
                    if (val == null || !val.contains("ok")) {
                        runOnUiThread(() -> MainActivity.super.onBackPressed());
                    }
                }
        );
    }

    /* ------------------------------------------------------------------ */
    /*  Clasa internă – bridge cu JavaScript                               */
    /* ------------------------------------------------------------------ */
    public class NativeBridge {

        /**
         * Salvează o imagine (baza64) în directorul DCIM/ROPhotoKml.
         *
         * @param b64  imaginea în formatul dataURL (base64)
         * @param fn   numele de salvare (ex.: "parcela1_12345.jpg")
         * @return     mesaj de succes sau eroare în format "OK:path" / "ERROR:msg"
         */
        @JavascriptInterface
        public String savePhoto(String b64, String fn) {
            try {
                byte[] bytes = Base64.decode(b64, Base64.DEFAULT);

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    // Android 10+ – Folosește MediaStore cu RELATIVE_PATH
                    ContentResolver r = getContentResolver();
                    ContentValues v = new ContentValues();
                    v.put(MediaStore.Images.Media.DISPLAY_NAME, fn);
                    v.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg");
                    v.put(MediaStore.Images.Media.RELATIVE_PATH, "DCIM/ROPhotoKml");
                    v.put(MediaStore.Images.Media.IS_PENDING, 1);

                    Uri u = r.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, v);
                    if (u == null) return "ERROR:insert";

                    try (OutputStream o = r.openOutputStream(u)) {
                        o.write(bytes);
                    }
                    v.clear();
                    v.put(MediaStore.Images.Media.IS_PENDING, 0);
                    r.update(u, v, null, null);
                    return "OK:" + u.toString();
                } else {
                    // Versiuni < 10 – Folosește sistemul de stocare extern
                    File d = new File(android.os.Environment.getExternalStorageDirectory(),
                            "DCIM/ROPhotoKml");
                    if (!d.exists()) d.mkdirs();
                    File file = new File(d, fn);
                    try (FileOutputStream fos = new FileOutputStream(file)) {
                        fos.write(bytes);
                    }
                    // Notificăm sistemul să reconsultă fişierul
                    sendBroadcast(new android.content.Intent(
                            android.content.Intent.ACTION_MEDIA_SCANNER_SCAN_FILE,
                            Uri.fromFile(file)));
                    return "OK:" + file.getAbsolutePath();
                }
            } catch (Exception e) {
                return "ERROR:" + e.getMessage();
            }
        }

        /**
         * Inchide aplicaţia (folosit de la JavaScript prin `window.exitApp()`).
         */
        @JavascriptInterface
        public void exitApp() {
            finishAffinity();
        }
    }
}
```

### Ce trebuie să verificaţi în acest cod:

| Element | Ce trebuie să fie corect |
|---------|--------------------------|
| `package ro.rophotokml.app;` | Să corespund pachetului definit în `AndroidManifest.xml`. Dacă pachetul este altul, schimbaţi la începutul fişierului. |
| `import com.getcapacitor.BridgeActivity;` | Este corect pentru proiectele care folosesc **Capacitor**. Dacă folosiţi **Capacitor 6** sau **Capacitor 7**, import‑ul rămâne acelaşi. |
| `getBridge().getWebView()` | Este valid pentru orice versiune de Capacitor care păstrează metoda `getBridge()`. |
| `handleIntent()` | Funcționează doar dacă aţi declara în `AndroidManifest.xml` activity‑a ca `android:exported="true"` (pentru API‑le 31+). Dacă nu aveţi acea linie, adăugaţi: <br>`<activity ... android:exported="true">` |
| `android:requestLegacyExternalStorage="true"` | Dacă veţi scrie în `getExternalStorageDirectory()` (Android < 10), adăugaţi această atribut în manifest. |
| `android:theme="@style/LaunchTheme"` | Asigură‑vă că tema este setată corect în manifest, altfel aplicaţia va cringe la start. |

## 5. Pas cu pas – recomandări pentru a evita acea eroare în viitor

| Pas | Descriere |
|-----|-----------|
| **1. Pregătiți proiectul** | rulează `npm install` sau `yarn install` pentru a descărca dependenţele. |
| **2. Porniţi serverul de dezvoltare** | `npm run build` sau `ionic capacitor add android && ionic capacitor sync` (depinde de fluxul vostru). |
| **3. Verificaţi existența fişierului** | După build, deschideţi folderul `android/app/src/main/java/...` și căutaţi `MainActivity.java`. |
| **4. Dacă lipseşte – creează-l** | Foloseşte scriptul de mai sus pentru a genera conţinutul. |
| **5. Rulează din nou** | `ionic capacitor copy && ionic capacitor run android` (sau `npx cap sync android`). |
| **6. Testă** | Deschideţi aplicaţia pe dispozitiv și testează funcţia **Open KML** şi **Save Photo**. |

## 6. Ce faceți dacă vreţi să generaţi automat `MainActivity.java` din un template

Dacă preferaţi să nu copieţi manual, puteţi genera codul cu `cat` sau cu un script:

```bash
cat > android/app/src/main/java/ro/rophotokml/app/MainActivity.java <<'EOF'
package ro.rophotokml.app;

import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.content.ContentValues;
import android.content.ContentResolver;
import android.provider.MediaStore;
import android.util.Base64;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.File;
import java.io.FileOutputStream;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getBridge().getWebView().addJavascriptInterface(new NativeBridge(), "AndroidApp");
        getBridge().getWebView().postDelayed(() -> handleIntent(getIntent()), 2000);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        getBridge().getWebView().postDelayed(() -> handleIntent(intent), 1000);
    }

    private void handleIntent(Intent intent) {
        if (intent == null) return;
        Uri data = intent.getData();
        if (data == null && intent.getClipData() != null) {
            data = intent.getClipData().getItemAt(0).getUri();
        }
        if (data == null) return;
        String action = intent.getAction();
        if (!Intent.ACTION_VIEW.equals(action) && !Intent.ACTION_SEND.equals(action)) return;
        try {
            final String fileName = getFileName(data);
            final String content = readTextFromUri(data);
            if (content == null || fileName == null) return;
            getBridge().getWebView().post(() -> {
                String escaped = content
                        .replace("\\", "\\\\")
                        .replace("'", "\\'")
                        .replace("\r", "")
                        .replace("\n", "\\n");
                String fnEsc = fileName.replace("'", "\\'");
                String js = "setTimeout(function(){if(typeof window.openKMLFromIntent==='function'){"
                        + "window.openKMLFromIntent('" + fnEsc + "','" + escaped + "');}},500);";
                getBridge().getWebView().evaluateJavascript(js, null);
            });
        } catch (Exception e) {
