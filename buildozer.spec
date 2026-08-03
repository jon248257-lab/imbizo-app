[app]
title = IMBIZO
package.name = imbizo
package.domain = org.jontech
source.dir =.
source.include_exts = py,json,xlsx
source.include_patterns = modules/*,modules/**/*.py
version = 1.0.0
requirements = python3,kivy,openpyxl,reportlab,pillow,android
orientation = portrait
# icon.filename = %(source.dir)s/icon.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk_path = 
android.archs = arm64-v8a
android.gradle_dependencies = 
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
