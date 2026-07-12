[app]

# (str) Title of your application
title = SMS Forwarder

# (str) Package name
package.name = smsforwarder

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (str) Source code includes
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,pyjnius

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = READ_SMS,INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# iOS settings
[app:ios]
# (str) iOS framework to use
ios.kivy_ios_url = https://github.com/kivy/kivy-ios

# (str) iOS framework version
ios.kivy_ios_version = master

# (list) iOS requirements
requirements = python3,kivy

# (str) iOS development team ID (required for signing)
ios.team_id = 

# (str) iOS code signing identity
ios.codesign_identity = 
