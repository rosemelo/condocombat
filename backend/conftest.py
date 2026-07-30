"""Pytest fixtures for CondoCombat backend tests."""

import os

# Define SECRET_KEY before any project import to ensure settings picks it up
os.environ["SECRET_KEY"] = "secret-key-ci-123"

from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_session():
    """Mock de AsyncSession para testes unitários de repository.

    Retorna AsyncMock para métodos async (commit, flush, etc.)
    e MagicMock para o Result de execute(), garantindo que métodos
    sync como scalar_one_or_none() e scalars().all() funcionem.
    """
    session = AsyncMock(spec=AsyncSession)
    result = MagicMock()
    result.scalar_one_or_none = MagicMock(return_value=None)
    scalars_mock = MagicMock()
    scalars_mock.all = MagicMock(return_value=[])
    result.scalars = MagicMock(return_value=scalars_mock)
    session.execute = AsyncMock(return_value=result)
    session.add = MagicMock()
    session.add_all = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.close = AsyncMock()
    session.flush = AsyncMock()
    return session
