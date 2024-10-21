from concurrent.futures import ThreadPoolExecutor

from base import cfg
from base.stock.manager import StockManager


def fetch_recommendations(silent: bool = False):
    cfg.stock_logger.info(f"Fetch recommendations command started [silent = {silent}].")

    manager = StockManager()

    with ThreadPoolExecutor() as executor:
        future = executor.submit(manager.scrap_recommendations, silent)
    try:
        future.result(timeout=60)  # Timeout of 60 seconds
    except TimeoutError:
        manager.send_email_action_timeout()
