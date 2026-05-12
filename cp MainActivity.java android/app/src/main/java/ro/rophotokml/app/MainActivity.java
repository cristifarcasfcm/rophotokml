package ro.rophotokml.app;

import android.os.Bundle;
import android.os.Build;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.content.ContentValues;
import android.content.ContentResolver;
import android.net.Uri;
import android.provider.MediaStore;
import android.util.Base64;
import java.io.OutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.ByteArrayOutputStream;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Adauga JavascriptInterface dupa ce bridge-ul e creat
        getBridge().getWebView().addJavascriptInterface(new PhotoSaver(), "AndroidPhotoSaver");
    }

    public class PhotoSaver {

        @JavascriptInterface
        public String savePhoto(String base64Data, String filename) {
            try {
                // Decodifica base64
                byte[] imageBytes = Base64.decode(base64Data, Base64.DEFAULT);

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    // Android 10+ — foloseste MediaStore (apare direct in Galerie)
                    ContentResolver resolver = getContentResolver();
                    ContentValues values = new ContentValues();
                    values.put(MediaStore.Images.Media.DISPLAY_NAME, filename);
                    values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg");
                    values.put(MediaStore.Images.Media.RELATIVE_PATH, "DCIM/ROPhotoKml");
                    values.put(MediaStore.Images.Media.IS_PENDING, 1);

                    Uri uri = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
                    if (uri == null) return "ERROR: nu s-a putut crea intrarea in MediaStore";

                    try (OutputStream out = resolver.openOutputStream(uri)) {
                        out.write(imageBytes);
                    }

                    values.clear();
                    values.put(MediaStore.Images.Media.IS_PENDING, 0);
                    resolver.update(uri, values, null, null);
                    return "OK:" + uri.toString();

                } else {
                    // Android 9 si mai vechi — scrie in DCIM direct
                    File dir = new File(android.os.Environment.getExternalStorageDirectory(),
                            "DCIM/ROPhotoKml");
                    if (!dir.exists()) dir.mkdirs();
                    File file = new File(dir, filename);
                    FileOutputStream fos = new FileOutputStream(file);
                    fos.write(imageBytes);
                    fos.close();

                    // Notifica galeria
                    sendBroadcast(new android.content.Intent(
                            android.content.Intent.ACTION_MEDIA_SCANNER_SCAN_FILE,
                            Uri.fromFile(file)));
                    return "OK:" + file.getAbsolutePath();
                }

            } catch (Exception e) {
                return "ERROR:" + e.getMessage();
            }
        }
    }
}
