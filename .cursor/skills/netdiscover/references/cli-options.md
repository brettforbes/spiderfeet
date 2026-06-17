# Netdiscover CLI Options

**Synopsis:**

```
netdiscover [-i device] [-r range | -l file | -p] [-s time] [-n node] [-c count]
            [-f] [-d] [-S] [-P] [-L]
```

Newer builds may also support `-m file`, `-F filter`, `-N` (no header with `-P`). Documented below where applicable.

Requires **root** or `CAP_NET_RAW` on Linux for active modes and packet capture.

---

## Target selection (mutually exclusive modes)

| Flag | Description | Example |
|------|-------------|---------|
| *(none)* | Auto-scan common LAN ranges from config or built-in list | `netdiscover -P -N` |
| `-r range` | Scan explicit CIDR(s); comma-separated allowed | `-r 192.168.1.0/24` |
| `-l file` | File with one CIDR per line | `-l ranges.txt` |
| `-p` | Passive: sniff ARP only, send no requests | `-p -i eth0` |

If `-r`, `-l`, and `-p` are all omitted, netdiscover enters **auto-scan** of common private ranges.

---

## `-i device`

Network interface for sniffing and injection.

```bash
netdiscover -i wlan0 -r 192.168.43.0/24
netdiscover -i eth0 -P -N -r 10.0.0.0/24
netdiscover -i tun0 -p          # VPN interface, passive
```

- Omit `-i` to use the first available interface.
- Always set explicitly on multi-homed hosts (Wi-Fi + Ethernet + Docker bridges).

---

## `-r range`

Active ARP scan of the given range.

```bash
netdiscover -r 192.168.1.0/24
netdiscover -r 10.0.0.0/8,172.16.0.0/12
```

Valid forms: `/24`, `/16`, `/8` CIDR notation.

---

## `-l file`

Scan each range listed in `file` (one per line).

```
192.168.1.0/24
10.0.0.0/16
172.16.5.0/24
```

```bash
netdiscover -l targets.txt -P -N
```

---

## `-p`

Passive mode — listen for ARP requests/replies without transmitting.

```bash
netdiscover -p -i eth0
```

- Default when no `-r`/`-l` in some usage guides; combined with auto-scan only when no range flags set.
- Does not complete quickly; operator quits with `q` in interactive mode.
- For automation, prefer `-P -L` active-then-passive if continuous capture is needed.

---

## `-s time`

Milliseconds to sleep **between each ARP request** (default: `1`).

```bash
netdiscover -s 100 -r 192.168.1.0/24    # slower, gentler on fragile networks
netdiscover -s 0 -S -r 192.168.1.0/24   # aggressive (with -S)
```

---

## `-c count`

Number of times to send each ARP request per target IP.

```bash
netdiscover -c 5 -r 192.168.1.0/24
```

Use on networks with **packet loss** or wireless with weak signal.

---

## `-n node`

Last octet of the **scanner's source IP** used during active scan.

- Range: `2`–`253` (default `66`).
- Change when the default source address conflicts with an existing host.

```bash
netdiscover -n 200 -r 192.168.1.0/24
```

---

## `-S`

**Sleep suppression / hardcore mode** — sleep once per 255 hosts instead of after every host.

```bash
netdiscover -S -r 192.168.1.0/24
```

- Faster but can miss hosts on lossy or Wi-Fi networks.
- Avoid combining with high packet loss; prefer `-c` retries instead.

---

## `-f`

**Fast mode** — scan only selected last-octets per subnet (defaults: `.1`, `.100`, `.254`; configurable in `~/.netdiscover/fastips`).

```bash
netdiscover -f -r 192.168.0.0/16
```

Use to **find which /24 blocks are in use** before a full sweep.

---

## `-d`

Ignore configuration files in `~/.netdiscover/`; use built-in defaults for auto-scan and fast-mode octets.

```bash
netdiscover -d -f
```

---

## `-P`

**Parseable output** — print tab-separated rows suitable for scripts; **exit after active scan** completes (unless `-L`).

```bash
netdiscover -P -N -r 192.168.1.0/24
```

Row format (whitespace-separated columns):

```
IP              MAC                 Count   Len   Vendor / Hostname
192.168.1.1     00:14:22:01:23:45   1       60    Dell Inc.
```

See [output-and-parsing.md](output-and-parsing.md).

---

## `-L`

With `-P`, continue execution after active scan to **passively capture** additional ARP traffic.

```bash
netdiscover -P -L -r 192.168.1.0/24
```

Emits parseable lines as new hosts appear; process runs until killed.

---

## `-N` (newer builds)

Suppress header/banner lines when `-P` is set. Recommended for clean TextFSM input.

```bash
netdiscover -P -N -r 192.168.1.0/24
```

---

## `-m file` (newer builds)

File of known `MAC hostname` pairs to enrich the Vendor/Hostname column.

```
00:14:22:01:23:45 server01
08:00:27:53:81:2b workstation-lab
```

```bash
netdiscover -m known_hosts.txt -r 192.168.1.0/24
```

---

## `-F filter` (newer builds)

Custom libpcap filter (default `arp`).

```bash
netdiscover -F "arp and src net 192.168.1.0/24" -r 192.168.1.0/24
```

---

## Interactive screen keys

When running **without** `-P` (TUI mode):

| Key | Action |
|-----|--------|
| `h` | Show help screen |
| `j` / Down arrow | Scroll down |
| `k` / Up arrow | Scroll up |
| `a` | Show ARP replies list |
| `r` | Show ARP requests list |
| `q` | Quit / close help |

**Do not parse TUI output** for automation — always use `-P`.

---

## Configuration files

| Path | Purpose |
|------|---------|
| `~/.netdiscover/ranges` | CIDR list for auto-scan (one per line) |
| `~/.netdiscover/fastips` | Last-octets for `-f` fast mode |

Disabled with `-d`.

Example `ranges`:

```
192.168.21.0/24
172.26.0.0/16
10.0.0.0/8
```

Example `fastips`:

```
1
10
25
254
```

---

## Privilege and platform notes

| Platform | Notes |
|----------|-------|
| Linux | `sudo netdiscover …` |
| macOS | Homebrew `netdiscover`; may need sudo |
| Windows | Use WSL2 or Linux VM; no native port |

---

## Quick reference matrix

| Need | Flags |
|------|-------|
| SpiderFeet / TextFSM | `-P -N -r <cidr>` |
| Stealth | `-p -i <iface>` |
| Lossy network | `-c 3 -s 50` (avoid `-S`) |
| Find busy /24 in /16 | `-f -r 10.0.0.0/16` |
| Continuous ARP watch | `-P -L -r <cidr>` |
| Conflict on .66 source | `-n 200` |
