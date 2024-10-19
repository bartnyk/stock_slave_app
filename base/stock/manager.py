from datetime import datetime

from base import cfg
from base.mailing.client import EmailClient
from base.stock.repository import StockRepository
from base.stock.schemas import StockRecommendation, StockRecommendationList
from base.stock.scrapper import StockScrapper


class StockManager:
    def __init__(self):
        self._repository = StockRepository("recommendation")
        self._email_client = EmailClient()

        recommendations_url = cfg.STOCK_RECOMMENDATIONS_URL
        self._scrapper = StockScrapper(recommendations_url)

    def _recommendation_exists(self, recommendation_id: str) -> bool:
        return bool(self._repository.get({"id": recommendation_id}))

    def scrap_recommendations(self, silent: bool = False) -> None:
        recommendations: StockRecommendationList = self._scrapper.get_recommendations()

        for recommendation in recommendations:
            if self._recommendation_exists(recommendation.id):
                continue

            self._repository.insert(recommendation.model_dump())

            if not silent:
                self._send_email_with_recommendation(recommendation)

    def _send_email_with_recommendation(
        self, recommendation: StockRecommendation
    ) -> None:
        mail_content = self._email_client.create_stock_recommendation_body(
            recommendation
        )
        message = self._email_client.create_message(
            subject=recommendation.title, body=mail_content
        )
        self._email_client.send_email(message)

    def get_saved_recommendations(self) -> StockRecommendationList:
        recommendations = self._repository.get_all()
        return StockRecommendationList.parse(recommendations)

    def send_email_action_timeout(self) -> None:
        self._email_client.send_email(
            self._email_client.create_message(
                subject=f"Recommendation fetching timed out [{datetime.now().strftime('%Y-%m-%d %H:%M')}]",
                body="Fetching recommendations took too long.",
            )
        )
