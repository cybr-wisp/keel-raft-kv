# Fault Model

Keel targets a **non-Byzantine crash-recovery** fault model.  This document
defines what failures the system tolerates, what it does not, and the
assumptions that underpin correctness.

## Assumptions

**Crash-stop with recovery.**  A node may crash at any point and restart with
its durable state (SQLite database) intact.  Between crash and recovery, the
node is unreachable and participates in no RPCs.  On restart it resumes from
its last persisted state.

**Reliable storage.**  Durable writes (SQLite with WAL mode, fsync on commit)
survive crashes.  Keel does not handle silent data corruption, bit rot, or
partial disk writes beyond what SQLite's own integrity mechanisms detect.

**Asynchronous network.**  Messages between nodes may be delayed, duplicated,
reordered, or dropped entirely.  There is no upper bound on message delivery
time.  The network may partition any subset of nodes for any duration.

**No Byzantine behavior.**  Nodes execute the protocol faithfully.  They do not
send forged, malformed, or intentionally misleading messages.  All nodes run
the same software version.

**Monotonic clocks.**  Logical clocks (term numbers) are strictly monotonic.
Physical clocks may drift but do not go backward.  Keel uses physical time
only for election timeout jitter, never for correctness-critical decisions.

## Tolerances

| Cluster size | Maximum simultaneous failures | Quorum |
|---|---|---|
| 3 nodes | 1 | 2 |
| 5 nodes | 2 | 3 |

The system makes progress as long as a strict majority of nodes are alive and
able to communicate with each other.

## Failure modes handled

- **Node crash and restart** -- the node catches up via AppendEntries or
  InstallSnapshot from the current leader.
- **Network partition** -- the majority partition elects a leader and continues
  serving requests; the minority partition stalls.  When the partition heals,
  minority nodes rejoin and replicate the log they missed.
- **Message loss, duplication, and reordering** -- Raft RPCs are idempotent.
  Duplicate messages are safe.  Out-of-order messages are handled by term and
  log index checks.
- **Slow followers** -- the leader sends snapshots to followers that are too
  far behind for log-based catch-up.
- **Leader failure during replication** -- uncommitted entries may be lost; the
  new leader's log is authoritative.  Committed entries are never lost.

## Failure modes NOT handled

- **Disk corruption or silent data loss** -- a node that returns corrupted data
  from disk may violate safety.
- **Byzantine nodes** -- a node that fabricates votes, forges log entries, or
  lies about its term can break consensus.
- **Clock reversal** -- if a node's monotonic clock goes backward, election
  timeouts may behave incorrectly.
- **Resource exhaustion** -- unbounded log growth without compaction will
  eventually exhaust disk.  Snapshots mitigate this but do not eliminate it.
