#!/usr/bin/env python3
"""
Demo script showing the enhanced interactive CLI Hub features
"""

import subprocess
import time


def run_hub_command(cmd):
    """Run a hub command and show output"""
    print(f"\n🎯 Running: hub {cmd}")
    print("=" * 50)
    result = subprocess.run(
        f'export PATH="$PATH:/Users/vymn/.local/bin" && hub {cmd}',
        shell=True,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def main():
    print("🚀 CLI Hub Enhanced Features Demo")
    print("================================\n")

    # Show new help
    run_hub_command("--help")

    # Show current scripts
    print("\n📝 Current registered scripts:")
    run_hub_command("list")

    # Test smart-add with template
    print("\n🎯 Testing smart-add with Python template:")
    print("This would normally be interactive, but showing the concept...")

    # Test running with arguments
    print("\n🏃 Testing activity monitor with arguments:")
    run_hub_command("run activity-monitor status")

    # Show process status
    print("\n📊 Hub status:")
    run_hub_command("status")

    print("\n✨ New Interactive Features Available:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("• hub wizard          - Interactive script addition wizard")
    print("• hub irun <name>     - Run with interactive argument prompting")
    print("• hub interactive     - Enter full interactive mode")
    print("• hub smart-add       - Smart addition with templates")
    print("• hub run -i <name>   - Enhanced run with smart prompting")
    print("\n🎉 Your CLI Hub is now much more powerful and user-friendly!")


if __name__ == "__main__":
    main()
