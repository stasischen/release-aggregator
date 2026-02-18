# Runbook: Windows Environment Setup

This guide details how to set up the Lingo Multi-Repo environment on a Windows machine to ensure compatibility with development and content pipelines.

## 1. Prerequisites

- **Git for Windows**: [Download Here](https://git-scm.com/download/win)
- **Python 3.10+**: [Download Here](https://www.python.org/downloads/windows/) (Ensure "Add Python to PATH" is checked)
- **Flutter SDK**: [Follow Official Guide](https://docs.flutter.dev/get-started/install/windows)

## 2. Git Configuration (Critical)

To prevent line-ending and encoding issues between Mac and Windows:

```powershell
# Set autocrlf to input to keep LF on remote and locally
git config --global core.autocrlf input

# Ensure long paths are supported (required for Dart/Flutter dependencies)
git config --global core.longpaths true
```

## 3. Directory Structure

We recommend maintaining a consistent structure. Create a dev root (e.g., `C:\Dev\lingo`):

```powershell
mkdir C:\Dev\lingo
cd C:\Dev\lingo
```

## 4. Multi-Repo Cloning

Run this PowerShell script to clone all essential repositories:

```powershell
$repos = @(
    "core-schema",
    "content-ko",
    "content-pipeline",
    "release-aggregator",
    "lingo-frontend-web"
)

foreach ($repo in $repos) {
    git clone "git@github.com:stasischen/$repo.git"
}
```

## 5. Agent Identity

On the new machine, create `.agent_identity.json` in each repository root (or the shared aggregator root) to identify this machine in the distributed workflow.

```json
{
    "agent_id": "Agent-Windows-PC",
    "machine_name": "Workstation-Office-1",
    "capabilities": ["build-json", "web-dev"]
}
```

## 6. Python Virtual Environment (Optional but Recommended)

To avoid system-wide dependency conflicts, use a virtual environment within each repository (especially `content-ko` and `content-pipeline`):

```powershell
# Create virtual environment
python -m venv .venv

# Activate environment
.\.venv\Scripts\Activate.ps1

# Install baseline dependencies
pip install -r requirements.txt
pip install google-genai pathspec python-dotenv
```

## 7. Verification

Run the following to ensure the environment is ready:

```powershell
# Check Python
python --version

# Check Flutter
flutter doctor

# Test Content Pipeline (Dry Run)
cd C:\Dev\lingo\content-pipeline
# Refer to content-pipeline/README.md for specific commands
```

## 7. Troubleshooting

- **Encoding**: If Korean characters look mangled in your editor (e.g., VS Code), ensure the file is opened as **UTF-8 with BOM** (or UTF-8-SIG).
- **Permissions**: Run PowerShell as Administrator if you encounter `mkdir` or `git link` errors.
