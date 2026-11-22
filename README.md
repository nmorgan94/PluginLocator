# PluginLocator

One Finder folder with links to everything you need when testing your own audio plugins in a DAW.

## Why it exists

When you test a new plugin feature or installer, the files that matter are scattered across the Mac: build output deep inside each project, installed copies in two different Library folders, and presets in Application Support. Finding them wastes time, and it is easy to end up testing a stale copy without noticing.

Running `pl` builds a `PluginLocator` folder and opens it in Finder. It has three sections that twist open in list view:

| Folder | What it shows |
|---|---|
| **Builds** | Each built AU and VST3 in your project folders, named by build, e.g. `Debug - VST3`, `Release (webview) - AU` |
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

- **The built file names the plugin.** A built `Drums.vst3` is listed as `Drums`, together with the installed `Drums.vst3` and the presets folder `Drums/Presets`. There is no name to configure, so renaming a plugin needs no config change: rebuild and run `pl` again.
- **Build folders start with `build`** and sit at the top of the project: `<project>/build*/<Target>_artefacts/<Debug or Release>/<AU or VST3>/`.
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

**List your project folders.** Every plugin built in them is shown. Comment a line out to hide that project while you work on something else.

```python
PROJECTS = [
    "~/Source/MyPlugin",
    # "~/Source/MyOtherPlugin",
]
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

- **A project appears only once it has been built.** The plugin's name comes from the built files, so a project with no AU or VST3 build yet shows nothing.
- **Old builds show up too.** Anything left in a build folder is listed, including plugins from before a rename. Treat an unexpected entry as a reminder to delete the stale build.
- **The folder is rebuilt on every run.** New builds, installs and presets appear only after running `pl` again.
- **Don't store files in the `PluginLocator` folder.** It only holds links. A preset dragged in there does not reach the plugin.
- **Deleting a link does not uninstall anything.** To remove an installed plugin, press Cmd + R on its link and delete the original.
- **Each run clears the `PluginLocator` folder's links.** It removes every link and every empty folder inside `PluginLocator`, including any you added yourself, then recreates its own. It never touches the files the links point to, and real files inside the folder are left alone.

## Troubleshooting

- **`no built AU or VST3 found in "..."`**: the project folder is wrong, or it hasn't been built yet.
- **`"..." already exists, so this was left out`**: two builds would have had the same link name, usually because a stale copy of a plugin is sitting in another build folder or another project. The first is linked; the message names the one that isn't. Delete the stale build.
- **A plugin is missing from Installed Plugins**: its bundle identifier doesn't start with anything in `PLUGIN_IDS`.
- **`problem in config.py`**: usually a missing quote, comma or pair of square brackets. Compare with `config.example.py`.
