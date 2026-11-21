#!/usr/bin/env python3
"""PluginLocator: builds a folder of links for audio plugin development and opens
it in Finder. Which plugins to show is set in config.py, next to this script.
The folder is rebuilt from scratch on every run."""

import os
import plistlib
import runpy
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HUB = HERE / "PluginLocator"

# Link name -> where macOS keeps that kind of installed plugin.
INSTALLED = {
    "User - AU": "~/Library/Audio/Plug-Ins/Components",
    "User - VST3": "~/Library/Audio/Plug-Ins/VST3",
    "System - AU": "/Library/Audio/Plug-Ins/Components",
    "System - VST3": "/Library/Audio/Plug-Ins/VST3",
}

# Build output folder -> the kind of file a built plugin is.
BUILD_FORMATS = {"AU": ".component", "VST3": ".vst3"}

# What each setting in config.py must be.
SETTINGS = {
    "PLUGINS": (dict, "a dictionary in curly brackets, { }"),
    "PLUGIN_IDS": (list, "a list in square brackets, [ ]"),
    "PRESETS": (list, "a list in square brackets, [ ]"),
}

found = set()  # names of the plugins that something was found for


def warn(message):
    print(f"pluginlocator: {message}", file=sys.stderr)


def read_config():
    """Load config.py and return (plugins, plugin ids, preset folders)."""
    if not (HERE / "config.py").exists():
        sys.exit("pluginlocator: no config.py yet. Copy config.example.py to "
                 f"config.py in {HERE} and edit it.")
    try:
        config = runpy.run_path(str(HERE / "config.py"))
        for setting, (kind, description) in SETTINGS.items():
            if not isinstance(config.get(setting), kind):
                raise ValueError(f"{setting} must be {description}")
        plugins = {name: Path(folder).expanduser() for name, folder in config["PLUGINS"].items()}
        preset_dirs = [Path(folder).expanduser() for folder in config["PRESETS"]]
        return plugins, tuple(config["PLUGIN_IDS"]), preset_dirs
    except Exception as error:
        sys.exit(f"pluginlocator: problem in config.py: {error}\n"
                 "Compare it with config.example.py.")


def link(section, plugin, name, target):
    """Make the link <section>/<plugin>/<name> pointing to `target`. If the
    name is already taken by something else, keep the first and say what was
    left out."""
    found.add(plugin)
    path = HUB / section / plugin / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not os.path.lexists(path):
        path.symlink_to(target)
    elif not path.is_symlink() or os.readlink(path) != str(target):
        warn(f'"{path.relative_to(HUB)}" already exists, so this was left out: {target}')


def clean():
    """Delete every link in the hub, then any folder left empty. Only links
    are deleted, never real files (apart from Finder's .DS_Store in a folder
    that is otherwise empty)."""
    HUB.mkdir(exist_ok=True)
    for folder, _, _ in os.walk(HUB, topdown=False):
        folder = Path(folder)
        for entry in folder.iterdir():
            if entry.is_symlink():
                entry.unlink()
        if folder != HUB and all(p.name == ".DS_Store" for p in folder.iterdir()):
            (folder / ".DS_Store").unlink(missing_ok=True)
            folder.rmdir()


def bundle_id(bundle):
    try:
        info = plistlib.loads((bundle / "Contents/Info.plist").read_bytes())
        return info.get("CFBundleIdentifier", "")
    except Exception:
        return ""


# Each section below lists what is really on disk and compares names itself,
# so a plugin's name has to match exactly, capitals included. (Asking a Mac
# disk for a path by name would ignore capitals.)

def link_installed(plugins, ids):
    """Installed Plugins/<Plugin>/"User - VST3" etc. Only plugins that are
    listed in config.py and whose bundle identifier starts with a plugin id."""
    for label, folder in INSTALLED.items():
        for bundle in Path(folder).expanduser().glob("*"):
            if bundle.stem in plugins and bundle_id(bundle).startswith(ids):
                link("Installed Plugins", bundle.stem, label, bundle)


def link_presets(plugins, preset_dirs):
    """Presets/<Plugin>/<preset files>, from <presets folder>/<Plugin>/Presets."""
    for root in preset_dirs:
        for presets in root.glob("*/Presets"):
            plugin = presets.parent.name
            if plugin not in plugins or not presets.is_dir():
                continue
            # Show the plugin even if it has no presets saved yet.
            (HUB / "Presets" / plugin).mkdir(parents=True, exist_ok=True)
            found.add(plugin)
            for file in presets.rglob("*"):
                inside = file.relative_to(presets)
                if not any(part.startswith(".") for part in inside.parts) and file.is_file():
                    link("Presets", plugin, inside, file)


def link_builds(plugins):
    """Builds/<Plugin>/"Debug - VST3" etc, from the CMake output
    <project>/build*/<Plugin>_artefacts/<Debug or Release>/<AU or VST3>/."""
    for plugin, project in plugins.items():
        if not project.is_dir():
            warn(f'project folder "{project}" for {plugin} does not exist')
        for bundle in sorted(project.glob("build*/*_artefacts/*/*/*.*")):
            build_dir, artefacts, build_type, fmt = bundle.relative_to(project).parts[:4]
            if artefacts != f"{plugin}_artefacts":  # another target
                continue
            if bundle.suffix != BUILD_FORMATS.get(fmt):  # not a built plugin
                continue
            # What is special about the build folder: build-webview-debug ->
            # "webview", build-release -> nothing, plain build -> "build".
            variant = build_dir
            if build_dir != "build":
                variant = build_dir.removeprefix("build")
                if variant.lower().endswith(build_type.lower()):
                    variant = variant[: -len(build_type)]
                variant = variant.strip("-")
            label = f"{build_type} ({variant})" if variant else build_type
            link("Builds", plugin, f"{label} - {fmt}", bundle)


plugins, ids, preset_dirs = read_config()
clean()
link_installed(plugins, ids)
link_presets(plugins, preset_dirs)
link_builds(plugins)
for plugin in plugins:  # a listed plugin that matched nothing is probably a typo
    if plugin not in found:
        warn(f'nothing found for "{plugin}". Check the name and capitals in config.py.')
subprocess.run(["open", HUB])
