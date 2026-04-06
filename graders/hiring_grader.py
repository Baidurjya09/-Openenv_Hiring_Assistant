from typing import List
from graders.base_grader import BaseGrader
from models.schemas import Reward


class HiringGrader(BaseGrader):
    """
    Deterministic grader for the hiring environment.

    Scoring logic:
      - Precision  = correct_selections / len(selected)   (penalizes false positives)
      - Recall     = correct_selections / len(correct)    (penalizes missed candidates)
      - Score      = F1 = 2 * precision * recall / (precision + recall)
      - Edge cases: empty selection → 0.0, no correct candidates → 1.0 if nothing selected
    """

    def grade(self, selected: List[str], correct: List[str]) -> Reward:
        correct_set = set(correct)
        selected_set = set(selected)

        # Edge case: no correct answers defined
        if not correct_set:
            score = 1.0 if not selected_set else 0.0
            return Reward(
                score=score,
                correct_selections=0,
                total_correct=0,
                false_positives=len(selected_set),
                feedback="No correct candidates defined for this task.",
            )

        # Edge case: agent selected nothing
        if not selected_set:
            return Reward(
                score=0.0,
                correct_selections=0,
                total_correct=len(correct_set),
                false_positives=0,
                feedback="No candidates were selected. Score is 0.",
            )

        true_positives = len(selected_set & correct_set)
        false_positives = len(selected_set - correct_set)

        precision = true_positives / len(selected_set)
        recall = true_positives / len(correct_set)

        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)

        score = round(f1, 4)

        if score == 1.0:
            feedback = "Perfect selection. All correct candidates identified with no false positives."
        elif true_positives == len(correct_set):
            feedback = f"All correct candidates found but {false_positives} false positive(s) included."
        elif false_positives == 0:
            feedback = f"No false positives but missed {len(correct_set) - true_positives} correct candidate(s)."
        else:
            feedback = (
                f"Partial match: {true_positives}/{len(correct_set)} correct, "
                f"{false_positives} false positive(s)."
            )

        return Reward(
            score=score,
            correct_selections=true_positives,
            total_correct=len(correct_set),
            false_positives=false_positives,
            feedback=feedback,
        )
