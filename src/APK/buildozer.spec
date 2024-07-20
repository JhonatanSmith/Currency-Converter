[app]
# (str) Title of your application
title = ScraperApp

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 31

# (str) Android API to use
android.api = 31

# (str) Package name
package.name = scraperapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yourname

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,requests,beautifulsoup4,pandas,lxml

# (str) Supported orientation (one of "landscape", "portrait" or "all")
orientation = portrait

# OS specific
osx.python_version = 3
osx.kivy_version = 1.11.1
