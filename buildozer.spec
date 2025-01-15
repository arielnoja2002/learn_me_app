[app]

# (str) Title of your application
title = MyKivyApp

# (str) Package name
package.name = mykivyapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,mp3

# (list) List of inclusions using pattern matching
source.include_patterns = data/*,config/*,*.jpg

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements - specify exact versions for offline use
requirements = python3,kivy==2.2.1,pillow==10.0.0,sdl2_ttf==2.0.15,sdl2_image==2.0.5,sdl2_mixer==2.0.0

# (list) Garden requirements - specify exact versions
garden_requirements =

# (str) Presplash of the application - using the same icon.jpg for presplash
presplash.filename = %(source.dir)s/icon.jpg

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.jpg

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = True

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# Android permissions
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (bool) Skip byte compile for .py files
android.no-byte-compile-python = False

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk

# (str) Application android style - material, android or system default
android.appstyle = material

# (list) Gradle dependencies to add
android.gradle_dependencies =

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Application name for Android
android.title = %(title)s

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin

# Cache downloaded packages
cache_dir = ./.buildozer_cache

# (bool) If True, then automatically download and install missing dependencies
p4a.local_recipes =
