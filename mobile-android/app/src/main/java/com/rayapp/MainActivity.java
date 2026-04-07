package com.rayapp;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.webkit.ConsoleMessage;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class MainActivity extends AppCompatActivity {

    private static final int REQUEST_PERMISSIONS = 1;
    private static final String TAG = "RayApp";
    private WebView webView;
    private SwipeRefreshLayout swipeRefresh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webView);
        swipeRefresh = findViewById(R.id.swipeRefresh);

        // Configure WebView FIRST before loading content
        configureWebView();

        // Check and request permissions
        checkPermissions();

        // Pull to refresh
        swipeRefresh.setOnRefreshListener(() -> webView.reload());

        // Load local app
        webView.loadUrl("file:///android_asset/mobile/index.html");
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setJavaScriptCanOpenWindowsAutomatically(true);

        // Enable debugging
        WebView.setWebContentsDebuggingEnabled(true);

        // Add JavaScript Interface
        webView.addJavascriptInterface(new AndroidBridge(), "AndroidInterface");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                Log.d(TAG, "Page loaded: " + url);
                swipeRefresh.setRefreshing(false);
            }

            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                Log.e(TAG, "WebView error: " + description + " on " + failingUrl);
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                Log.d(TAG, "Permission request for: " + request.getOrigin());
                runOnUiThread(() -> {
                    String[] resources = request.getResources();
                    for (String resource : resources) {
                        Log.d(TAG, "Requested resource: " + resource);
                    }
                    request.grant(resources);
                });
            }

            @Override
            public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
                Log.d(TAG, "Console: " + consoleMessage.message() +
                        " -- From line " + consoleMessage.lineNumber() +
                        " of " + consoleMessage.sourceId());
                return true;
            }
        });
    }

    private void checkPermissions() {
        String[] permissions = {
            Manifest.permission.CAMERA,
            Manifest.permission.RECORD_AUDIO
        };

        boolean needRequest = false;
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                needRequest = true;
                break;
            }
        }

        if (needRequest) {
            ActivityCompat.requestPermissions(this, permissions, REQUEST_PERMISSIONS);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    // JavaScript Bridge for camera access
    public class AndroidBridge {
        @JavascriptInterface
        public void startQRScanner() {
            runOnUiThread(() -> {
                // For now, show a message that camera scanning requires
                // the web version or manual code entry
                webView.evaluateJavascript(
                    "alert('Por favor ingresa el codigo manualmente: RAY-XXXX');",
                    null
                );
            });
        }
    }
}
