# CLI Hub

A comprehensive Python CLI application that serves as a central hub for managing your other command-line applications and modules.

## Features

### 🎯 Core Features

- **Script Management**: Register and manage your CLI scripts and applications
- **Background Processes**: Run scripts in the background with process management
- **Output Monitoring**: View logs and output from background processes
- **Process Control**: Start, stop, and monitor background processes
- **Direct Execution**: Execute commands directly through the hub

### 🔧 Commands

#### Script Management

- `hub add <name> <command>` - Register a new script
- `hub remove <name>` - Remove a registered script
- `hub list` - List all registered scripts

#### Execution

- `hub run <name> [args]` - Run a registered script
- `hub run <name> --background` - Run a script in the background
- `hub exec <command>` - Execute a command directly
- `hub exec <command> --background --name <process_name>` - Execute in background

#### Process Management

- `hub ps` - List background processes
- `hub stop <name>` - Stop a background process
- `hub logs <name> [--lines N]` - View logs from a background process
- `hub cleanup` - Remove stopped processes from the list

#### System

- `hub status` - Show hub status and statistics

## Installation

1. Clone or download the CLI Hub files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the setup script to make it globally accessible:
   ```bash
   python setup.py
   ```
   This will create a `hub` command that you can use from anywhere.

## Quick Start

### 1. Add Your First Script

```bash
hub add myapi "python /path/to/my/api.py" --description "My REST API server"
```

### 2. Run It in Background

```bash
hub run myapi --background
```

### 3. Check Status

```bash
hub ps
```

### 4. View Logs

```bash
hub logs myapi
```

### 5. Stop When Done

```bash
hub stop myapi
```

## Examples

### Managing a Web Server

```bash
# Add a development server
hub add devserver "python -m http.server 8000" --workdir "/path/to/web/files"

# Start in background
hub run devserver --background

# Check if it's running
hub ps

# View recent logs
hub logs devserver --lines 20
```

### Managing Multiple Services

```bash
# Add multiple services
hub add database "mongod --dbpath ./data"
hub add redis "redis-server"
hub add api "python app.py"

# Start all in background
hub run database --background
hub run redis --background
hub run api --background

# Monitor all processes
hub ps
```

### Direct Command Execution

```bash
# Run a one-time command
hub exec "npm run build"

# Run a long-running process in background
hub exec "npm run watch" --background --name "webpack-watch"
```

## Configuration

The CLI Hub stores its configuration in `~/.cli-hub/`:

- `config.yaml` - Script definitions and settings
- `processes.json` - Background process information
- `logs/` - Log files from background processes

### Configuration Options

- `default_timeout`: Default timeout for commands (seconds)
- `max_log_size`: Maximum log file size
- `auto_cleanup`: Automatically clean up stopped processes

## Advanced Usage

### Working Directories

When adding scripts, you can specify a working directory:

```bash
hub add buildscript "make build" --workdir "/path/to/project"
```

### Environment Variables

The hub inherits your shell's environment variables, so your scripts will have access to the same environment.

### Log Management

- Log files are automatically created for background processes
- Logs are stored in `~/.cli-hub/logs/`
- Each background process gets a timestamped log file

## Tips

1. **Organize Your Scripts**: Use descriptive names and descriptions for your scripts
2. **Monitor Resources**: Use `hub ps` regularly to check on background processes
3. **Clean Up**: Run `hub cleanup` occasionally to remove stopped processes
4. **Check Logs**: Use `hub logs` to debug issues with background processes
5. **Use Aliases**: Create shell aliases for frequently used hub commands

## Requirements

- Python 3.7+
- click
- rich
- psutil
- pyyaml
- watchdog

## Platform Support

- ✅ macOS
- ✅ Linux
- ⚠️ Windows (limited testing)

---

**Made with ❤️ for developers who love the command line**
