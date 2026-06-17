# MSFvenom Workflows

Common tasks:

- List payloads, formats, encoders.
- Generate payload with explicit platform/arch/format/output.
- Handle badchars and optional encoders only when needed.
- Pair reverse payloads with `exploit/multi/handler`.

Safety:

- Lab-only by default.
- Treat payload generation as sensitive behavior.
