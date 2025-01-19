# Cursor IDE Tips for Trading Bot Development

## Essential Keyboard Shortcuts
- `Cmd/Ctrl + P`: Quick file switching
- `Cmd/Ctrl + Shift + F`: Project-wide search
- `Cmd/Ctrl + B`: Toggle sidebar
- `Alt + Up/Down`: Move lines up/down

## Recommended Workspace Setup
### Split Views
1. Main split:
   - Exchange implementation
   - Current test file
2. Secondary split:
   - Project progress
   - Documentation

### File Organization
Keep these files in separate tabs:
- src/core/exchange.py
- src/core/risk_manager.py
- docs/project_progress.md
- config_local.py

## Cursor Settings
### Essential Settings
```json
{
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "git.enableSmartCommit": true,
    "files.autoSave": "afterDelay"
}
```

### Debug Configuration
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Trading Bot",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

## AI Features Usage
- Code completion for trading functions
- Documentation generation
- Test case generation
- Error handling suggestions

## Best Practices
1. Use split views for related files
2. Keep project progress visible
3. Utilize AI for repetitive tasks
4. Set up custom snippets for common patterns 