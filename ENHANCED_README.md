# CLI Hub - Enhanced Interactive CLI Manager

A comprehensive Python CLI application that serves as a central hub for managing your other command-line applications and modules with powerful interactive features.

## 🎯 Core Features

### **Script Management**

- Register and manage your CLI scripts and applications
- Interactive script addition wizard with templates
- Smart argument handling and prompting
- Background process management with full logging

### **Interactive Features** ✨

- **Interactive Mode** - Full interactive shell for CLI Hub
- **Wizard Mode** - Guided script addition with templates
- **Smart Run** - Intelligent argument prompting for complex CLIs
- **Template System** - Pre-configured templates for common tools

### **Process Management**

- Run scripts in foreground or background
- Real-time log monitoring and output viewing
- Process control (start, stop, monitor)
- Automatic cleanup of stopped processes

## 🔧 Enhanced Commands

### **New Interactive Commands**

- `hub interactive` - Launch full interactive mode
- `hub wizard` - Interactive script addition wizard
- `hub irun <name>` - Run script with interactive argument prompting
- `hub smart-add <name> --template <type>` - Smart addition with templates
- `hub run <name> --interactive` - Enhanced run with smart prompting

### **Traditional Commands**

- `hub add <name> <command>` - Register a new script
- `hub run <name> [args]` - Run a registered script
- `hub run <name> --background` - Run in background
- `hub ps` - List background processes
- `hub logs <name>` - View process logs
- `hub stop <name>` - Stop background process

## 🚀 Installation

1. Clone or download the CLI Hub files:

   ```bash
   cd /path/to/cli-hub
   pip install -r requirements.txt
   ```

2. Install globally:

   ```bash
   python setup.py
   # Restart terminal or: source ~/.zshrc
   ```

3. Start using:
   ```bash
   hub --help
   hub interactive  # Try interactive mode!
   ```

## 🎮 Interactive Mode Demo

The CLI Hub now supports a full interactive mode that makes managing complex CLI applications much easier:

```bash
hub interactive
```

Interactive commands:

- `add` - Launch script addition wizard
- `run <name>` - Run with interactive prompting
- `list` - Show all scripts
- `ps` - Show background processes
- `logs <name>` - View process logs
- `stop <name>` - Stop background process
- `help` - Show available commands
- `exit` - Exit interactive mode

## 🧙 Wizard Mode for Complex CLIs

Perfect for CLIs with subcommands (like your activity monitor):

```bash
hub wizard
```

The wizard will:

1. Ask for script name
2. Offer templates (Python, Node.js, Docker, etc.)
3. Configure argument handling (subcommands, flags, etc.)
4. Set up working directory
5. Test the script immediately

## 💡 Smart Argument Handling

For complex CLIs like your activity monitor that have subcommands:

```bash
# Instead of failing with no args:
hub run timer  # ❌ Shows help/usage

# Use interactive run:
hub irun timer  # ✅ Prompts for subcommand interactively

# Or run with smart prompting:
hub run timer --interactive  # ✅ Prompts if no args provided

# Or just pass args directly:
hub run timer status  # ✅ Works as expected
```

## 🎯 Solving Your Activity Monitor Issue

Here's how the enhanced CLI Hub solves your original problem:

### **Before** (Traditional approach):

```bash
hub run timer        # ❌ Fails - needs subcommand
```

### **After** (Interactive approach):

```bash
# Option 1: Interactive run with prompting
hub irun timer       # ✅ Prompts for: start/status/debug/report/etc.

# Option 2: Enhanced run with smart detection
hub run timer --interactive  # ✅ Detects missing args and prompts

# Option 3: Direct with args (still works)
hub run timer status # ✅ Works directly

# Option 4: Use interactive mode
hub interactive
> run timer          # ✅ Prompts for subcommand interactively
```

## 📋 Example: Setting up Activity Monitor

```bash
# Use the wizard for initial setup
hub wizard

# When prompted:
# Script name: activity-monitor
# Template: 1 (Python)
# Command: python3 /path/to/activity-monitor/main_new.py
# Supports args: Yes
# Arg style: subcommand
# Subcommands: start,status,debug,report,export

# Now you can run it interactively:
hub irun activity-monitor  # Will prompt for subcommand

# Or use interactive mode:
hub interactive
> run activity-monitor     # Interactive prompting
```

## 🎨 Templates Available

- **Python**: `python script.py`
- **Node.js**: `node script.js`
- **NPM**: `npm run command`
- **Docker**: `docker run image`
- **Custom**: Enter any command

## 💾 Configuration

Enhanced configuration now supports:

- Argument handling preferences
- Subcommand definitions
- Template customizations
- Interactive behavior settings

Config location: `~/.cli-hub/config.yaml`

## 🔥 Key Benefits

1. **No More Failed Commands** - Interactive prompting prevents CLI failures
2. **Learning Friendly** - Discover subcommands and options interactively
3. **Template System** - Quick setup for common CLI patterns
4. **Smart Detection** - Automatically prompts when arguments are missing
5. **Full Control** - Choose between interactive and direct command execution

## 📊 Current Status

Your CLI Hub now includes:

- ✅ **8 registered scripts** (including your activity monitor)
- ✅ **Interactive Mode** for easy management
- ✅ **Smart Argument Handling** for complex CLIs
- ✅ **Template System** for quick setup
- ✅ **Background Process Management**
- ✅ **Real-time Logging** and monitoring

---

**🎉 Your CLI Hub is now an intelligent, interactive command center that handles complex CLIs gracefully!**
