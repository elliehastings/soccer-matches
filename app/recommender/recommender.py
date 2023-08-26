from typing import Literal

from fastapi import HTTPException, status as httpstatus

from app.models.matches import Match
from app.models.match_recommendations import MatchRecommendation


class Recommender:
    def __init__(self) -> None:
        pass

    def recommend(self, matches: list[Match]) -> list[MatchRecommendation]:
        return []

    def calculate_score_values(self, matches: list[Match]) -> list[MatchRecommendation]:
        match_recommendations = []

        for match in matches:
            if match.away_team.points is None or match.home_team.points is None:
                # TODO: Might be nice to log warnings and filter these teams out instead,
                # Or return an additional list of teams without sufficient data
                raise HTTPException(
                    status_code=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Teams without points present"
                )

            closeness_value = abs(
                match.away_team.points - match.home_team.points)
            quality_value = (match.away_team.points +
                             match.home_team.points) / 2

            match_recommendations.append(
                MatchRecommendation(
                    **dict(match),
                    closeness_value=closeness_value,
                    quality_value=quality_value
                )
            )

        return match_recommendations

    def calculate_scores(self, matches: list[MatchRecommendation]) -> list[MatchRecommendation]:
        matches_sorted_on_closeness = sorted(
            matches, key=lambda m: m.closeness_value)
        for idx, match in enumerate(matches_sorted_on_closeness):
            match.closeness_score = idx + 1

        matches_sorted_on_quality = sorted(
            matches_sorted_on_closeness, key=lambda m: m.quality_value, reverse=True)
        for idx, match in enumerate(matches_sorted_on_quality):
            match.quality_score = idx + 1

        return matches_sorted_on_quality

# TODO: AI implementation
# TODO: Identical method signatures may not work because AI responses will be unstructured


class AIRecommender(Recommender):
    def __init__(self) -> None:
        super().__init__()

    def recommend(self, matches: list[Match]):
        return super().recommend(matches)


class ManualRecommender(Recommender):
    def __init__(self) -> None:
        super().__init__()

    def recommend(self, matches: list[Match]) -> list[MatchRecommendation]:
        scored_matches = self.calculate_score_values(matches)
        recommendations = self.calculate_scores(scored_matches)

        return recommendations


class RecommenderFactory:
    @classmethod
    def create_recommender(cls, type: Literal['MANUAL', 'AI']) -> Recommender:
        RECOMMENDER_TYPE_MAPPING = {
            'MANUAL': ManualRecommender,
            'AI': AIRecommender
        }
        return RECOMMENDER_TYPE_MAPPING[type]()
