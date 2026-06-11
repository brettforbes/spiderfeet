#!/usr/bin/env bash
# Run quarantine battery for CLI tools inside WSL (does not touch Windows .venv).
set -euo pipefail

REPO="${SPIDERFEET_REPO:-/mnt/c/projects/spiderfeet}"
export PATH="$HOME/.local/bin:$PATH"
export POETRY_VIRTUALENVS_IN_PROJECT=false
export POETRY_CACHE_DIR="${POETRY_CACHE_DIR:-$HOME/.cache/pypoetry}"

source "$HOME/.local/spiderfeet-cli/manifest.env"

cd "$REPO"
if [[ ! -f "$HOME/.local/spiderfeet-cli/manifest.env" ]]; then
  echo "Run install_wsl_cli_tools.sh first" >&2
  exit 1
fi

poetry env use python3 >/dev/null 2>&1 || true
poetry install --no-interaction --sync

MODULES=(
  sfp_tool_cmseek
  sfp_tool_testsslsh
  sfp_tool_whatweb
  sfp_tool_nbtscan
  sfp_tool_onesixtyone
  sfp_tool_wappalyzer
)

poetry run python .seed/scripts/run_quarantine_battery.py \
  --local \
  --timeout 300 \
  --only "${MODULES[@]}" \
  --write \
  --promote \
  "$@"
