# Limitations

This document lists known limitations of Keel that follow from deliberate
scope decisions, architectural trade-offs, or the current stage of
implementation.  Each limitation includes the reason it exists and, where
applicable, what would be needed to remove it.

## Static membership

Keel clusters have a fixed set of nodes declared at startup.  Adding or
removing nodes requires stopping the entire cluster, updating the
configuration, and restarting all nodes.

**Why:** Dynamic membership (Raft joint consensus or single-server changes)
introduces subtle safety hazards, particularly around overlapping
configurations and quorum calculation during transitions.  Excluding it keeps
the invariant space small enough to verify exhaustively in simulation.

**To lift:** Implement the joint-consensus protocol from Raft Section 6, with
a configuration log entry that transitions through C_old,new before committing
C_new.

## Single-key operations only

The key-value API supports PUT, DELETE, CAS, and GET on individual keys.
There are no multi-key transactions, range queries, or batch operations.

**Why:** Multi-key transactions require concurrency control (2PL, OCC, or MVCC)
on top of the replicated log, which is a separate problem from consensus.

**To lift:** Layer a transaction manager over the state machine with a
conflict-detection protocol.  Each transaction becomes a single log entry
containing all mutations.

## No authentication or encryption

All communication between nodes and between clients and the cluster is
unencrypted and unauthenticated.

**Why:** TLS, mTLS, and auth tokens are orthogonal to consensus correctness.
Adding them would increase code surface without improving the educational value
of the Raft implementation.

**To lift:** Add TLS to the asyncio transport layer and a token-based auth
middleware to the HTTP gateway.

## Performance is not a goal

Keel is optimized for clarity and correctness, not throughput or latency.
Python's GIL, the single-threaded event loop, and SQLite as the persistence
backend all impose performance ceilings that are acceptable for this project's
goals.

**Why:** The target audience is someone reading the code to understand Raft, not
someone deploying it in production.

## No persistence portability

The durable state format (SQLite schema) is not versioned and not guaranteed
to be backward-compatible across Keel versions.

**Why:** Schema migration adds complexity with no benefit until the project is
stable enough to warrant upgrading between versions.
