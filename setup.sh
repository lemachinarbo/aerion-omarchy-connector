#!/bin/bash
set -e

HOOKS_DIR="$HOME/.config/omarchy/hooks"
THEME_SET_HOOK="$HOOKS_DIR/theme-set"

echo "Setting up Omarchy Integration for Aerion..."

# 1. Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# 2. Append hook logic to theme-set
if [ -f "$THEME_SET_HOOK" ]; then
    # Check if aerion hook is already installed
    if grep -q "aerion --theme-change" "$THEME_SET_HOOK"; then
        echo "Aerion hook is already installed in $THEME_SET_HOOK."
    else
        echo "Appending Aerion hook logic to existing theme-set hook..."
        echo "" >> "$THEME_SET_HOOK"
        cat theme-set.sample >> "$THEME_SET_HOOK"
    fi
else
    echo "Creating new theme-set hook..."
    cat theme-set.sample > "$THEME_SET_HOOK"
fi

# 3. Make hook executable
chmod +x "$THEME_SET_HOOK"

echo "Setup completed successfully! Make sure to run Aerion built from source."
