# Omarchy Integration for Aerion

This directory contains integration assets to enable seamless live theming between the Omarchy desktop theme switcher and Aerion.

## Contents

1. **`generate_themes.py`**: A helper script that reads colors from your local Omarchy configuration (`~/.config/omarchy/themes/`) and automatically builds the static `.css` stylesheets, registers them in Go (`internal/settings/store.go`), and updates Svelte settings (`settings.svelte.ts`/`GeneralTab.svelte`).
2. **`theme-set.sample`**: A sample hook script that handles automatic mappings (such as converting `nord` $\rightarrow$ `nord-dark`/`nord-light` based on the system's `light.mode` state) and triggers theme-changing command on running Aerion instances.

## How to Set Up Live Theming

1. **Enable the Hook**:
   Copy the contents of `theme-set.sample` into your local Omarchy hooks:
   ```bash
   cat theme-set.sample >> ~/.config/omarchy/hooks/theme-set
   chmod +x ~/.config/omarchy/hooks/theme-set
   ```

2. **Test Theme Synchronization**:
   Change your Omarchy theme (e.g., to `Kanagawa` or `Everforest`). Aerion will automatically and instantly update its UI to match!
