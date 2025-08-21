#!/usr/bin/env python3
"""
Setup script to make cli_hub easily accessible
"""

import os
from pathlib import Path


def create_symlink():
    """Create a symlink to make cli_hub accessible from anywhere"""
    script_path = Path(__file__).parent / "cli_hub.py"

    # Make the script executable
    os.chmod(script_path, 0o755)

    # Get user's local bin directory
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)

    symlink_path = local_bin / "hub"

    try:
        if symlink_path.exists():
            symlink_path.unlink()

        symlink_path.symlink_to(script_path)
        print(f"✓ Created symlink: {symlink_path} -> {script_path}")

        # Check if ~/.local/bin is in PATH
        path_env = os.environ.get("PATH", "")
        if str(local_bin) not in path_env:
            shell_config = Path.home() / ".zshrc"
            if shell_config.exists():
                with open(shell_config, "a", encoding="utf-8") as f:
                    f.write(f'\n# Added by CLI Hub\nexport PATH="$PATH:{local_bin}"\n')
                print(f"✓ Added {local_bin} to PATH in {shell_config}")
                print("Please run 'source ~/.zshrc' or restart your terminal")
            else:
                print(f"Please add {local_bin} to your PATH")

        print("\n🎉 CLI Hub installed successfully!")
        print("You can now use 'hub' command from anywhere")

    except (OSError, FileNotFoundError, PermissionError) as e:
        print(f"Error creating symlink: {e}")
        return False

    return True


if __name__ == "__main__":
    create_symlink()
