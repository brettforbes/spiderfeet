# mapcidr Output and Parsing

Most workflows consume one value per line (IP or CIDR).

## Parsing Steps

1. Trim line.
2. Skip empty lines.
3. Validate as IP or CIDR.
4. Emit canonical string form.
5. Attach source provenance metadata.

## Python Example

```python
import ipaddress

for raw in lines:
    line = raw.strip()
    if not line:
        continue
    try:
        print(ipaddress.ip_address(line).compressed)
        continue
    except ValueError:
        pass
    try:
        print(ipaddress.ip_network(line, strict=False).compressed)
    except ValueError:
        continue
```
