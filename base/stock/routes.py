from flask import Blueprint
from flask_login import login_required

from base.stock.manager import StockManager
from base.stock.schemas import StockRecommendationList

manager = StockManager()

blueprint = Blueprint("stock", __name__, url_prefix="/stock")


@blueprint.route("/list", methods=["GET"])
@login_required
def list():
    recommendations: StockRecommendationList = manager.get_saved_recommendations()
    return recommendations.model_dump_json(exclude={"id"})
