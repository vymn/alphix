#!/usr/bin/env python3
"""
CLI Hub - A central command-line application manager
"""

import click
import os
import sys
import json
import subprocess
import signal
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.syntax import Syntax
from rich import print as rprint
import psutil
import yaml
from datetime import datetime

# Initialize Rich console
console = Console()

# Configuration file path
CONFIG_DIR = Path.home() / ".cli-hub"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
PROCESSES_FILE = CONFIG_DIR / "processes.json"
LOGS_DIR = CONFIG_DIR / "logs"


class CLIHub:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.processes_file = PROCESSES_FILE
        self.logs_dir = LOGS_DIR
        self.ensure_config_exists()
        self.load_config()
        self.load_processes()

    def ensure_config_exists(self):
        """Ensure configuration directory and files exist"""
        self.config_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        if not self.config_file.exists():
            default_config = {
                "scripts": {},
                "aliases": {},
                "default_timeout": 30,
                "max_log_size": "10MB",
                "auto_cleanup": True,
            }
            with open(self.config_file, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)

        if not self.processes_file.exists():
            with open(self.processes_file, "w") as f:
                json.dump({}, f)

    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, "r") as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            self.config = {"scripts": {}, "aliases": {}}

    def save_config(self):
        """Save configuration to YAML file"""
        try:
            with open(self.config_file, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            console.print(f"[red]Error saving config: {e}[/red]")

    def load_processes(self):
        """Load background processes information"""
        try:
            with open(self.processes_file, "r") as f:
                self.processes = json.load(f)
        except Exception as e:
            self.processes = {}

    def save_processes(self):
        """Save background processes information"""
        try:
            with open(self.processes_file, "w") as f:
                json.dump(self.processes, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving processes: {e}[/red]")

    def add_script(
        self, name: str, command: str, description: str = "", working_dir: str = ""
    ):
        """Add a new script to the hub"""
        self.config["scripts"][name] = {
            "command": command,
            "description": description,
            "working_dir": working_dir or os.getcwd(),
            "added_at": datetime.now().isoformat(),
        }
        self.save_config()
        console.print(f"[green]✓ Added script '{name}'[/green]")

    def remove_script(self, name: str):
        """Remove a script from the hub"""
        if name in self.config["scripts"]:
            del self.config["scripts"][name]
            self.save_config()
            console.print(f"[green]✓ Removed script '{name}'[/green]")
        else:
            console.print(f"[red]Script '{name}' not found[/red]")

    def list_scripts(self):
        """List all registered scripts"""
        if not self.config["scripts"]:
            console.print("[yellow]No scripts registered[/yellow]")
            return

        table = Table(title="Registered Scripts")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Command", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Working Dir", style="blue")

        for name, info in self.config["scripts"].items():
            table.add_row(
                name,
                (
                    info["command"][:50] + "..."
                    if len(info["command"]) > 50
                    else info["command"]
                ),
                info.get("description", ""),
                info.get("working_dir", ""),
            )

        console.print(table)

    def run_script(self, name: str, args: List[str] = None, background: bool = False):
        """Run a registered script"""
        if name not in self.config["scripts"]:
            console.print(f"[red]Script '{name}' not found[/red]")
            # Show available scripts
            if self.config["scripts"]:
                console.print("\n[yellow]Available scripts:[/yellow]")
                for script_name in self.config["scripts"].keys():
                    console.print(f"  • {script_name}")
            return False

        script_info = self.config["scripts"][name]
        command = script_info["command"]
        working_dir = script_info.get("working_dir", os.getcwd())

        # Add additional arguments if provided
        if args:
            command += " " + " ".join(args)

        if background:
            return self._run_background(name, command, working_dir)
        else:
            return self._run_foreground(command, working_dir)

    def _run_foreground(self, command: str, working_dir: str):
        """Run command in foreground"""
        try:
            console.print(f"[blue]Running: {command}[/blue]")
            console.print(f"[dim]Working directory: {working_dir}[/dim]")

            process = subprocess.run(command, shell=True, cwd=working_dir, text=True)

            if process.returncode == 0:
                console.print("[green]✓ Command completed successfully[/green]")
                return True
            else:
                console.print(
                    f"[red]✗ Command failed with exit code {process.returncode}[/red]"
                )
                return False

        except Exception as e:
            console.print(f"[red]Error running command: {e}[/red]")
            return False

    def _run_background(self, name: str, command: str, working_dir: str):
        """Run command in background"""
        try:
            log_file = self.logs_dir / f"{name}_{int(time.time())}.log"

            # Add environment variable to disable Python buffering
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"

            with open(log_file, "w") as f:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=working_dir,
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env,
                    bufsize=0,  # Unbuffered
                )

            # Store process information
            process_info = {
                "pid": process.pid,
                "command": command,
                "working_dir": working_dir,
                "started_at": datetime.now().isoformat(),
                "log_file": str(log_file),
                "status": "running",
            }

            self.processes[name] = process_info
            self.save_processes()

            console.print(
                f"[green]✓ Started '{name}' in background (PID: {process.pid})[/green]"
            )
            console.print(f"[dim]Log file: {log_file}[/dim]")
            return True

        except Exception as e:
            console.print(f"[red]Error starting background process: {e}[/red]")
            return False

    def list_background_processes(self):
        """List all background processes"""
        if not self.processes:
            console.print("[yellow]No background processes[/yellow]")
            return

        table = Table(title="Background Processes")
        table.add_column("Name", style="cyan")
        table.add_column("PID", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Started", style="blue")
        table.add_column("Command", style="white")

        for name, info in self.processes.items():
            # Check if process is still running
            status = self._get_process_status(info["pid"])
            if status != info.get("status"):
                info["status"] = status
                self.save_processes()

            table.add_row(
                name,
                str(info["pid"]),
                status,
                info["started_at"][:19],  # Remove milliseconds
                (
                    info["command"][:50] + "..."
                    if len(info["command"]) > 50
                    else info["command"]
                ),
            )

        console.print(table)

    def _get_process_status(self, pid: int) -> str:
        """Get the current status of a process"""
        try:
            process = psutil.Process(pid)
            if process.is_running():
                return "running"
            else:
                return "stopped"
        except psutil.NoSuchProcess:
            return "stopped"
        except Exception:
            return "unknown"

    def stop_background_process(self, name: str):
        """Stop a background process"""
        if name not in self.processes:
            console.print(f"[red]Background process '{name}' not found[/red]")
            return False

        process_info = self.processes[name]
        pid = process_info["pid"]

        try:
            process = psutil.Process(pid)
            if process.is_running():
                process.terminate()

                # Wait for graceful termination
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    process.kill()
                    console.print(f"[yellow]Force killed process {pid}[/yellow]")

                console.print(f"[green]✓ Stopped process '{name}' (PID: {pid})[/green]")
            else:
                console.print(f"[yellow]Process '{name}' was already stopped[/yellow]")

            process_info["status"] = "stopped"
            self.save_processes()
            return True

        except psutil.NoSuchProcess:
            console.print(f"[yellow]Process '{name}' was already stopped[/yellow]")
            process_info["status"] = "stopped"
            self.save_processes()
            return True
        except Exception as e:
            console.print(f"[red]Error stopping process: {e}[/red]")
            return False

    def get_process_output(self, name: str, lines: int = 50):
        """Get the last output from a background process"""
        if name not in self.processes:
            console.print(f"[red]Background process '{name}' not found[/red]")
            return

        process_info = self.processes[name]
        log_file = Path(process_info["log_file"])

        if not log_file.exists():
            console.print(f"[red]Log file not found: {log_file}[/red]")
            return

        try:
            with open(log_file, "r") as f:
                all_lines = f.readlines()
                recent_lines = (
                    all_lines[-lines:] if len(all_lines) > lines else all_lines
                )

            console.print(
                Panel(
                    "".join(recent_lines),
                    title=f"Output from '{name}' (last {len(recent_lines)} lines)",
                    border_style="blue",
                )
            )

        except Exception as e:
            console.print(f"[red]Error reading log file: {e}[/red]")

    def cleanup_stopped_processes(self):
        """Remove stopped processes from the list"""
        to_remove = []

        for name, info in self.processes.items():
            if self._get_process_status(info["pid"]) == "stopped":
                to_remove.append(name)

        for name in to_remove:
            del self.processes[name]

        self.save_processes()

        if to_remove:
            console.print(
                f"[green]✓ Cleaned up {len(to_remove)} stopped processes[/green]"
            )
        else:
            console.print("[yellow]No stopped processes to clean up[/yellow]")

    def interactive_add_script(self):
        """Interactive script addition wizard"""
        console.print(Panel("🧙 Script Addition Wizard", style="bold blue"))

        # Get script name
        name = Prompt.ask("[cyan]Script name")
        if name in self.config["scripts"]:
            if not Confirm.ask(
                f"[yellow]Script '{name}' already exists. Replace?[/yellow]"
            ):
                return

        # Get command with templates
        console.print("\n[yellow]Choose a template or enter custom command:[/yellow]")
        templates = {
            "1": "python script.py",
            "2": "node script.js",
            "3": "npm run command",
            "4": "docker run image",
            "5": "custom command",
        }

        for key, template in templates.items():
            console.print(f"  {key}. {template}")

        template_choice = Prompt.ask(
            "Choose template", choices=list(templates.keys()), default="5"
        )

        if template_choice == "5":
            command = Prompt.ask("[cyan]Command")
        else:
            base_template = templates[template_choice]
            command = Prompt.ask(f"[cyan]Command", default=base_template)

        # Get description
        description = Prompt.ask("[cyan]Description", default="")

        # Get working directory
        current_dir = os.getcwd()
        workdir = Prompt.ask(f"[cyan]Working directory", default=current_dir)

        # Ask about argument handling
        supports_args = Confirm.ask(
            "[yellow]Does this script accept additional arguments?[/yellow]",
            default=True,
        )

        if supports_args:
            arg_style = Prompt.ask(
                "[cyan]Argument style",
                choices=["append", "subcommand", "flags"],
                default="append",
            )

            if arg_style == "subcommand":
                subcommands = Prompt.ask(
                    "[cyan]Common subcommands (comma-separated)", default=""
                )
                if subcommands:
                    # Store subcommands for future interactive use
                    self.config["scripts"][name] = {
                        "command": command,
                        "description": description,
                        "working_dir": workdir,
                        "added_at": datetime.now().isoformat(),
                        "supports_args": True,
                        "arg_style": arg_style,
                        "subcommands": [s.strip() for s in subcommands.split(",")],
                    }

        # Add the script
        self.add_script(name, command, description, workdir)

        # Ask if they want to test it
        if Confirm.ask("[green]Test the script now?[/green]", default=False):
            self.interactive_run_script(name)

    def interactive_run_script(self, name: str):
        """Interactive script runner with argument prompting"""
        if name not in self.config["scripts"]:
            console.print(f"[red]Script '{name}' not found[/red]")
            return

        script_info = self.config["scripts"][name]
        console.print(Panel(f"🚀 Running: {name}", style="bold green"))
        console.print(f"[dim]Command: {script_info['command']}[/dim]")
        console.print(
            f"[dim]Description: {script_info.get('description', 'N/A')}[/dim]"
        )

        args = []

        # Check if script supports arguments
        if script_info.get("supports_args", False):
            arg_style = script_info.get("arg_style", "append")

            if arg_style == "subcommand" and "subcommands" in script_info:
                console.print("\n[yellow]Available subcommands:[/yellow]")
                subcommands = script_info["subcommands"]
                for i, sub in enumerate(subcommands, 1):
                    console.print(f"  {i}. {sub}")

                choice = Prompt.ask(
                    "Choose subcommand or enter custom",
                    choices=[str(i) for i in range(1, len(subcommands) + 1)]
                    + ["custom"],
                    default="custom",
                )

                if choice != "custom":
                    args.append(subcommands[int(choice) - 1])
                else:
                    custom_sub = Prompt.ask("Enter subcommand")
                    if custom_sub:
                        args.append(custom_sub)

            # Ask for additional arguments
            while True:
                additional_arg = Prompt.ask(
                    "Additional arguments (Enter to finish)", default=""
                )
                if not additional_arg:
                    break
                args.append(additional_arg)

        # Ask about execution mode
        if Confirm.ask("[yellow]Run in background?[/yellow]", default=False):
            self.run_script(name, args, background=True)
        else:
            self.run_script(name, args, background=False)

    def interactive_mode(self):
        """Interactive CLI Hub mode"""
        console.print(Panel("🎯 CLI Hub Interactive Mode", style="bold blue"))
        console.print("Type 'help' for commands, 'exit' to quit\n")

        while True:
            try:
                command = Prompt.ask("[bold green]hub>[/bold green]").strip().lower()

                if not command:
                    continue

                if command in ["exit", "quit", "q"]:
                    console.print("[green]Goodbye![/green]")
                    break

                elif command == "help":
                    self._show_interactive_help()

                elif command == "list" or command == "ls":
                    self.list_scripts()

                elif command == "add":
                    self.interactive_add_script()

                elif command.startswith("run "):
                    script_name = command[4:].strip()
                    if script_name:
                        self.interactive_run_script(script_name)
                    else:
                        console.print("[red]Usage: run <script_name>[/red]")

                elif command == "ps":
                    self.list_background_processes()

                elif command.startswith("logs "):
                    script_name = command[5:].strip()
                    if script_name:
                        lines = IntPrompt.ask("Number of lines", default=20)
                        self.get_process_output(script_name, lines)
                    else:
                        console.print("[red]Usage: logs <script_name>[/red]")

                elif command.startswith("stop "):
                    script_name = command[5:].strip()
                    if script_name:
                        self.stop_background_process(script_name)
                    else:
                        console.print("[red]Usage: stop <script_name>[/red]")

                elif command == "status":
                    self._show_status()

                elif command == "cleanup":
                    self.cleanup_stopped_processes()

                elif command.startswith("remove "):
                    script_name = command[7:].strip()
                    if script_name:
                        if Confirm.ask(f"[red]Remove script '{script_name}'?[/red]"):
                            self.remove_script(script_name)
                    else:
                        console.print("[red]Usage: remove <script_name>[/red]")

                elif command not in [
                    "help",
                    "list",
                    "ls",
                    "add",
                    "run",
                    "ps",
                    "logs",
                    "stop",
                    "status",
                    "cleanup",
                    "remove",
                ]:
                    # Try to execute as native command
                    console.print(
                        f"[yellow]Script '{command}' not found. Trying as native command...[/yellow]"
                    )
                    success = self._run_foreground(command, os.getcwd())
                    if not success:
                        console.print(
                            f"[red]Command '{command}' failed or not found[/red]"
                        )
                        console.print(
                            "[dim]Type 'help' for available commands or 'list' to see registered scripts[/dim]"
                        )

                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("[dim]Type 'help' for available commands[/dim]")

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except EOFError:
                console.print("\n[green]Goodbye![/green]")
                break

    def _show_interactive_help(self):
        """Show interactive mode help"""
        help_text = """
[bold cyan]Available Commands:[/bold cyan]

[yellow]Script Management:[/yellow]
  list, ls          List all scripts
  add              Interactive script wizard
  remove <name>    Remove a script
  run <name>       Run script interactively

[yellow]Process Management:[/yellow]
  ps               List background processes
  stop <name>      Stop background process
  logs <name>      View process logs
  cleanup          Clean stopped processes

[yellow]General:[/yellow]
  status           Show hub status
  help             Show this help
  exit, quit, q    Exit interactive mode
        """
        console.print(Panel(help_text, title="Help", border_style="blue"))

    def _show_status(self):
        """Show hub status (used by interactive mode)"""
        scripts_count = len(self.config["scripts"])
        running_processes = sum(
            1
            for info in self.processes.values()
            if self._get_process_status(info["pid"]) == "running"
        )

        panel_content = f"""
[bold cyan]CLI Hub Status[/bold cyan]

[green]Scripts registered:[/green] {scripts_count}
[blue]Background processes:[/blue] {len(self.processes)}
[yellow]Currently running:[/yellow] {running_processes}

[dim]Config directory:[/dim] {self.config_dir}
[dim]Logs directory:[/dim] {self.logs_dir}
        """

        console.print(Panel(panel_content, title="Status", border_style="green"))


# Initialize the hub
hub = CLIHub()


@click.group()
def cli():
    """CLI Hub - Central management for your command-line applications"""
    pass


@cli.command()
@click.argument("name")
@click.argument("command")
@click.option("--description", "-d", default="", help="Description of the script")
@click.option("--workdir", "-w", default="", help="Working directory for the script")
def add(name, command, description, workdir):
    """Add a new script to the hub"""
    hub.add_script(name, command, description, workdir)


@cli.command()
@click.argument("name")
def remove(name):
    """Remove a script from the hub"""
    hub.remove_script(name)


@cli.command("list")
def list_scripts():
    """List all registered scripts"""
    hub.list_scripts()


@cli.command()
@click.argument("name")
@click.argument("args", nargs=-1)
@click.option("--background", "-b", is_flag=True, help="Run in background")
@click.option(
    "--interactive", "-i", is_flag=True, help="Interactive argument prompting"
)
def run(name, args, background, interactive):
    """Run a registered script"""
    if interactive:
        hub.interactive_run_script(name)
    else:
        # If no args provided and script exists, check if we should prompt
        if not args and name in hub.config.get("scripts", {}):
            script_info = hub.config["scripts"][name]
            if script_info.get("supports_args", False):
                if Confirm.ask(
                    f"[yellow]Script '{name}' accepts arguments. Run interactively?[/yellow]",
                    default=True,
                ):
                    hub.interactive_run_script(name)
                    return

        hub.run_script(name, list(args), background)


@cli.command()
def ps():
    """List background processes"""
    hub.list_background_processes()


@cli.command()
@click.argument("name")
def stop(name):
    """Stop a background process"""
    hub.stop_background_process(name)


@cli.command()
@click.argument("name")
@click.option("--lines", "-n", default=50, help="Number of lines to show")
def logs(name, lines):
    """Show logs from a background process"""
    hub.get_process_output(name, lines)


@cli.command()
def cleanup():
    """Clean up stopped background processes"""
    hub.cleanup_stopped_processes()


@cli.command()
def status():
    """Show hub status and statistics"""
    scripts_count = len(hub.config["scripts"])
    running_processes = sum(
        1
        for info in hub.processes.values()
        if hub._get_process_status(info["pid"]) == "running"
    )

    panel_content = f"""
[bold cyan]CLI Hub Status[/bold cyan]

[green]Scripts registered:[/green] {scripts_count}
[blue]Background processes:[/blue] {len(hub.processes)}
[yellow]Currently running:[/yellow] {running_processes}

[dim]Config directory:[/dim] {hub.config_dir}
[dim]Logs directory:[/dim] {hub.logs_dir}
    """

    console.print(Panel(panel_content, title="Status", border_style="green"))


@cli.command()
@click.argument("command")
@click.option("--background", "-b", is_flag=True, help="Run in background")
@click.option("--name", "-n", help="Name for background process")
def exec(command, background, name):
    """Execute a command directly"""
    if background:
        if not name:
            name = f"exec_{int(time.time())}"
        hub._run_background(name, command, os.getcwd())
    else:
        hub._run_foreground(command, os.getcwd())


@cli.command()
def wizard():
    """Launch interactive script addition wizard"""
    hub.interactive_add_script()


@cli.command()
@click.argument("name")
def irun(name):
    """Run a script interactively with argument prompting"""
    hub.interactive_run_script(name)


@cli.command()
def interactive():
    """Launch interactive CLI Hub mode"""
    hub.interactive_mode()


@cli.command()
@click.argument("name")
@click.option("--template", "-t", help="Use a template (python, node, npm, docker)")
@click.option("--interactive", "-i", is_flag=True, help="Use interactive wizard")
def smart_add(name, template, interactive):
    """Smart script addition with templates and prompting"""
    if interactive:
        hub.interactive_add_script()
        return

    if template:
        templates = {
            "python": "python script.py",
            "node": "node script.js",
            "npm": "npm run command",
            "docker": "docker run image",
        }

        if template in templates:
            base_command = templates[template]
            command = Prompt.ask(f"[cyan]Command", default=base_command)
            description = Prompt.ask(
                f"[cyan]Description", default=f"{template.title()} script"
            )
            workdir = Prompt.ask(f"[cyan]Working directory", default=os.getcwd())

            hub.add_script(name, command, description, workdir)
        else:
            console.print(f"[red]Unknown template: {template}[/red]")
            console.print(
                "[yellow]Available templates: python, node, npm, docker[/yellow]"
            )
    else:
        console.print("[yellow]Use --template or --interactive flag[/yellow]")


if __name__ == "__main__":
    cli()
