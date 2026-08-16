#!/usr/bin/env bash
# setup.sh — KN-Stack Deployment Script
# Deploy skills via Windows directory junctions, copy hooks/rules to vault.
#
# Usage:
#   bash setup.sh --install [VAULT_DIR]   Deploy skills + hooks + rules
#   bash setup.sh --update  [VAULT_DIR]   Re-copy hooks + rules only
#   bash setup.sh --verify                Check all junctions resolve
#   bash setup.sh --unlink                Remove all junctions
#   bash setup.sh --status                Show deployment summary

set -euo pipefail
shopt -s nullglob  # empty globs (e.g., empty mentors/ domain) return [] instead of literal pattern

KNSTACK_DIR="$(cd "$(dirname "$0")" && pwd)"
COMMANDS_DIR="${HOME}/.claude/commands"
MODE="${1:---status}"
VAULT_DIR="${2:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err()  { echo -e "${RED}[ERR]${NC} $1"; }
log_skip() { echo -e "  [SKIP] $1"; }

# ── Plugin skill dirs ──
# Plugins keep their skills at plugins/<plugin>/skills/<dir>/ and may ship a shared
# reference dir (e.g. fluency-4d-shared/) that the SKILL.md files reach via ../fluency-4d-shared/…
# Every child of plugins/*/skills/ must be junctioned — including the shared dir — otherwise
# ".." resolves to ~/.claude/commands/ and the shared references vanish silently.
#
# ~/.claude/commands/ is a FLAT namespace shared by every plugin, so a generic dir
# name (_shared, common, refs) collides across plugins. Name shared dirs <plugin>-shared.
plugin_skill_dirs() {
    local d
    for d in "$KNSTACK_DIR"/plugins/*/skills/*/; do
        [ -d "$d" ] && echo "${d%/}"
    done
}

# Map every junction under COMMANDS_DIR to the path it actually points at.
# Emits "<name>|<windows target path>" lines, lowercased for comparison.
junction_targets() {
    local win_commands=$(cygpath -w "$COMMANDS_DIR" 2>/dev/null || echo "$COMMANDS_DIR")
    powershell.exe -ExecutionPolicy Bypass -Command "
        Get-ChildItem -Path '${win_commands}' -Directory -Force |
            Where-Object { \$_.LinkType } | ForEach-Object {
                \$t = \$_.Target; if (\$t -is [array]) { \$t = \$t[0] }
                Write-Output (\$_.Name + '|' + \$t)
            }
    " 2>/dev/null | tr -d '\r' | tr '[:upper:]' '[:lower:]'
}

# Windows path, lowercased, backslashes — same shape junction_targets emits.
win_key() {
    local p=$(cygpath -w "$1" 2>/dev/null || echo "$1")
    echo "$p" | tr '[:upper:]' '[:lower:]'
}

# ── Install: create junctions for all skills ──
do_install() {
    echo "=== KN-Stack Install ==="
    echo "Source: $KNSTACK_DIR/skills/"
    echo "Target: $COMMANDS_DIR/"
    [ -n "$VAULT_DIR" ] && echo "Vault:  $VAULT_DIR"
    echo ""

    mkdir -p "$COMMANDS_DIR"

    # Use PowerShell for reliable junction creation on Windows
    local win_commands=$(cygpath -w "$COMMANDS_DIR" 2>/dev/null || echo "$COMMANDS_DIR")
    local win_skills=$(cygpath -w "$KNSTACK_DIR/skills" 2>/dev/null || echo "$KNSTACK_DIR/skills")

    local result=$(powershell.exe -ExecutionPolicy Bypass -Command "
        \$TARGET = '${win_commands}'
        \$SOURCE = '${win_skills}'
        \$count = 0; \$skip = 0; \$err = 0
        if (-not (Test-Path \$TARGET)) { New-Item -ItemType Directory -Path \$TARGET | Out-Null }
        Get-ChildItem -Path \$SOURCE -Directory | ForEach-Object {
            Get-ChildItem -Path \$_.FullName -Directory | ForEach-Object {
                \$t = Join-Path \$TARGET \$_.Name
                if (Test-Path \$t) { \$skip++; return }
                try { New-Item -ItemType Junction -Path \$t -Target \$_.FullName -ErrorAction Stop | Out-Null; \$count++ }
                catch { \$err++ }
            }
        }
        Write-Output \"\$count linked, \$skip skipped, \$err errors\"
    " 2>&1)

    log_ok "Skills: $result"

    # Plugin skills (plugins/<plugin>/skills/<dir>/, including shared reference dirs)
    local win_plugins=$(cygpath -w "$KNSTACK_DIR/plugins" 2>/dev/null || echo "$KNSTACK_DIR/plugins")
    local presult=$(powershell.exe -ExecutionPolicy Bypass -Command "
        \$TARGET = '${win_commands}'
        \$SOURCE = '${win_plugins}'
        \$count = 0; \$skip = 0; \$err = 0
        if (Test-Path \$SOURCE) {
            Get-ChildItem -Path \$SOURCE -Directory | ForEach-Object {
                \$sk = Join-Path \$_.FullName 'skills'
                if (-not (Test-Path \$sk)) { return }
                Get-ChildItem -Path \$sk -Directory | ForEach-Object {
                    \$t = Join-Path \$TARGET \$_.Name
                    if (Test-Path \$t) { \$skip++; return }
                    try { New-Item -ItemType Junction -Path \$t -Target \$_.FullName -ErrorAction Stop | Out-Null; \$count++ }
                    catch { \$err++ }
                }
            }
        }
        Write-Output \"\$count linked, \$skip skipped, \$err errors\"
    " 2>&1)

    log_ok "Plugin skills: $presult"

    # Deploy hooks and rules to vault
    if [ -n "$VAULT_DIR" ]; then
        do_update_vault "$VAULT_DIR"
    fi
}

# ── Update: re-copy hooks and rules ──
do_update_vault() {
    local vault="$1"
    echo ""
    echo "=== Deploying hooks + rules to $vault ==="

    # Hooks
    local hooks_dir="$vault/.claude/hooks"
    mkdir -p "$hooks_dir"
    for hook in "$KNSTACK_DIR"/hooks/*.sh; do
        local name=$(basename "$hook")
        cp "$hook" "$hooks_dir/$name"
        chmod +x "$hooks_dir/$name"
        log_ok "hook: $name"
    done

    # Rules
    local rules_dir="$vault/.claude/rules"
    mkdir -p "$rules_dir"
    for rule in "$KNSTACK_DIR"/rules/*.md; do
        local name=$(basename "$rule")
        cp "$rule" "$rules_dir/$name"
        log_ok "rule: $name"
    done
}

# ── Verify: check all junctions ──
do_verify() {
    echo "=== KN-Stack Verify ==="
    local ok=0
    local broken=0
    local total=0

    for domain_dir in "$KNSTACK_DIR"/skills/*/; do
        for skill_dir in "$domain_dir"*/; do
            local skill_name=$(basename "$skill_dir")
            local target="$COMMANDS_DIR/$skill_name"
            total=$((total + 1))

            if [ -d "$target" ] && [ -f "$target/SKILL.md" ]; then
                ok=$((ok + 1))
            else
                log_err "BROKEN: $skill_name → $target"
                broken=$((broken + 1))
            fi
        done
    done

    local p_ok=0
    local p_broken=0
    local p_total=0
    local src name target

    # Shape alone is not enough: another plugin owning the same name produces a
    # junction that has SKILL.md/references/ and verifies green while pointing
    # somewhere else entirely. Compare the junction TARGET against this source.
    declare -A JT
    local line
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        JT["${line%%|*}"]="${line#*|}"
    done < <(junction_targets)

    while IFS= read -r src; do
        [ -z "$src" ] && continue
        name=$(basename "$src")
        target="$COMMANDS_DIR/$name"
        p_total=$((p_total + 1))
        # A plugin skill dir carries SKILL.md; a shared reference dir carries references/.
        if [ ! -d "$target" ] || { [ ! -f "$target/SKILL.md" ] && [ ! -d "$target/references" ]; }; then
            log_err "BROKEN (plugin): $name → $target"
            p_broken=$((p_broken + 1))
            continue
        fi
        local want=$(win_key "$src")
        local got="${JT[$(echo "$name" | tr '[:upper:]' '[:lower:]')]:-}"
        if [ -n "$got" ] && [ "$got" != "$want" ]; then
            log_err "HIJACKED (plugin): $name → $got (phải là $want)"
            p_broken=$((p_broken + 1))
        else
            p_ok=$((p_ok + 1))
        fi
    done < <(plugin_skill_dirs)

    echo ""
    if [ $broken -eq 0 ]; then
        log_ok "All $total skills verified"
    else
        log_err "$broken/$total skills broken"
    fi
    if [ $p_total -gt 0 ]; then
        if [ $p_broken -eq 0 ]; then
            log_ok "All $p_total plugin skill dirs verified"
        else
            log_err "$p_broken/$p_total plugin skill dirs broken"
        fi
    fi
}

# ── Unlink: remove all junctions ──
do_unlink() {
    echo "=== KN-Stack Unlink ==="
    local count=0

    for domain_dir in "$KNSTACK_DIR"/skills/*/; do
        for skill_dir in "$domain_dir"*/; do
            local skill_name=$(basename "$skill_dir")
            local target="$COMMANDS_DIR/$skill_name"

            if [ -d "$target" ]; then
                # Remove junction (rmdir removes junction without deleting target)
                rmdir "$target" 2>/dev/null && count=$((count + 1))
            fi
        done
    done

    local src name target
    while IFS= read -r src; do
        [ -z "$src" ] && continue
        name=$(basename "$src")
        target="$COMMANDS_DIR/$name"
        if [ -d "$target" ]; then
            rmdir "$target" 2>/dev/null && count=$((count + 1))
        fi
    done < <(plugin_skill_dirs)

    log_ok "Removed $count junctions"
    echo "Restore from backup: cp -r ~/.claude/commands.bak.*/* ~/.claude/commands/"
}

# ── Status: show summary ──
do_status() {
    echo "=== KN-Stack Status ==="
    echo "Location: $KNSTACK_DIR"
    echo ""

    echo "Skills by domain:"
    local total=0
    for domain_dir in "$KNSTACK_DIR"/skills/*/; do
        local domain=$(basename "$domain_dir")
        local count=$(ls -1d "$domain_dir"*/ 2>/dev/null | wc -l)
        printf "  %-12s %3d\n" "$domain" "$count"
        total=$((total + count))
    done
    echo "  ────────────────"
    printf "  %-12s %3d\n" "TOTAL" "$total"

    echo ""
    local plugin_dirs=$(plugin_skill_dirs | wc -l)
    echo "Plugin skill dirs (not counted above): $plugin_dirs"
    local p
    while IFS= read -r p; do
        [ -z "$p" ] && continue
        printf "  %s\n" "$(basename "$p")"
    done < <(plugin_skill_dirs)

    echo ""
    echo "Deployed junctions:"
    local linked=$(ls -1d "$COMMANDS_DIR"/*/ 2>/dev/null | wc -l)
    echo "  $linked skill directories in ~/.claude/commands/"

    echo ""
    local version=$(cat "$KNSTACK_DIR/VERSION" 2>/dev/null || echo "unknown")
    echo "Version: $version"
}

# ── Main ──
case "$MODE" in
    --install) do_install ;;
    --update)
        if [ -z "$VAULT_DIR" ]; then
            log_err "Usage: setup.sh --update VAULT_DIR"
            exit 1
        fi
        do_update_vault "$VAULT_DIR"
        ;;
    --verify) do_verify ;;
    --unlink) do_unlink ;;
    --status) do_status ;;
    *)
        echo "Usage: bash setup.sh {--install|--update|--verify|--unlink|--status} [VAULT_DIR]"
        exit 1
        ;;
esac
