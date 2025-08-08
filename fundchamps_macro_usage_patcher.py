import os
import re

# Directory where your templates live
TEMPLATE_DIRS = [
    "./templates",
    "./app/templates",
]

# List of your macro names that accept attrs (add more as needed)
MACROS_WITH_ATTRS = [
    'render_button',
    'progress_meter',
    # Add other macro names here as you refactor!
]

# Arguments allowed in your macros BEFORE attrs (set these for each macro)
MACRO_ARG_WHITELIST = {
    'render_button': ['label', 'href', 'color', 'size', 'icon', 'loading', 'external', 'aria_label', 'extra_classes', 'type'],
    'progress_meter': ['raised', 'goal', 'size', 'extra_classes'],
}

# Regex to match macro calls, e.g. {{ render_button(...)}}
MACRO_CALL_PATTERN = re.compile(
    r'(\{\{\s*(' + '|'.join(MACROS_WITH_ATTRS) + r')\s*\((.*?)\)\s*\}\})',
    re.DOTALL
)

def parse_macro_args(arg_str):
    """
    Returns: (known_args, unknown_kwargs)
    """
    # This is a naive parser: will break on nested dicts/lists, but works for 90% of simple Jinja calls.
    args = []
    kwargs = {}
    buf = ''
    depth = 0
    key = None
    for c in arg_str + ',':
        if c in '({[':
            depth += 1
            buf += c
        elif c in ')}]':
            depth -= 1
            buf += c
        elif c == ',' and depth == 0:
            part = buf.strip()
            buf = ''
            if '=' in part:
                k, v = part.split('=', 1)
                kwargs[k.strip()] = v.strip()
            elif part:
                args.append(part)
        else:
            buf += c
    return args, kwargs

def rewrite_macro_call(macro_name, args, kwargs):
    allowed = MACRO_ARG_WHITELIST[macro_name]
    known = []
    unknown = []
    for k in list(kwargs):
        if k in allowed:
            known.append(f"{k}={kwargs[k]}")
        else:
            unknown.append(f'"{k}": {kwargs[k]}')
    # Add attrs if needed
    if unknown:
        known.append(f"attrs={{ {', '.join(unknown)} }}")
    args_str = ', '.join(args + known)
    return f"{{{{ {macro_name}({args_str}) }}}}"

def patch_macros_in_file(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    changed = False

    def replacer(match):
        full, macro_name, argstr = match.groups()
        args, kwargs = parse_macro_args(argstr)
        new_macro = rewrite_macro_call(macro_name, args, kwargs)
        nonlocal changed
        if new_macro != full:
            changed = True
            return new_macro
        return full

    new_content = MACRO_CALL_PATTERN.sub(replacer, content)

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Patched: {path}")
    else:
        print(f"— No changes: {path}")

def scan_and_patch():
    for tdir in TEMPLATE_DIRS:
        if not os.path.isdir(tdir):
            continue
        for root, _, files in os.walk(tdir):
            for file in files:
                if file.endswith('.html'):
                    patch_macros_in_file(os.path.join(root, file))

if __name__ == "__main__":
    print("🔍 FundChamps Macro Usage Patcher: Refactoring macro calls to use attrs={...}")
    scan_and_patch()
    print("🌟 All done! Your templates now pass data-* and htmx- attributes via attrs.")


