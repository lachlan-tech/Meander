package com.example.meanderapp

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.webkit.WebView
import android.net.http.HttpResponseCache

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val myWebView: WebView = findViewById(R.id.webView)
        myWebView.loadUrl("http://meandersuite.com")
        myWebView.settings.javaScriptEnabled = true
        myWebView.clearCache(true)
    }
}