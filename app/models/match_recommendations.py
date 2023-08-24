from typing import Optional

from app.models.matches import Match


class MatchRecommendation(Match):
    closeness_value: float
    quality_value: float
    closeness_score: Optional[int] = None
    quality_score: Optional[int] = None
