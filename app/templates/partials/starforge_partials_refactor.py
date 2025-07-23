#!/usr/bin/env python3
"""
starforge_partials_refactor.py
Elite Partial Backup & Clean-up 🚀
"""

import os
import re
from shutil import copyfile

DIR = os.path.abspath(os.path.dirname(__file__))
BACKUP_SUFFIX = ".starforgebak"
EXT = ".html"

def backup_partials():
    for fname in os.listdir(DIR):
        if fname.endswith(EXT) and not fname.endswith(BACKUP_SUFFIX):
            copyfile(fname, fname + BACKUP_SUFFIX)
            print(f"🔒 Backed up {fname} → {fname + BACKUP_SUFFIX}")

def cleanup_baks():
    deleted = 0
    for fname in os.listdir(DIR):
        if fname.endswith(".bak"):
            os.remove(os.path.join(DIR, fname))
            deleted += 1
    print(f"🧹 Cleaned up {deleted} .bak files.")

def find_duplicates():
    # (Optional) Warn on likely dupes: same base name, different extension
    base_names = {}
    for fname in os.listdir(DIR):
        if fname.endswith(EXT):
            key = fname.replace(".bak", "").replace(BACKUP_SUFFIX, "").replace(EXT, "")
            base_names.setdefault(key, []).append(fname)
    for key, files in base_names.items():
        if len(files) > 1:
            print(f"⚠️  Multiple versions of partial '{key}': {', '.join(files)} (review for dupe/merge)")

if __name__ == "__main__":
    print("🌟 STARFORGE PARTIALS ELITE UPGRADE: START 🌟\n")
    backup_partials()
    cleanup_baks()
    find_duplicates()
    print("\n🚀 All done! Every partial is backed up, bloat-free, and ready for SaaS scaling.\n")
    print("💡 Pro tip: Keep only one version of each partial for clean rebranding or white-label rollouts.")
