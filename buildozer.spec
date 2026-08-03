[app]
title = IMBIZO
package.name = drdigital
package.domain = org.jontech
source.dir =.
source.include_exts = py,json,xlsx
version = 1.0
requirements = python3,kivy,openpyxl,reportlab
orientation = portrait
#icon.filename = %(source.dir)s/icon.png
android.permissions = SEND_SMS,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
