# Roadmap

## Phase 0 -- Scope and design contract

- [x] Repository scaffold: Python 3.13, uv, ruff, strict mypy, pytest, CI
- [x] Fixed-membership cluster configuration with quorum math
- [x] Design docs: scope, fault model, limitations, glossary, roadmap
- [x] README with no unimplemented claims

## Phase 1 -- Raft consensus core

- [ ] Type definitions: Term, LogIndex, NodeId, Entry
- [ ] Raft state: Follower, Candidate, Leader role variants
- [ ] Message types: RequestVote, AppendEntries, InstallSnapshot (and responses)
- [ ] Event types: MessageReceived, Tick, Propose
- [ ] Action types: SendMessage, PersistState, ApplyEntry, TakeSnapshot
- [ ] Pure state transition function: `(State, Event) -> (State, list[Action])`
- [ ] Leader election with randomized timeouts
- [ ] Pre-vote protocol
- [ ] Log replication with consistency checks
- [ ] Commit index advancement on quorum acknowledgment

## Phase 2 -- Persistence

- [ ] SQLite storage backend for persistent state (term, voted-for, log)
- [ ] Write-ahead semantics: persist before acknowledging
- [ ] Crash recovery: reconstruct volatile state from durable state
- [ ] Atomic snapshot writes (write-temp, fsync, rename)
- [ ] Log compaction after snapshot

## Phase 3 -- Key-value state machine

- [ ] Deterministic KV state machine: PUT, DELETE, CAS, GET
- [ ] Client session registration and deduplication
- [ ] Exactly-once semantics via session ID + sequence number
- [ ] Linearizable reads via quorum confirmation

## Phase 4 -- Networking

- [ ] asyncio TCP transport between nodes
- [ ] msgpack serialization for the wire protocol
- [ ] FastAPI HTTP gateway for client-facing API
- [ ] Connection management and reconnection

## Phase 5 -- Simulation and testing

- [ ] Deterministic simulation harness with seeded PRNG
- [ ] Simulated message delivery: delay, drop, duplicate, reorder
- [ ] Simulated network partitions
- [ ] Simulated node crashes and restarts
- [ ] Linearizability checker
- [ ] Property-based tests with Hypothesis for state transitions
- [ ] Correctness report: seeds, traces, invariant coverage

## Phase 6 -- Demo and observability

- [ ] Docker Compose 5-node cluster
- [ ] CLI demo client with narrated walkthrough
- [ ] Structured logging with structlog
- [ ] asciinema recording for README
- [ ] Optional: Prometheus metrics + Grafana dashboard

## Non-goals for v1

See `docs/scope.md` for excluded features and rationale.
