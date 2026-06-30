#!/usr/bin/env python3
import os
import re
import colorsys

def hex_to_hsl_str(hex_str):
    hex_str = hex_str.lstrip('#').strip()
    if len(hex_str) == 3:
        hex_str = "".join(c*2 for c in hex_str)
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    r_f, g_f, b_f = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r_f, g_f, b_f)
    return f"{round(h * 360)} {round(s * 100)}% {round(l * 100)}%"

def get_luminance(hex_str):
    hex_str = hex_str.lstrip('#').strip()
    if len(hex_str) == 3:
        hex_str = "".join(c*2 for c in hex_str)
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return 0.2126 * (r/255.0) + 0.7152 * (g/255.0) + 0.0722 * (b/255.0)

def adjust_lightness(hex_str, target_l_percent):
    hex_str = hex_str.lstrip('#').strip()
    if len(hex_str) == 3:
        hex_str = "".join(c*2 for c in hex_str)
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    r_f, g_f, b_f = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r_f, g_f, b_f)
    return f"{round(h * 360)} {round(s * 100)}% {target_l_percent}%"

def parse_colors_toml(filepath):
    colors = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.match(r'^([a-zA-Z0-9_]+)\s*=\s*["\']?([^"\']+)["\']?', line)
            if match:
                key, val = match.groups()
                colors[key] = val
    return colors

def main():
    themes_dir = os.path.expanduser("~/.config/omarchy/themes")
    generated_themes = []

    labels = {
        "nord": "Nord",
        "everforest": "Everforest",
        "rose-pine": "Rose Pine",
        "tokyo-night": "Tokyo Night",
        "catppuccin": "Catppuccin",
        "catppuccin-latte": "Catppuccin Latte",
        "flexoki-light": "Flexoki",
        "flexoki-dark": "Flexoki",
        "gruvbox": "Gruvbox",
        "hackerman": "Hackerman",
        "kanagawa": "Kanagawa",
        "miasma": "Miasma",
        "ristretto": "Ristretto",
        "matte-black": "Matte Black",
        "vantablack": "Vantablack",
        "white": "White",
        "ethereal": "Ethereal",
        "lumon": "Lumon",
        "retro-82": "Retro 82",
        "osaka-jade": "Osaka Jade"
    }

    # Base native themes already registered in Aerion
    base_modes = [
        ("ThemeModeSystem", "system"),
        ("ThemeModeLight", "light"),
        ("ThemeModeLightBlue", "light-blue"),
        ("ThemeModeLightOrange", "light-orange"),
        ("ThemeModeLightBalanced", "light-balanced"),
        ("ThemeModeAdwaitaLight", "adwaita-light"),
        ("ThemeModeBreezeLight", "breeze-light"),
        ("ThemeModeDark", "dark"),
        ("ThemeModeDarkGray", "dark-gray"),
        ("ThemeModeDarkBalanced", "dark-balanced"),
        ("ThemeModeAdwaitaDark", "adwaita-dark"),
        ("ThemeModeBreezeDark", "breeze-dark"),
        ("ThemeModeCatppuccinLatte", "catppuccin-latte"),
        ("ThemeModeCatppuccinFrappe", "catppuccin-frappe"),
        ("ThemeModeCatppuccinMacchiato", "catppuccin-macchiato"),
        ("ThemeModeCatppuccinMocha", "catppuccin-mocha"),
        ("ThemeModeDracula", "dracula"),
        ("ThemeModeGithubLight", "github-light"),
        ("ThemeModeGithubDark", "github-dark"),
        ("ThemeModeGithubSoftDark", "github-soft-dark"),
        ("ThemeModeTokyoNight", "tokyo-night"),
        ("ThemeModeNordLight", "nord-light"),
        ("ThemeModeNordDark", "nord-dark"),
        ("ThemeModePopLight", "pop-light"),
        ("ThemeModePopDark", "pop-dark"),
        ("ThemeModeVSCodeLight", "vs-code-light"),
        ("ThemeModeVSCodeDark", "vs-code-dark"),
        ("ThemeModeYaruLight", "yaru-light"),
        ("ThemeModeYaruDark", "yaru-dark")
    ]
    
    native_values = {val for _, val in base_modes}

    # Add Flexoki Dark manually as well since it is upstreamable
    flexoki_dark = {
        "value": "flexoki-dark",
        "label": "Flexoki (Dark)",
        "is_dark": True,
        "bg": "#100F0F",
        "fg": "#CECDC3",
        "accent": "#3AA99F",
        "sel_bg": "#282726",
        "sel_fg": "#CECDC3",
        "c0": "#100F0F",
        "c1": "#D14D41",
        "c2": "#CECDC3",
        "c3": "#D0A215",
        "c4": "#205EA6",
        "c5": "#CE5D97",
        "c6": "#3AA99F",
        "c7": "#CECDC3",
        "c8": "#282726"
    }

    print("Scanning themes...")
    for item in sorted(os.listdir(themes_dir)):
        item_path = os.path.join(themes_dir, item)
        if not os.path.isdir(item_path):
            continue
        
        toml_path = os.path.join(item_path, "colors.toml")
        if not os.path.exists(toml_path):
            continue
        
        try:
            colors = parse_colors_toml(toml_path)
            bg = colors.get("background")
            fg = colors.get("foreground")
            accent = colors.get("accent", fg)
            
            if not bg or not fg:
                continue
                
            bg_lum = get_luminance(bg)
            is_dark = bg_lum < 0.5
            theme_name = item.lower().replace(" ", "-")
            
            # Skip if it is already natively supported in base_modes
            # or overlaps with pre-existing default themes (like nord, catppuccin, tokyo-night)
            if theme_name in native_values or theme_name in ["nord", "catppuccin", "tokyo-night", "catppuccin-latte"]:
                print(f"Skipping native theme duplicate: {theme_name}")
                continue
                
            if theme_name == "aether":
                print("Skipping non-official theme aether")
                continue
                
            label_base = labels.get(theme_name, item.replace("-", " ").title())
            if label_base.endswith(" Light"):
                label_base = label_base[:-6]
            elif label_base.endswith(" Dark"):
                label_base = label_base[:-5]
                
            suffix = " (Dark)" if is_dark else " (Light)"
            label = f"{label_base}{suffix}"

            theme_info = {
                "value": theme_name,
                "label": label,
                "is_dark": is_dark,
                "bg": bg,
                "fg": fg,
                "accent": accent,
                "sel_bg": colors.get("selection_background", colors.get("color8" if is_dark else "color0", bg)),
                "sel_fg": colors.get("selection_foreground", fg),
                "c0": colors.get("color0", bg),
                "c1": colors.get("color1", accent),
                "c2": colors.get("color2", fg),
                "c3": colors.get("color3", fg),
                "c4": colors.get("color4", fg),
                "c5": colors.get("color5", fg),
                "c6": colors.get("color6", fg),
                "c7": colors.get("color7", fg),
                "c8": colors.get("color8", colors.get("color0", bg))
            }
            generated_themes.append(theme_info)
            print(f"Parsed theme data for {theme_name}")
        except Exception as e:
            print(f"Failed to parse theme {item}: {e}")

    if flexoki_dark["value"] not in native_values:
        generated_themes.append(flexoki_dark)

    # Write separate CSS files for each theme
    import_statements = []
    for t in generated_themes:
        theme_name = t["value"]
        bg_hsl = hex_to_hsl_str(t["bg"])
        fg_hsl = hex_to_hsl_str(t["fg"])
        accent_hsl = hex_to_hsl_str(t["accent"])
        c1_hsl = hex_to_hsl_str(t["c1"])
        c2_hsl = hex_to_hsl_str(t["c2"])
        c3_hsl = hex_to_hsl_str(t["c3"])
        c4_hsl = hex_to_hsl_str(t["c4"])
        c5_hsl = hex_to_hsl_str(t["c5"])
        c6_hsl = hex_to_hsl_str(t["c6"])
        c7_hsl = hex_to_hsl_str(t["c7"])
        c8_hsl = hex_to_hsl_str(t["c8"])

        scheme = "dark" if t["is_dark"] else "light"
        sec_hsl = c8_hsl if t["is_dark"] else c7_hsl
        mut_hsl = c8_hsl if t["is_dark"] else c7_hsl
        sel_bg_hsl = hex_to_hsl_str(t["sel_bg"])
        sel_fg_hsl = hex_to_hsl_str(t["sel_fg"])
        
        # Convert bg/fg colors to HSL components to scale contrast properly
        bg_hex = t["bg"].lstrip('#')
        fg_hex = t["fg"].lstrip('#')
        if len(bg_hex) == 3: bg_hex = "".join(c*2 for c in bg_hex)
        if len(fg_hex) == 3: fg_hex = "".join(c*2 for c in fg_hex)
        bg_r, bg_g, bg_b = int(bg_hex[0:2], 16)/255.0, int(bg_hex[2:4], 16)/255.0, int(bg_hex[4:6], 16)/255.0
        fg_r, fg_g, fg_b = int(fg_hex[0:2], 16)/255.0, int(fg_hex[2:4], 16)/255.0, int(fg_hex[4:6], 16)/255.0
        _, bg_l, _ = colorsys.rgb_to_hls(bg_r, bg_g, bg_b)
        _, fg_l, _ = colorsys.rgb_to_hls(fg_r, fg_g, fg_b)
        
        bg_l_pct = bg_l * 100
        fg_l_pct = fg_l * 100
        
        if t["is_dark"]:
            mut_fg_l = round(bg_l_pct + 0.75 * (fg_l_pct - bg_l_pct))
            base_muted_hex = t["c8"]  # ANSI Bright Black (gray/slate/muted)
        else:
            mut_fg_l = round(bg_l_pct - 0.75 * (bg_l_pct - fg_l_pct))
            base_muted_hex = t["c0"]  # ANSI Black (dark gray)
            
        mut_fg_hsl = adjust_lightness(base_muted_hex, mut_fg_l)
 
        primary_hex = t["accent"]
        primary_hsl = accent_hsl
 
        # Compute foreground colors for primary and destructive (c1/red) buttons
        if t["is_dark"]:
            primary_fg_hsl = bg_hsl if get_luminance(primary_hex) > 0.5 else fg_hsl
            destructive_fg_hsl = bg_hsl if get_luminance(t['c1']) > 0.5 else fg_hsl
        else:
            primary_fg_hsl = fg_hsl if get_luminance(primary_hex) > 0.5 else bg_hsl
            destructive_fg_hsl = fg_hsl if get_luminance(t['c1']) > 0.5 else bg_hsl
 
        css_lines = [
            f"/* {t['label']} */",
            "@layer base {",
            f'  [data-theme="{theme_name}"] {{',
            f"    color-scheme: {scheme};",
            f"    --background: {bg_hsl};",
            f"    --foreground: {fg_hsl};",
            f"    --card: {bg_hsl};",
            f"    --card-foreground: {fg_hsl};",
            f"    --popover: {bg_hsl};",
            f"    --popover-foreground: {fg_hsl};",
            f"    --primary: {primary_hsl};",
            f"    --primary-foreground: {primary_fg_hsl};",
            f"    --secondary: {sec_hsl};",
            f"    --secondary-foreground: {fg_hsl};",
            f"    --muted: {mut_hsl};",
            f"    --muted-foreground: {mut_fg_hsl};",
            f"    --accent: {sel_bg_hsl};",
            f"    --accent-foreground: {sel_fg_hsl};",
            f"    --destructive: {c1_hsl};",
            f"    --destructive-foreground: {destructive_fg_hsl};",
            f"    --border: {sec_hsl};",
            f"    --input: {sec_hsl};",
            f"    --ring: {primary_hsl};",
            f"    --avatar-fg: {bg_hsl if t['is_dark'] else fg_hsl};",
            f"    --avatar-1:  {c1_hsl};",
            f"    --avatar-2:  {c2_hsl};",
            f"    --avatar-3:  {c3_hsl};",
            f"    --avatar-4:  {c4_hsl};",
            f"    --avatar-5:  {c5_hsl};",
            f"    --avatar-6:  {c6_hsl};",
            f"    --avatar-7:  {accent_hsl};",
            f"    --avatar-8:  {c7_hsl};",
            f"    --avatar-9:  {c8_hsl};",
            f"    --avatar-10: {c1_hsl};",
            f"    --avatar-11: {c2_hsl};",
            f"    --avatar-12: {c3_hsl};",
            f"    --avatar-13: {c4_hsl};",
            f"    --avatar-14: {c5_hsl};",
            "  }",
            "}"
        ]

        css_filepath = f"frontend/src/themes/{theme_name}.css"
        with open(css_filepath, "w") as f:
            f.write("\n".join(css_lines) + "\n")
        print(f"Created stylesheet: {css_filepath}")
        import_statements.append(f"@import './themes/{theme_name}.css';")

    # 1. Update frontend/src/themes.css
    # Rebuild themes.css imports cleanly
    base_imports = [
        "/* Theme registry — entry point that imports each theme family */",
        "@import './themes/_defaults.css';",
        "@import './themes/built-in.css';",
        "@import './themes/adwaita.css';",
        "@import './themes/breeze.css';",
        "@import './themes/catppuccin.css';",
        "@import './themes/dracula.css';",
        "@import './themes/github.css';",
        "@import './themes/nord.css';",
        "@import './themes/pop.css';",
        "@import './themes/tokyo-night.css';",
        "@import './themes/vs-code.css';",
        "@import './themes/yaru.css';"
    ]
    all_imports = base_imports + import_statements + ["@import './themes/_utilities.css';"]
    with open("frontend/src/themes.css", "w") as f:
        f.write("\n".join(all_imports) + "\n")
    print("Updated themes.css")

    # 2. Update store.go with native Go constants and switch cases
    go_filepath = "internal/settings/store.go"
    
    # Re-read original store.go logic to start fresh and avoid double-modification errors
    # Reset file using git checkout to ensure pure regex replacements work perfectly
    os.system(f"git checkout {go_filepath}")
    
    with open(go_filepath, "r") as f:
        go_code = f.read()

    go_constants_list = []
    go_switch_cases = []
    go_error_modes = []

    for const_name, val in base_modes:
        go_switch_cases.append(const_name)
        go_error_modes.append(f"'{val}'")

    for t in generated_themes:
        const_name = "ThemeMode" + "".join(w.title() for w in t["value"].split("-"))
        go_constants_list.append(f'\t{const_name} = "{t["value"]}"')
        go_switch_cases.append(const_name)
        go_error_modes.append(f"'{t['value']}'")

    go_cases_str = ",\n\t\t".join(go_switch_cases)
    go_errors_str = ", ".join(go_error_modes[:-1]) + ", or " + go_error_modes[-1]
    
    # Construct complete SetThemeMode function
    set_theme_func = f"""func (s *Store) SetThemeMode(mode string) error {{
	switch mode {{
	case {go_cases_str}:
		return s.Set(KeyThemeMode, mode)
	default:
		return fmt.Errorf("invalid theme mode: %s (must be {go_errors_str})", mode)
	}}
}}"""
    
    # Re-insert Go constants
    go_code = re.sub(
        r'const \(\n\tThemeModeSystem.*?\n\tThemeModeVSCodeDark.*?=.*?\n\)',
        "const (\n\tThemeModeSystem      = \"system\"\n\tThemeModeLight       = \"light\"\n\tThemeModeLightBlue   = \"light-blue\"\n\tThemeModeLightOrange   = \"light-orange\"\n\tThemeModeLightBalanced = \"light-balanced\"\n\tThemeModeAdwaitaLight  = \"adwaita-light\"\n\tThemeModeBreezeLight   = \"breeze-light\"\n\tThemeModeDark          = \"dark\"\n\tThemeModeDarkGray     = \"dark-gray\"\n\tThemeModeDarkBalanced = \"dark-balanced\"\n\tThemeModeAdwaitaDark  = \"adwaita-dark\"\n\tThemeModeBreezeDark   = \"breeze-dark\"\n\tThemeModeCatppuccinLatte     = \"catppuccin-latte\"\n\tThemeModeCatppuccinFrappe    = \"catppuccin-frappe\"\n\tThemeModeCatppuccinMacchiato = \"catppuccin-macchiato\"\n\tThemeModeCatppuccinMocha     = \"catppuccin-mocha\"\n\tThemeModeDracula         = \"dracula\"\n\tThemeModeGithubLight     = \"github-light\"\n\tThemeModeGithubDark      = \"github-dark\"\n\tThemeModeGithubSoftDark  = \"github-soft-dark\"\n\tThemeModeTokyoNight      = \"tokyo-night\"\n\tThemeModeNordLight       = \"nord-light\"\n\tThemeModeNordDark        = \"nord-dark\"\n\tThemeModePopLight        = \"pop-light\"\n\tThemeModePopDark         = \"pop-dark\"\n\tThemeModeYaruLight       = \"yaru-light\"\n\tThemeModeYaruDark        = \"yaru-dark\"\n\tThemeModeVSCodeLight     = \"vs-code-light\"\n\tThemeModeVSCodeDark      = \"vs-code-dark\"\n" + "\n".join(go_constants_list) + "\n)",
        go_code,
        flags=re.DOTALL
    )

    # Re-insert SetThemeMode validation logic
    go_code = re.sub(
        r'func \(s \*Store\) SetThemeMode\(mode string\).*?^\}',
        set_theme_func,
        go_code,
        flags=re.DOTALL | re.MULTILINE
    )

    # Append WriteThemeMode database helper if not already present
    if "func WriteThemeMode(" not in go_code:
        go_code += """
// WriteThemeMode opens the database directly to write the theme_mode setting.
// Used when updating the theme from CLI while the main window is not running.
func WriteThemeMode(dbPath string, mode string) error {
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return err
	}
	defer db.Close()

	_, err = db.Exec(`
		INSERT INTO settings (key, value) VALUES ('theme_mode', ?)
		ON CONFLICT(key) DO UPDATE SET value = excluded.value
	`, mode)
	return err
}
"""

    with open(go_filepath, "w") as f:
        f.write(go_code)
    print("Updated internal/settings/store.go")

    # 3. Update Svelte Settings store settings.svelte.ts (ThemeMode type union)
    svelte_store_path = "frontend/src/lib/stores/settings.svelte.ts"
    os.system(f"git checkout {svelte_store_path}")
    
    with open(svelte_store_path, "r") as f:
        svelte_code = f.read()

    base_types = [
        "'system'",
        "'light'", "'light-blue'", "'light-orange'", "'light-balanced'", "'adwaita-light'", "'breeze-light'",
        "'dark'", "'dark-gray'", "'dark-balanced'", "'adwaita-dark'", "'breeze-dark'",
        "'catppuccin-latte'", "'catppuccin-frappe'", "'catppuccin-macchiato'", "'catppuccin-mocha'",
        "'dracula'", "'github-light'", "'github-dark'", "'github-soft-dark'", "'tokyo-night'",
        "'nord-light'", "'nord-dark'",
        "'pop-light'", "'pop-dark'",
        "'yaru-light'", "'yaru-dark'",
        "'vs-code-light'", "'vs-code-dark'"
    ]
    for t in generated_themes:
        base_types.append(f"'{t['value']}'")

    type_union_str = "export type ThemeMode =\n  | " + "\n  | ".join(base_types)
    svelte_code = re.sub(
        r'export type ThemeMode =.*?\n\n',
        type_union_str + "\n\n",
        svelte_code,
        flags=re.DOTALL
    )

    with open(svelte_store_path, "w") as f:
        f.write(svelte_code)
    print("Updated settings.svelte.ts")

    # 4. Update GeneralTab.svelte options dropdown
    gen_tab_path = "frontend/src/lib/components/settings/GeneralTab.svelte"
    os.system(f"git checkout {gen_tab_path}")
    
    with open(gen_tab_path, "r") as f:
        gen_tab_code = f.read()

    # Build dropdown Svelte options
    theme_options = [
        "{ value: 'system', label: $_('settingsGeneral.themeSystem') }",
        "{ value: 'light', label: $_('settingsGeneral.themeLight') }",
        "{ value: 'light-blue', label: $_('settingsGeneral.themeLightBlue') }",
        "{ value: 'light-orange', label: $_('settingsGeneral.themeLightOrange') }",
        "{ value: 'light-balanced', label: $_('settingsGeneral.themeLightBalanced') }",
        "{ value: 'adwaita-light', label: 'Adwaita (Light)' }",
        "{ value: 'breeze-light', label: 'Breeze (Light)' }",
        "{ value: 'catppuccin-latte', label: 'Catppuccin Latte' }",
        "{ value: 'github-light', label: 'GitHub (Light)' }",
        "{ value: 'nord-light', label: 'Nord (Light)' }",
        "{ value: 'pop-light', label: 'Pop! (Light)' }",
        "{ value: 'vs-code-light', label: 'VS Code (Light)' }",
        "{ value: 'yaru-light', label: 'Yaru (Light)' }"
    ]
    
    # Add light generated themes
    for t in generated_themes:
        if not t["is_dark"]:
            theme_options.append(f"    {{ value: '{t['value']}', label: '{t['label']}' }}")

    # Add dark base themes
    theme_options += [
        "{ value: 'dark', label: $_('settingsGeneral.themeDark') }",
        "{ value: 'dark-gray', label: $_('settingsGeneral.themeDarkGray') }",
        "{ value: 'dark-balanced', label: $_('settingsGeneral.themeDarkBalanced') }",
        "{ value: 'adwaita-dark', label: 'Adwaita (Dark)' }",
        "{ value: 'breeze-dark', label: 'Breeze (Dark)' }",
        "{ value: 'catppuccin-frappe', label: 'Catppuccin Frappé' }",
        "{ value: 'catppuccin-macchiato', label: 'Catppuccin Macchiato' }",
        "{ value: 'catppuccin-mocha', label: 'Catppuccin Mocha' }",
        "{ value: 'dracula', label: 'Dracula' }",
        "{ value: 'github-dark', label: 'GitHub (Dark)' }",
        "{ value: 'github-soft-dark', label: 'GitHub (Soft Dark)' }",
        "{ value: 'nord-dark', label: 'Nord (Dark)' }",
        "{ value: 'pop-dark', label: 'Pop! (Dark)' }",
        "{ value: 'tokyo-night', label: 'Tokyo Night' }",
        "{ value: 'vs-code-dark', label: 'VS Code (Dark)' }",
        "{ value: 'yaru-dark', label: 'Yaru (Dark)' }"
    ]

    # Add dark generated themes
    for t in generated_themes:
        if t["is_dark"]:
            theme_options.append(f"    {{ value: '{t['value']}', label: '{t['label']}' }}")

    dropdown_options_str = "  const themeModeOptions = $derived([\n    " + ",\n    ".join(theme_options) + "\n  ])"
    
    gen_tab_code = re.sub(
        r'  const themeModeOptions = \$derived\(.*?^\s*\]\)',
        dropdown_options_str,
        gen_tab_code,
        flags=re.DOTALL | re.MULTILINE
    )

    with open(gen_tab_path, "w") as f:
        f.write(gen_tab_code)
    print("Updated GeneralTab.svelte dropdown menu")

    print("\nAll files successfully restructured natively! 🚀")

if __name__ == "__main__":
    main()
