import os, base64, shutil

ma = "android/app/src/main/java/ro/rophotokml/app/MainActivity.java"
os.makedirs(os.path.dirname(ma), exist_ok=True)

content = '''package ro.rophotokml.app;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.Build;
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
        handleIntent(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleIntent(intent);
    }

    private void handleIntent(Intent intent) {
        if (intent == null) return;
        String action = intent.getAction();
        Uri data = intent.getData();
        if (data == null && intent.getClipData() != null) {
            data = intent.getClipData().getItemAt(0).getUri();
        }
        if ((Intent.ACTION_VIEW.equals(action) || Intent.ACTION_SEND.equals(action)) && data != null) {
            try {
                String fileName = getFileName(data);
                String content = readTextFromUri(data);
                if (content != null && fileName != null) {
                    final String fn = fileName;
                    final String ct = content;
                    getBridge().getWebView().post(() -> {
                        String escaped = ct.replace("\\\\", "\\\\\\\\")
                            .replace("'", "\\\\'")
                            .replace("\\r", "")
                            .replace("\\n", "\\\\n");
                        String fnEsc = fn.replace("'", "\\\\'");
                        String js = "if(typeof window.openKMLFromIntent==='function'){" +
                            "window.openKMLFromIntent('" + fnEsc + "','" + escaped + "');}";
                        getBridge().getWebView().evaluateJavascript(js, null);
                    });
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private String getFileName(Uri uri) {
        String result = null;
        if ("content".equals(uri.getScheme())) {
            try (Cursor cursor = getContentResolver().query(uri, null, null, null, null)) {
                if (cursor != null && cursor.moveToFirst()) {
                    int idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                    if (idx >= 0) result = cursor.getString(idx);
                }
            } catch (Exception e) { e.printStackTrace(); }
        }
        if (result == null) result = uri.getLastPathSegment();
        return result;
    }

    private String readTextFromUri(Uri uri) {
        try {
            InputStream is = getContentResolver().openInputStream(uri);
            if (is == null) return null;
            BufferedReader reader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) sb.append(line).append("\\n");
            reader.close();
            return sb.toString();
        } catch (Exception e) { return null; }
    }

    @Override
    public void onBackPressed() {
        WebView wv = getBridge().getWebView();
        wv.evaluateJavascript(
            "if(typeof window.onAndroidBack==='function'){window.onAndroidBack();'ok';}else{'no';}",
            val -> { if(val==null||!val.contains("ok")){runOnUiThread(()->MainActivity.super.onBackPressed());} }
        );
    }

    public class NativeBridge {
        @JavascriptInterface
        public String savePhoto(String b64, String fn) {
            try {
                byte[] b = Base64.decode(b64, Base64.DEFAULT);
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    ContentResolver r = getContentResolver();
                    ContentValues v = new ContentValues();
                    v.put(MediaStore.Images.Media.DISPLAY_NAME, fn);
                    v.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg");
                    v.put(MediaStore.Images.Media.RELATIVE_PATH, "DCIM/ROPhotoKml");
                    v.put(MediaStore.Images.Media.IS_PENDING, 1);
                    Uri u = r.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, v);
                    if (u == null) return "ERROR:insert failed";
                    try (OutputStream o = r.openOutputStream(u)) { o.write(b); }
                    v.clear();
                    v.put(MediaStore.Images.Media.IS_PENDING, 0);
                    r.update(u, v, null, null);
                    return "OK:" + u.toString();
                } else {
                    File d = new File(android.os.Environment.getExternalStorageDirectory(), "DCIM/ROPhotoKml");
                    if (!d.exists()) d.mkdirs();
                    File f2 = new File(d, fn);
                    FileOutputStream fs = new FileOutputStream(f2);
                    fs.write(b); fs.close();
                    sendBroadcast(new android.content.Intent(
                        android.content.Intent.ACTION_MEDIA_SCANNER_SCAN_FILE, Uri.fromFile(f2)));
                    return "OK:" + f2.getAbsolutePath();
                }
            } catch (Exception e) { return "ERROR:" + e.getMessage(); }
        }

        @JavascriptInterface
        public void exitApp() { finishAffinity(); }
    }
}
'''

open(ma, 'w').write(content)
print("MainActivity.java written:", len(content), "chars")

# Copiaza iconitele in folderele Android corecte
icon_map = [
    ('icon-48.png',  'android/app/src/main/res/mipmap-mdpi/ic_launcher.png'),
    ('icon-72.png',  'android/app/src/main/res/mipmap-hdpi/ic_launcher.png'),
    ('icon-96.png',  'android/app/src/main/res/mipmap-xhdpi/ic_launcher.png'),
    ('icon-144.png', 'android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png'),
    ('icon-192.png', 'android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png'),
    # Round icons
    ('icon-48.png',  'android/app/src/main/res/mipmap-mdpi/ic_launcher_round.png'),
    ('icon-72.png',  'android/app/src/main/res/mipmap-hdpi/ic_launcher_round.png'),
    ('icon-96.png',  'android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.png'),
    ('icon-144.png', 'android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png'),
    ('icon-192.png', 'android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png'),
]

for src_name, dst_path in icon_map:
    if os.path.exists(src_name):
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy(src_name, dst_path)
        print(f"Icon: {src_name} -> {dst_path}")
    else:
        print(f"WARNING: {src_name} not found")
