"""
Simple WebView wrapper for Android
This creates a native app that loads your Streamlit web app
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.garden.webview import WebView

class KanchanWebViewApp(App):
    def build(self):
        # Replace with your deployed Streamlit app URL
        webview = WebView(url='https://your-streamlit-app-url.streamlit.app')
        return webview

if __name__ == '__main__':
    KanchanWebViewApp().run()