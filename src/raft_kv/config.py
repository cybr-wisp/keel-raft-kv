"""Cluster configuration.

Keel uses **fixed static membership**: the set of nodes is declared at startup
and never changes for the lifetime of the cluster.  Dynamic reconfiguration
(joint consensus, single-server changes) is explicitly out of scope.

See ``docs/scope.md`` and ``docs/limitations.md`` for rationale.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

NodeId = NewType("NodeId", int)
"""Unique identifier for a node within the cluster.  Assigned at startup."""


@dataclass(frozen=True, slots=True)
class ClusterConfig:
    """Immutable description of a fixed-membership Raft cluster.

    Parameters
    ----------
    node_ids:
        The complete, ordered set of node identifiers.  Must contain an odd
        number of members (3 or 5).
    """

    node_ids: tuple[NodeId, ...]

    def __post_init__(self) -> None:
        if len(self.node_ids) not in (3, 5):
            msg = f"cluster size must be 3 or 5, got {len(self.node_ids)}"
            raise ValueError(msg)
        if len(set(self.node_ids)) != len(self.node_ids):
            msg = "node_ids must be unique"
            raise ValueError(msg)

    @property
    def quorum(self) -> int:
        """Minimum votes required for majority (strict majority)."""
        return len(self.node_ids) // 2 + 1

    @property
    def size(self) -> int:
        return len(self.node_ids)
