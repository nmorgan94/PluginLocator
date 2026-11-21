# PluginLocator

One Finder folder with links to everything you need when testing your own audio plugins in a DAW.

## Why it exists

When you test a new plugin feature or installer, the files that matter are scattered across the Mac: build output deep inside each project, installed copies in two different Library folders, and presets in Application Support. Finding them wastes time, and it is easy to end up testing a stale copy without noticing.

Running `pl` builds a `PluginLocator` folder and opens it in Finder. It has three sections that twist open in list view:

| Folder | What it shows |
|---|---|
| **Builds** | Each built AU and VST3 in the plugin's project, named by build, e.g. `Debug - VST3`, `Release (webview) - AU` |
| **Installed Plugins** | Each installed copy, e.g. `User - VST3`, `System - AU` |
| **Presets** | The plugin's saved preset files |

Everything inside is a link to the real file. Select a link and press Cmd + R to jump to the original.

Build links are named after the build type, plus whatever is distinctive in the build folder's name:

| Build folder | Link name |
|---|---|
| `build-debug` | `Debug - VST3` |
| `build-release` | `Release - VST3` |
| `build-webview` | `Release (webview) - VST3` |
| `build` | `Debug (build) - VST3` or `Release (build) - VST3` |

## Requirements

- macOS
- Python 3.9 or newer (the one that ships with macOS is fine); nothing else to install
- Plugins built with JUCE and CMake

It also expects each plugin to follow these conventions:

- **One name everywhere.** The CMake target, the built file, the installed file and the presets folder all use the same name, e.g. `Drums_artefacts`, `Drums.vst3`, `Drums/Presets`. A plugin whose product name differs from its target name is not found.
- **Build folders start with `build`** and sit at the top of the project: `<project>/build*/<Name>_artefacts/<Debug or Release>/<AU or VST3>/`.
- **Presets are stored as `<folder>/<Name>/Presets`.**

Projucer and Xcode build folders are not scanned, and only AU and VST3 are listed.

## Setup

1. Clone the repository anywhere.
2. Copy `config.example.py` to `config.py` and edit it (see below). `config.py` is ignored by git, so your paths stay private.
3. Add an alias to `~/.zshrc`, using the path you cloned to, then open a new terminal:

   ```zsh
   alias pl='~/Source/PluginLocator/pluginlocator.py'
   ```

4. Run `pl`.

## Configuration

All settings are in `config.py`. Run `pl` again after editing.

**Choose which plugins to show.** Each line is a plugin's name and its project folder. Comment a line out to hide that plugin while you work on something else.

```python
PLUGINS = {
    "MyPlugin": "~/Source/MyPlugin",
    # "MyOtherPlugin": "~/Source/MyOtherPlugin",
}
```

**Say which installed plugins are yours.** Only plugins whose bundle identifier starts with one of these are listed, so a third-party plugin that happens to share a name is never shown.

```python
PLUGIN_IDS = ["com.MyCompany."]
```

**Say where presets live.**

```python
PRESETS = ["~/Library/Application Support/MyCompany"]
```

`config.py` is Python, so keep the quotes and the comma at the end of each line.

## Things to know

- **The folder is rebuilt on every run.** New builds, installs and presets appear only after running `pl` again.
- **Don't store files in the `PluginLocator` folder.** It only holds links. A preset dragged in there does not reach the plugin.
- **Deleting a link does not uninstall anything.** To remove an installed plugin, press Cmd + R on its link and delete the original.
- **Each run clears the `PluginLocator` folder's links.** It removes every link and every empty folder inside `PluginLocator`, including any you added yourself, then recreates its own. It never touches the files the links point to, and real files inside the folder are left alone.

## Troubleshooting

- **`nothing found for "Name"`**: the name in `config.py` doesn't match the plugin. Check spelling and capitals against the built file, e.g. `Name.vst3`.
- **`"..." already exists, so this was left out`**: two things would have had the same link name, usually two plugins in one build's `AU` or `VST3` folder after a rename. The first is linked; the message names the one that isn't. Delete the stale one from the build folder.
- **A plugin is missing from Installed Plugins**: its bundle identifier doesn't start with anything in `PLUGIN_IDS`.
- **`problem in config.py`**: usually a missing quote, comma or pair of square brackets. Compare with `config.example.py`.
