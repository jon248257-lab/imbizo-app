[app]
title = Imbizo
package.name = imbizo
package.domain = org.jontech
source.dir =.
source.include_exts = py,json,xlsx
version = 1.0
requirements = python3,kivy
orientation = portrait
#icon.filename = %(source.dir)s/icon.png
android.permissions = SEND_SMS,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.sdk_path =
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
