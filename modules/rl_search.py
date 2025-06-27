# modules/rl_search.py

from modules.chromadb_store import search_versions
from modules.rl_selector import RLVersionSelector
import numpy as np

def rl_weighted_search(query: str, top_k: int = 5):
    """
    Perform hybrid retrieval:
    - Start with ChromaDB semantic search
    - Re-rank based on RL feedback (if available)
    """
    rl_agent = RLVersionSelector()
    raw_results = search_versions(query, top_k=top_k * 2)  # Get extra for reranking

    scored_results = []
    for result in raw_results:
        version_id = result["id"]
        semantic_score = 1.0 - result["score"]  # Convert distance to similarity
        rl_scores = rl_agent.version_scores.get(version_id, [])
        avg_rl_score = np.mean(rl_scores) if rl_scores else 0.0

        # Hybrid scoring: weighted average (tuneable)
        combined_score = 0.6 * semantic_score + 0.4 * (avg_rl_score / 5.0)
        scored_results.append((combined_score, result))

    # Sort by combined score descending
    scored_results.sort(key=lambda x: x[0], reverse=True)

    return [r[1] for r in scored_results[:top_k]]
