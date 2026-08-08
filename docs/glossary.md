# Glossary

Terms used throughout Keel's codebase and documentation.  Definitions follow
the Raft paper (Ongaro & Ousterhout, 2014) unless noted otherwise.

**Action.**  An output produced by a state transition.  Actions are
instructions to the runtime: send a message, persist state, apply a committed
entry to the state machine, or take a snapshot.  The consensus core never
executes actions itself; it only emits them.

**AppendEntries.**  The RPC used by the leader to replicate log entries to
followers and to serve as a heartbeat when the entry list is empty.

**Candidate.**  A node that has started an election by incrementing its term
and requesting votes from its peers.

**CAS (Compare-And-Swap).**  A conditional write operation: set key K to value
V only if K's current value equals some expected value E.  Fails if the
current value differs.

**Client session.**  A server-side record associating a client with a
monotonically increasing sequence number.  Used to deduplicate retried
requests and provide exactly-once semantics.

**Commit.**  A log entry is committed when the leader has replicated it to a
quorum of nodes.  Committed entries are durable and will never be overwritten.

**Commit index.**  The index of the highest log entry known to be committed.
Entries up to and including the commit index are safe to apply to the state
machine.

**Election timeout.**  The duration a follower waits without hearing from a
leader before becoming a candidate.  Randomized to avoid split votes.

**Entry.**  A single record in the replicated log, containing a term number,
a log index, and a command (or a no-op for leader establishment).

**Event.**  An input to the consensus core: a message received from a peer, a
clock tick, or a client proposal.

**Follower.**  A node that accepts log entries from the current leader and
responds to RequestVote RPCs.

**Heartbeat.**  An empty AppendEntries RPC sent by the leader to maintain its
authority and prevent unnecessary elections.

**InstallSnapshot.**  The RPC used by the leader to send a snapshot to a
follower that is too far behind for log-based catch-up.

**Leader.**  The node responsible for accepting client requests, replicating
log entries, and advancing the commit index.  At most one leader per term.

**Linearizability.**  A consistency guarantee: every operation appears to take
effect at a single point in time between its invocation and its response, and
the resulting order is consistent with real-time ordering.

**Log.**  The ordered sequence of entries that records all state transitions.
The log is the source of truth for replication.

**Majority / Quorum.**  A strict majority of the cluster: ceil(n/2) nodes for
a cluster of size n.  Required for elections and commits.

**Node.**  A single process participating in the Raft cluster.  Each node
maintains its own copy of the log and state machine.

**Persistent state.**  State that must survive crashes: current term, voted-for,
and the log entries.  Stored in SQLite.

**Pre-vote.**  An optional protocol extension where a candidate solicits
"pre-votes" before incrementing its term, preventing disruptive elections from
partitioned nodes that would otherwise force term inflation.

**Replicated state machine.**  A deterministic state machine that each node
applies committed log entries to, in order.  All nodes that apply the same
sequence of entries arrive at the same state.

**RequestVote.**  The RPC used by a candidate to solicit votes during an
election.

**Snapshot.**  A compact representation of the state machine at a given log
index.  Allows log truncation and fast catch-up for slow followers.

**State transition.**  A pure function: given the current state and an event,
produce a new state and a list of actions.  The core of Keel's Raft
implementation.

**Term.**  A logical clock that increases monotonically.  Each term has at most
one leader.  Terms are used to detect stale messages and resolve conflicts.

**Volatile state.**  State that can be reconstructed after a crash: commit
index, last applied index, and (on leaders) next-index and match-index arrays.

**WAL (Write-Ahead Log).**  The durable log that entries are written to before
being acknowledged.  In Keel, SQLite in WAL mode serves this role.
