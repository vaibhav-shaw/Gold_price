[app]
title = Kanchan Jewellers
package.name = kanchanjewellers
package.domain = com.kanchanjewellers

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 2.1
requirements = python3,kivy,kivymd,pandas

[buildozer]
log_level = 2

[app]
icon.filename = icon.png
presplash.filename = presplash.png

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

[buildozer]
warn_on_root = 1