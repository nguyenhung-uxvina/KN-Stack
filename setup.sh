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

    echo ""
    if [ $broken -eq 0 ]; then
        log_ok "All $total skills verified"
    else
        log_err "$broken/$total skills broken"
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
