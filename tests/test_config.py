"""Tests for cluster configuration and fixed-membership constraints."""

from __future__ import annotations

import pytest

import keel
from keel.config import ClusterConfig, NodeId


class TestPackageImport:
    """Verify that the package is importable and exposes a version."""

    def test_version_exists(self) -> None:
        assert hasattr(keel, "__version__")

    def test_version_is_string(self) -> None:
        assert isinstance(keel.__version__, str)


class TestClusterConfig:
    """Fixed-membership cluster configuration."""

    @staticmethod
    def _ids(*args: int) -> tuple[NodeId, ...]:
        return tuple(NodeId(i) for i in args)

    def test_three_node_cluster(self) -> None:
        cfg = ClusterConfig(node_ids=self._ids(1, 2, 3))
        assert cfg.size == 3
        assert cfg.quorum == 2

    def test_five_node_cluster(self) -> None:
        cfg = ClusterConfig(node_ids=self._ids(1, 2, 3, 4, 5))
        assert cfg.size == 5
        assert cfg.quorum == 3

    def test_rejects_single_node(self) -> None:
        with pytest.raises(ValueError, match="cluster size must be 3 or 5"):
            ClusterConfig(node_ids=self._ids(1))

    def test_rejects_even_cluster(self) -> None:
        with pytest.raises(ValueError, match="cluster size must be 3 or 5"):
            ClusterConfig(node_ids=self._ids(1, 2, 3, 4))

    def test_rejects_duplicate_ids(self) -> None:
        with pytest.raises(ValueError, match="node_ids must be unique"):
            ClusterConfig(node_ids=self._ids(1, 1, 3))

    def test_config_is_immutable(self) -> None:
        cfg = ClusterConfig(node_ids=self._ids(1, 2, 3))
        with pytest.raises(AttributeError):
            cfg.node_ids = self._ids(4, 5, 6)  # type: ignore[misc]
