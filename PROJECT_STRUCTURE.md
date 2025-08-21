# CLI Hub - Project Structure

```
meta-work/
├── cli_hub.py              # Main CLI Hub application
├── setup.py               # Installation script (creates 'hub' command)
├── requirements.txt       # Python dependencies
├── examples.py            # Example scripts for testing
├── demo.sh               # Demonstration script
├── Makefile              # Convenient make commands
├── README.md             # Comprehensive documentation
├── _hub                  # Zsh completion script
├── hub_completion.bash   # Bash completion script
└── PROJECT_STRUCTURE.md  # This file
```

## Configuration Directory Structure

After running CLI Hub, it creates `~/.cli-hub/` with:

```
~/.cli-hub/
├── config.yaml           # Script definitions and settings
├── processes.json        # Background process tracking
└── logs/                 # Log files from background processes
    ├── script1_timestamp.log
    ├── script2_timestamp.log
    └── ...
```

## Key Files Description

### `cli_hub.py`

- Main application with all CLI Hub functionality
- Uses Click for command-line interface
- Uses Rich for beautiful terminal output
- Uses psutil for process management
- Handles script registration, execution, and background process management

### `setup.py`

- Creates a symbolic link in `~/.local/bin/hub`
- Adds `~/.local/bin` to PATH in `.zshrc`
- Makes CLI Hub globally accessible

### `examples.py`

- Contains example scripts for testing
- Includes counter, logger, and server simulators
- Useful for demonstrating background process capabilities

### `demo.sh`

- Complete demonstration of CLI Hub features
- Shows script registration, background execution, monitoring, and cleanup

### Completion Scripts

- `_hub`: Zsh completion with intelligent suggestions
- `hub_completion.bash`: Bash completion support

## Installation

1. `cd meta-work`
2. `pip install -r requirements.txt`
3. `python setup.py`
4. Restart terminal or `source ~/.zshrc`
5. Use `hub` command anywhere!

## Quick Test

```bash
make test      # Basic functionality test
make demo      # Full demonstration
hub status     # Check hub status
```
