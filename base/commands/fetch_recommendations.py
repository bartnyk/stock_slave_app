from concurrent.futures import ThreadPoolExecutor, TimeoutError

from base.stock.manager import StockManager


def fetch_recommendations(silent: bool = False):
    manager = StockManager()
    manager.scrap_recommendations(silent)
    with ThreadPoolExecutor() as executor:
        future = executor.submit(manager.scrap_recommendations, silent)
    try:
        future.result(timeout=60)  # Timeout of 60 seconds
    except TimeoutError:
        manager._email_client.send_email(
            manager._email_client.create_message(
                subject="Recommendation fetching timed out",
                body="Fetching recommendations took too long.",
            )
        )
