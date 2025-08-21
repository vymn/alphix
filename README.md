# Alphix — Rule All Your Tools from One Den

Alphix is a centralized CLI hub that allows you to manage all your scripts, packages, and automation tools from one place. Inspired by the alpha wolf, Alphix provides a unified interface with thematic commands to streamline and organize your workflow.

## Features

- **Alpha-Themed Commands**: Use commands like `hunt`, `scout`, `shed`, and `tracks` along with the standard commands like run/stop/logs/cleanup.
- **Dynamic Tool Discovery**: Automatically detects scripts and modules in Python, Dart, Node, and shell.
- **Interactive CLI**: Modern interface powered by Rich, and live updates.
- **Command History**: Keep track of all executions and logs.
- **Flexible Config**: Define tools in a YAML file for persistent custom commands.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/vymn/alphix.git
   cd alphix
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python setup.py
   ```

## Usage

Launch Alphix:

```bash
alphix i
```

## Configuration

Alphix uses a YAML file `~/.alphix.yaml` to define tools:

```yaml
tools:
  release:
    type: script
    path: ~/work-scripts/release.sh
    desc: Build and release app
  whatsapp:
    type: python
    module: whatsapp_auto_sender.main
    desc: Send WhatsApp messages
```

## Contributing

Contributions are welcome. You can add new tools, improve the CLI interface, or suggest new alpha-themed commands.

## License

This project is open-source under the Apache-2.0 license.
