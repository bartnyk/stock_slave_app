from datetime import datetime

from pymongo import DESCENDING

from base import cfg
from base.mailing.client import EmailClient
from base.stock.repository import StockRepository
from base.stock.schemas import StockRecommendation, StockRecommendationList
from base.stock.scrapper import StockScrapper

logger = cfg.logger.stock


class StockManager:
    def __init__(self):
        self._repository = StockRepository("recommendation")
        self._email_client = EmailClient()

        recommendations_url = cfg.STOCK_RECOMMENDATIONS_URL
        self._scrapper = StockScrapper(recommendations_url)

    def _recommendation_exists(self, recommendation_id: str) -> bool:
        return bool(self._repository.get({"id": recommendation_id}))

    def scrap_recommendations(self, silent: bool = False) -> None:
        any_new = False
        recommendations: StockRecommendationList = self._scrapper.get_recommendations()

        for recommendation in recommendations:
            if self._recommendation_exists(recommendation.id):
                continue

            logger.info(f"New recommendation found: {recommendation.title}")
            self._repository.insert(recommendation.model_dump())
            any_new = True
            if not silent:
                self._send_email_with_recommendation(recommendation)

        if not any_new:
            logger.info("No new recommendations found.")

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
        recommendations = self._repository.get_all().sort("title", DESCENDING)
        return StockRecommendationList.parse(recommendations)

    def send_email_action_timeout(self) -> None:
        msg = f"Recommendation fetching timed out [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
        logger.error(msg)
        self._email_client.send_email(
            self._email_client.create_message(
                subject=msg,
                body="Fetching recommendations took too long.",
            )
        )
