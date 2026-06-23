#!/usr/bin/env bash
# User-local install for CLI profiling batch (no sudo).
set -euo pipefail
CLI_ROOT="${SPIDERFEET_CLI_ROOT:-$HOME/.local/spiderfeet-cli}"
BIN="$CLI_ROOT/bin"
mkdir -p "$BIN"
export PATH="$BIN:$PATH"

install_nerva() {
  if command -v nerva >/dev/null 2>&1; then return; fi
  local tmp=/tmp/nerva_dl
  mkdir -p "$tmp"
  if curl -fsSL -o "$tmp/nerva.tgz" "https://github.com/praetorian-inc/nerva/releases/download/v0.3.0/nerva_0.3.0_linux_amd64.tar.gz"; then
    tar -xzf "$tmp/nerva.tgz" -C "$tmp"
    install -m 0755 "$tmp/nerva" "$BIN/nerva" 2>/dev/null || cp "$tmp/nerva" "$BIN/nerva"
  elif command -v go >/dev/null 2>&1; then
    GOBIN="$BIN" go install github.com/praetorian-inc/nerva/cmd/nerva@latest
  fi
}

install_netdiscover() {
  if command -v netdiscover >/dev/null 2>&1 || [[ -x "$BIN/netdiscover" ]]; then return; fi
  if [[ -f /usr/include/pcap.h ]] || [[ -f /usr/include/pcap/pcap.h ]]; then
    local src="$CLI_ROOT/netdiscover-src"
    [[ -d "$src/.git" ]] || git clone --depth 1 https://github.com/netdiscover-scanner/netdiscover "$src"
    make -C "$src"
    install -m 0755 "$src/src/netdiscover" "$BIN/netdiscover"
  fi
}

install_nerva
install_netdiscover
echo "nerva: $(command -v nerva || echo MISSING)"
echo "netdiscover: $(command -v netdiscover || echo MISSING)"
