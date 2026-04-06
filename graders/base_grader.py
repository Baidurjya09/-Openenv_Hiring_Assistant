from abc import ABC, abstractmethod
from typing import List
from models.schemas import Reward


class BaseGrader(ABC):
    """Abstract base class for all graders."""

    @abstractmethod
    def grade(self, selected: List[str], correct: List[str]) -> Reward:
        """
        Grade the agent's selection against the correct answer.

        Args:
            selected: Candidate IDs chosen by the agent.
            correct: Ground-truth correct candidate IDs.

        Returns:
            Reward with a score between 0.0 and 1.0.
        """
        pass
