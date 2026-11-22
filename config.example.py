# PluginLocator settings. Copy this file to config.py and edit it, then run
# `pl`. Run it again after every change.

# Your plugin project folders, one per line. The plugins shown are whatever
# has been built there: each built Name.vst3 or Name.component is listed as
# "Name", along with installed copies and presets of the same name.
# Comment a line out to hide that project for now.
PROJECTS = [
    "~/Source/MyPlugin",
    # "~/Source/MyOtherPlugin",
]

# Which installed plugins are yours: only plugins whose bundle identifier
# starts with one of these are listed under Installed Plugins.
PLUGIN_IDS = [
    "com.MyCompany.",
]

# Folders that hold <Name>/Presets for each plugin. Listed under Presets.
PRESETS = [
    "~/Library/Application Support/MyCompany",
]
