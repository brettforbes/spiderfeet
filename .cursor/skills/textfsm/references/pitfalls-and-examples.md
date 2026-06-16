# Pitfalls and Worked Examples

## Pitfall table

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Missing `-> Record` | Only last block saved | Add `Record` at row boundaries |
| Context without `Filldown` | Empty column on continuation lines | `Value Filldown Hostname (\S+)` |
| `Filldown` without `Required` | Spurious trailing row | Mark a data column `Required` |
| `List` + immediate `Record` on cont. lines | Values attach to wrong row | `^O -> Continue.Record` before full rule |
| Blank line in Value section | Template parse error | No empty lines between `Value` lines |
| Wrong rule order | Wrong rule matches | Specific rules above general |
| No header skip | Banner corrupts data | Explicit skip rule for headers |
| Implicit EOF `Record` | Unexpected final row | Define empty `EOF` state |
| `Continue` + state change | Template error | Cannot combine |
| Wrong CliTable import | `ModuleNotFoundError` | `from textfsm import clitable` ≥ 1.1.0 |

## Example A — show clock

**Input:**
```
18:42:41.321 PST Sun Feb 8 2009
```

**Template:**
```
Value Year (\d+)
Value MonthDay (\d+)
Value Month (\w+)
Value Timezone (\S+)
Value Time (..:..:..)

Start
  ^${Time}.* ${Timezone} \w+ ${Month} ${MonthDay} ${Year} -> Record
```

## Example B — show ip route OSPF (multi-line List)

**Input:**
```
O 10.4.4.4/32 [110/11] via 10.0.13.3, 1w2d, Ethernet0/2
  [110/11] via 10.0.14.4, 1w2d, Ethernet0/3
```

**Template:**
```
Value NETWORK (\S+)
Value MASK (\d+)
Value DISTANCE (\d+)
Value METRIC (\d+)
Value List NEXTHOP (\S+)

Start
  ^O -> Continue.Record
  ^O +${NETWORK}/${MASK}\s\[${DISTANCE}/${METRIC}\]\svia\s${NEXTHOP},
  ^\s+\[${DISTANCE}/${METRIC}\]\svia\s${NEXTHOP},
```

## Example C — show ip arp

**Template:**
```
Value Required PROTOCOL (\S+)
Value Required IP_ADDRESS (\d+\.\d+\.\d+\.\d+)
Value Required AGE (\S+)
Value Required MAC_ADDRESS (\S+)
Value Required TYPE (\S+)
Value INTERFACE (\S+)

Start
  ^Protocol\s+Address\s+Age
  ^${PROTOCOL}\s+${IP_ADDRESS}\s+${AGE}\s+${MAC_ADDRESS}\s+${TYPE}\s+${INTERFACE} -> Record
  ^${PROTOCOL}\s+${IP_ADDRESS}\s+${AGE}\s+${MAC_ADDRESS}\s+${TYPE} -> Record
  ^. -> Error
```

## Example D — Netdiscover -P output (SpiderFeet target)

Typical columns: IP, MAC, Count, Len, Vendor.

```
Value Required IP (\d+\.\d+\.\d+\.\d+)
Value Required MAC ([0-9a-fA-F:]{17})
Value COUNT (\d+)
Value LEN (\d+)
Value VENDOR (.+)

Start
  ^\s*IP\s+At MAC
  ^\s*${IP}\s+${MAC}\s+${COUNT}\s+${LEN}\s+${VENDOR}\s*$$ -> Record
```

Map: IP → `IP_ADDRESS`, MAC → `MAC_ADDRESS`, Vendor → attribute edge.
