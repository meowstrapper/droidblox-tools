package com.drake;

import com.drake.WVCCallback;

import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;

public class CustomWVC extends WebViewClient {
    public WVCCallback callback_wrapper;

    public CustomWVC(WCCCallback callback_wrapper) {
	    this.callback_wrapper = callback_wrapper;
    }

    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        String url = request.getUrl().toString();
	    this.callback_wrapper.shouldOverrideUrlLoading(url);
	    return false;
    }
}