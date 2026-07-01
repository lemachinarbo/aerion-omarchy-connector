# Omarchy Integration for Aerion

Assets to enable real-time theme synchronization between the Omarchy desktop environment and [Aerion](https://github.com/hkdb/aerion).



https://github.com/user-attachments/assets/18d12c22-135a-49a4-bb18-0dbcee25eb34



## Setup

### Step 1: Install Aerion
Since live theming support is in progress for upstream, you must build Aerion from the custom fork containing these changes:

```bash
git clone https://github.com/lemachinarbo/aerion.git
cd aerion
# Follow Aerion build instructions to compile and install
```

### Step 2: Enable the Hook (Quick Setup)
Run this one-liner to clone the connector and enable the theme sync hook:
```bash
git clone https://github.com/lemachinarbo/aerion-omarchy-connector.git && cd aerion-omarchy-connector && ./setup.sh
```

## Files

* **`theme-set.sample`**: A sample hook script that maps Omarchy themes to Aerion equivalents (e.g., handling dark/light variants for Nord and Catppuccin) and sends the update to running Aerion instances. It also updates `mako` notification colors to match the active theme.
* **`generate_themes.py`**: A helper script to generate CSS files, register new themes in Go (`internal/settings/store.go`), and expose them in Svelte (`settings.svelte.ts`/`GeneralTab.svelte`).
