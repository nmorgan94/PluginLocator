# PluginLocator settings. Copy this file to config.py and edit it, then run
# `pl`. Run it again after every change.

# The plugins to show, as  "Name": "project folder".
# The name must be exactly the plugin's name (capitals included): the same
# name as the CMake target, the built file (Name.vst3) and the presets folder.
# Comment a line out to hide that plugin for now.
PLUGINS = {
    "MyPlugin": "~/Source/MyPlugin",
    # "MyOtherPlugin": "~/Source/MyOtherPlugin",
}

# Which installed plugins are yours: only plugins whose bundle identifier
# starts with one of these are listed under Installed Plugins.
PLUGIN_IDS = [
    "com.MyCompany.",
]

# Folders that hold <Name>/Presets for each plugin. Listed under Presets.
PRESETS = [
    "~/Library/Application Support/MyCompany",
]
