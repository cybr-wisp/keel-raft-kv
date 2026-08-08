# Scope

Keel is a fixed-membership replicated key-value store implementing the Raft
consensus protocol in Python.  It exists to demonstrate correctness-oriented
distributed systems engineering: every invariant is documented, every state
transition is deterministic, and every claim is backed by a reproducible test.

## Included

| Capability | Notes |
|---|---|
| Fixed 3- or 5-node clusters | Membership is declared at startup and never changes. |
| RequestVote RPC | Leader election with randomized timeouts and pre-vote protocol. |
| AppendEntries RPC | Log replication with consistency checks per Raft Section 5.3. |
| InstallSnapshot RPC | Transfer compacted state to slow or recovering followers. |
| Durable SQLite persistence | WAL, log entries, voted-for, current term, and snapshots stored in SQLite. |
| PUT, DELETE, CAS operations | Client-facing key-value mutations. |
| Linearizable GET | Reads go through the leader, which confirms quorum before responding. |
| Replicated client sessions | Each client registers a session; requests carry session ID + sequence number for exactly-once semantics. |
| Snapshots and compaction | State machine checkpointing with atomic writes; log truncation after snapshot. |
| Deterministic simulation | A simulation harness with seeded PRNG controls message delivery, drops, partitions, and crashes. |
| Chaos and linearizability testing | Automated fault injection with linearizability checker to validate correctness under adversarial schedules. |

## Excluded

| Capability | Rationale |
|---|---|
| Dynamic membership changes | Joint consensus and single-server changes add significant complexity with limited educational value for v1. |
| Byzantine fault tolerance | Raft assumes a non-Byzantine model; BFT is a fundamentally different problem. |
| TLS and authentication | Security is orthogonal to consensus correctness; would obscure the core logic. |
| Lease-based reads | Read leases require clock assumptions that complicate the fault model. Quorum reads are sufficient and correct. |
| Rolling upgrades | Requires versioned wire protocols and backward-compatible serialization. Out of scope for v1. |
| Multi-region guarantees | Latency-aware placement, witness replicas, and region-aware quorums are production concerns beyond v1. |
