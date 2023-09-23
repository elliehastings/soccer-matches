from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

from app.models.match_recommendations import MatchRecommendation
from app.models.teams import Team


class ScoreTypeEnum(str, Enum):
    closeness_score = 'closeness_score'
    quality_score = 'quality_score'


class SortOrderEnum(str, Enum):
    asc = 'asc'
    desc = 'desc'


def filter_match_recommendations(
        recs: list[MatchRecommendation],
        score_type: ScoreTypeEnum,
        date_range: tuple[date, date],
        **kwargs,
) -> list[MatchRecommendation]:
    reverse_sort = False
    if "sort_order" in kwargs:
        if kwargs["sort_order"] == SortOrderEnum.desc:
            reverse_sort = True

    filtered_recs = [
        rec for rec in recs if rec.starts_at > date_range[0] and rec.starts_at < date_range[1]]

    filtered_recs.sort(key=lambda r: getattr(
        r, score_type), reverse=reverse_sort)

    limit = len(filtered_recs)
    if "limit" in kwargs:
        if limit != 0:
            limit = kwargs["limit"]

    return filtered_recs[:limit]
