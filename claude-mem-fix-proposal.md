# Claude-Mem Plugin Fix Proposal

## Problem Summary

The claude-mem plugin's auto-install feature for Bun fails silently:
1. Hook errors show only generic "SessionStart:startup hook error"
2. Detailed error messages written to stderr are not visible to users
3. After successful Bun installation, hooks still fail because Bun isn't in PATH
4. Users must manually restart terminal without being told to do so

## Root Causes

1. **Hook Output Suppression**: Claude Code doesn't display hook stderr/stdout to users
2. **PATH Inheritance**: Newly installed Bun updates shell config (~/.zshrc) but current session's PATH is unchanged
3. **Rigid Detection Logic**: Script exits with error even when Bun is successfully installed but not in current PATH
4. **No Visible Feedback**: All error messages go to invisible stderr stream

## Proposed Fix (Cross-Platform)

### Part 1: Visible Error Logging

**Create persistent status file**: `~/.claude/plugins/marketplaces/thedotmack/.setup-status.log`

```javascript
// Add to smart-install.js
const LOG_FILE = join(ROOT, '.setup-status.log');

function logStatus(level, message, action = null) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level, // 'success' | 'warning' | 'error'
    message,
    action // What user should do
  };

  // Append to log file
  const logLine = `[${timestamp}] ${level.toUpperCase()}: ${message}\n`;
  if (action) {
    logLine += `  ACTION REQUIRED: ${action}\n`;
  }

  try {
    const existing = existsSync(LOG_FILE) ? readFileSync(LOG_FILE, 'utf-8') : '';
    writeFileSync(LOG_FILE, existing + logLine);
  } catch (err) {
    // Fallback: write to home directory if plugin dir fails
    const fallbackLog = join(homedir(), '.claude-mem-setup.log');
    writeFileSync(fallbackLog, logLine);
  }

  // Still log to stderr for debugging
  console.error(logLine);

  return logEntry;
}
```

### Part 2: Smart Bun Detection & PATH Resolution

**Modify Bun detection to be PATH-independent:**

```javascript
// Modified installBun() function
function installBun() {
  logStatus('info', 'Bun not found. Installing Bun runtime...');

  try {
    if (IS_WINDOWS) {
      execSync('powershell -c "irm bun.sh/install.ps1 | iex"', {
        stdio: 'inherit',
        shell: true
      });
    } else {
      execSync('curl -fsSL https://bun.sh/install | bash', {
        stdio: 'inherit',
        shell: true
      });
    }

    // Check installation by file existence, not PATH
    const expectedPath = IS_WINDOWS
      ? join(homedir(), '.bun', 'bin', 'bun.exe')
      : join(homedir(), '.bun', 'bin', 'bun');

    if (existsSync(expectedPath)) {
      // SUCCESS - but PATH not updated in current session
      logStatus('warning',
        `Bun installed successfully to ${expectedPath}`,
        'Please restart your terminal/Claude Code for changes to take effect'
      );

      // CRITICAL: Save the detected Bun path for hooks to use
      writeFileSync(join(ROOT, '.bun-path'), expectedPath);

      // DON'T exit with error - installation succeeded!
      return expectedPath;
    } else {
      throw new Error('Bun installation completed but binary not found');
    }
  } catch (error) {
    logStatus('error',
      'Failed to install Bun automatically: ' + error.message,
      'Please install manually: curl -fsSL https://bun.sh/install | bash && restart terminal'
    );
    throw error;
  }
}
```

### Part 3: Hook Command Resolution

**Modify hooks.json to use smart path resolution:**

Create a new wrapper script: `scripts/bun-wrapper.sh`

```bash
#!/usr/bin/env bash
# Wrapper script to find and execute Bun

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/thedotmack}"
BUN_PATH_FILE="$PLUGIN_ROOT/.bun-path"

# Try to find Bun
find_bun() {
  # 1. Check saved path from smart-install
  if [ -f "$BUN_PATH_FILE" ]; then
    BUN_PATH=$(cat "$BUN_PATH_FILE")
    if [ -x "$BUN_PATH" ]; then
      echo "$BUN_PATH"
      return 0
    fi
  fi

  # 2. Check PATH
  if command -v bun &> /dev/null; then
    echo "bun"
    return 0
  fi

  # 3. Check common install locations
  for path in "$HOME/.bun/bin/bun" "/usr/local/bin/bun" "/opt/homebrew/bin/bun"; do
    if [ -x "$path" ]; then
      echo "$path"
      return 0
    fi
  done

  # 4. Not found - write error to visible log
  echo "[$(date -Iseconds)] ERROR: Bun not found. Install with: curl -fsSL https://bun.sh/install | bash" >> "$PLUGIN_ROOT/.setup-status.log"
  echo "  ACTION REQUIRED: Restart terminal after installation" >> "$PLUGIN_ROOT/.setup-status.log"
  return 1
}

BUN=$(find_bun)
if [ $? -eq 0 ]; then
  exec "$BUN" "$@"
else
  echo "Error: Bun not found. Check $PLUGIN_ROOT/.setup-status.log for details" >&2
  exit 1
fi
```

**Update hooks.json:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/smart-install.js\"",
            "timeout": 300
          },
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/scripts/bun-wrapper.sh\" \"${CLAUDE_PLUGIN_ROOT}/scripts/worker-service.cjs\" start",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Part 4: User-Visible Error Display

**Display error on next Claude Code interaction:**

When hooks fail, write a special marker file that Claude can detect and display:

```javascript
// Add to end of smart-install.js catch block
} catch (e) {
  const errorMessage = {
    title: 'Claude-Mem Setup Required',
    message: e.message,
    action: 'Restart your terminal and Claude Code',
    logFile: LOG_FILE,
    timestamp: new Date().toISOString()
  };

  writeFileSync(
    join(ROOT, '.setup-error.json'),
    JSON.stringify(errorMessage, null, 2)
  );

  logStatus('error', 'Installation failed: ' + e.message);
  process.exit(1);
}
```

## Implementation Checklist

- [ ] Add `logStatus()` function to smart-install.js
- [ ] Modify `installBun()` to save detected path and not exit on PATH miss
- [ ] Modify `installUv()` with same pattern
- [ ] Create `scripts/bun-wrapper.sh` (Unix/Mac)
- [ ] Create `scripts/bun-wrapper.ps1` (Windows PowerShell)
- [ ] Update hooks.json to use wrapper scripts
- [ ] Add .setup-error.json detection and display mechanism
- [ ] Test on macOS (official installer)
- [ ] Test on macOS (Homebrew)
- [ ] Test on Linux (official installer)
- [ ] Test on Windows
- [ ] Add troubleshooting docs with log file location

## Benefits

1. ✅ **Cross-platform**: Works on all OSes (macOS, Linux, Windows)
2. ✅ **PATH-independent**: Hooks work even before PATH is updated
3. ✅ **Visible errors**: Users can always check `.setup-status.log`
4. ✅ **Graceful degradation**: Installation success doesn't fail due to PATH timing
5. ✅ **Debuggable**: Clear log trail for troubleshooting
6. ✅ **No breaking changes**: Backward compatible with existing installs

## Testing Plan

1. **Fresh install test**: Uninstall Bun, install plugin, verify auto-install works
2. **PATH test**: Verify hooks work immediately after install without terminal restart
3. **Error visibility**: Force failure, verify error appears in log file
4. **Multiple platforms**: Test on macOS (Intel/Apple Silicon), Linux, Windows
5. **Homebrew test**: Install Bun via Homebrew, verify plugin detects it

## Files to Modify

1. `scripts/smart-install.js` - Add logging, fix exit logic
2. `hooks/hooks.json` - Use wrapper scripts
3. `scripts/bun-wrapper.sh` - New file (Unix)
4. `scripts/bun-wrapper.ps1` - New file (Windows)
5. `README.md` - Document log file location

## Migration Path

Existing users with working setups won't be affected. New users or those experiencing issues will automatically get the improved error handling.
