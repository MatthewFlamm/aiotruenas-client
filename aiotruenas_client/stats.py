from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class StatsDataMeta(ABC):
    @property
    @abstractmethod
    def end(self) -> int:
        """Type."""

    @property
    @abstractmethod
    def legend(self) -> List[str]:
        """Type."""

    @property
    @abstractmethod
    def start(self) -> int:
        """Type."""

    @property
    @abstractmethod
    def step(self) -> int:
        """Time Step."""


class StatsData(ABC):
    @property
    @abstractmethod
    def about(self) -> str:
        """Type."""

    @property
    @abstractmethod
    def data(self) -> List[List[Optional[float]]]:
        """Type."""

    @property
    @abstractmethod
    def meta(self) -> StatsDataMeta:
        """Meta Data."""


class StatsDatasetInfo(ABC):
    @property
    @abstractmethod
    def datasets(self) -> Dict[str, Any]:
        """Datasets."""

    @property
    @abstractmethod
    def last_update(self) -> int:
        """Last update time"""

    @property
    @abstractmethod
    def source(self) -> str:
        """Source."""

    @property
    @abstractmethod
    def step(self) -> int:
        """Time step."""

    @property
    @abstractmethod
    def type(self) -> str:
        """Type."""


class StatsType(ABC):
    @property
    @abstractmethod
    def dataset_info(self) -> StatsDatasetInfo:
        """Dataset info."""

    @property
    @abstractmethod
    def data(self) -> Dict[str, StatsData]:
        """Datasets."""


class StatsSource(ABC):
    @property
    @abstractmethod
    def types(self) -> Dict[str, StatsType]:
        """Types."""


class Stats(ABC):
    @property
    @abstractmethod
    def sources(self) -> Dict[str, StatsSource]:
        """Sources."""
