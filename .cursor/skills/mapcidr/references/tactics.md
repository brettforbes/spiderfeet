# mapcidr Tactics and Workflows

## Workflow: Netblock to Scan Queue

1. Expand all authorized netblocks.
2. De-duplicate host outputs.
3. Chunk hosts for scanner-safe batches.
4. Track provenance netblock -> host.

## Workflow: Differential Updates

1. Re-expand latest netblocks.
2. Compare against previous host snapshot.
3. Scan only net-new hosts first.

## Tactics

- Normalize once, reuse everywhere.
- Keep both block-level and host-level views.
- Prioritize smaller/high-value ranges first.
