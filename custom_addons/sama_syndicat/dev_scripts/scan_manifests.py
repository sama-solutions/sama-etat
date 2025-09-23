#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ast
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CUSTOM_ADDONS = os.path.abspath(os.path.join(BASE_DIR, '..'))

TARGET_DIRS = [CUSTOM_ADDONS]

def scan_dir(root):
    issues = []
    checked = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for name in ('__manifest__.py', '__openerp__.py'):
            if name in filenames:
                path = os.path.join(dirpath, name)
                checked += 1
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.literal_eval(content)
                except SyntaxError as e:
                    issues.append((path, f"SyntaxError line {e.lineno}: {e.msg}"))
                except Exception as e:
                    issues.append((path, f"Error: {e}"))
    return checked, issues

if __name__ == '__main__':
    total_checked = 0
    total_issues = []
    print("🔍 Scanning manifests under:", ", ".join(TARGET_DIRS))
    for td in TARGET_DIRS:
        checked, issues = scan_dir(td)
        total_checked += checked
        total_issues.extend(issues)
    print(f"📦 Manifests checked: {total_checked}")
    if total_issues:
        print(f"❌ Issues found: {len(total_issues)}\n")
        for path, err in total_issues:
            print(f"• {path}: {err}")
        sys.exit(1)
    else:
        print("✅ All manifests are valid.")
        sys.exit(0)
