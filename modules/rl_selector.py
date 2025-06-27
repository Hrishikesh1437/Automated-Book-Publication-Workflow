# modules/rl_selector.py

import json
import os
from collections import defaultdict
import numpy as np

RL_DATA_PATH = "data/rl_feedback.json"

class RLVersionSelector:
    def __init__(self):
        self.version_scores = defaultdict(list)
        self._load()

    def _load(self):
        if os.path.exists(RL_DATA_PATH):
            with open(RL_DATA_PATH, "r", encoding="utf-8") as f:
                self.version_scores = defaultdict(list, json.load(f))

    def _save(self):
        with open(RL_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self.version_scores, f, indent=2)

    def add_feedback(self, version_id: str, reward: float):
        """
        Add a feedback score (1-5 scale typically) to a version.
        """
        self.version_scores[version_id].append(reward)
        self._save()
        print(f"✅ Feedback recorded for version {version_id}.")

    def get_top_versions(self, top_k=3):
        """
        Return top-k version IDs sorted by average reward.
        """
        if not self.version_scores:
            return []

        avg_scores = {
            vid: np.mean(scores) for vid, scores in self.version_scores.items() if scores
        }
        sorted_versions = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_versions[:top_k]

    def display_all_scores(self):
        """
        Show current average scores for all versions.
        """
        if not self.version_scores:
            print("⚠️ No feedback recorded yet.")
            return

        print("\n📊 RL Version Scores (Average Ratings):")
        for vid, scores in self.version_scores.items():
            avg = np.mean(scores)
            print(f"🆔 {vid}: {avg:.2f} ({len(scores)} ratings)")

