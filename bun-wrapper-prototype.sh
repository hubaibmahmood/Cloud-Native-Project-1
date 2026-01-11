#!/usr/bin/env bash
# Prototype: Bun wrapper script for claude-mem hooks
# This finds Bun regardless of PATH state

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/thedotmack}"
BUN_PATH_FILE="$PLUGIN_ROOT/.bun-path"
LOG_FILE="$PLUGIN_ROOT/.setup-status.log"

# Function to log messages
log_message() {
  local level="$1"
  local message="$2"
  local timestamp=$(date -Iseconds 2>/dev/null || date +%Y-%m-%dT%H:%M:%S)
  echo "[$timestamp] $level: $message" >> "$LOG_FILE"
}

# Function to find Bun executable
find_bun() {
  # 1. Check saved path from smart-install.js
  if [ -f "$BUN_PATH_FILE" ]; then
    BUN_PATH=$(cat "$BUN_PATH_FILE" 2>/dev/null || echo "")
    if [ -n "$BUN_PATH" ] && [ -x "$BUN_PATH" ]; then
      echo "$BUN_PATH"
      return 0
    fi
  fi

  # 2. Check if 'bun' is in PATH
  if command -v bun &> /dev/null; then
    BUN_PATH=$(command -v bun)
    # Save for future use
    echo "$BUN_PATH" > "$BUN_PATH_FILE" 2>/dev/null || true
    echo "$BUN_PATH"
    return 0
  fi

  # 3. Check common installation locations
  local common_paths=(
    "$HOME/.bun/bin/bun"
    "/usr/local/bin/bun"
    "/opt/homebrew/bin/bun"
    "/home/linuxbrew/.linuxbrew/bin/bun"
  )

  for path in "${common_paths[@]}"; do
    if [ -x "$path" ]; then
      # Save for future use
      echo "$path" > "$BUN_PATH_FILE" 2>/dev/null || true
      echo "$path"
      return 0
    fi
  done

  # 4. Not found - log error
  log_message "ERROR" "Bun executable not found in PATH or common locations"
  log_message "ACTION" "Install Bun: curl -fsSL https://bun.sh/install | bash"
  log_message "ACTION" "Then restart your terminal and Claude Code"
  return 1
}

# Main execution
BUN=$(find_bun)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  log_message "INFO" "Using Bun at: $BUN"
  # Execute Bun with all arguments passed to this script
  exec "$BUN" "$@"
else
  echo "❌ Error: Bun not found" >&2
  echo "📋 Check setup log: $LOG_FILE" >&2
  echo "" >&2
  echo "To fix:" >&2
  echo "  1. Install Bun: curl -fsSL https://bun.sh/install | bash" >&2
  echo "  2. Restart your terminal" >&2
  echo "  3. Restart Claude Code" >&2
  exit 1
fi
