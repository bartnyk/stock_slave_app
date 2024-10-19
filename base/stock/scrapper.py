from base.scrapper import BaseScrapper
from base.stock.schemas import StockRecommendation, StockRecommendationList


class StockScrapper(BaseScrapper):
    def get_recommendations(self) -> list:
        self._get_content()
        self._create_soup()
        recommendations = self._soup.find_all("article", class_="market-news-list-row")
        recommendation_list: StockRecommendationList = StockRecommendationList()

        for rec in recommendations:
            title = rec.find("h2").get_text(strip=True)
            id = StockRecommendation.get_id(title)
            date = rec.find_previous("div", class_="market-news-list-date").get_text(
                strip=True
            )
            time = rec.find("span", class_="time").get_text(strip=True)
            instrument = (
                rec.find("div", class_="col-md-4")
                .find_next("strong")
                .get_text(strip=True)
            )
            recommendation = (
                rec.find("div", class_="col-md-4")
                .find_next("strong")
                .find_next("strong")
                .get_text(strip=True)
            )
            price = rec.find_all("strong")[2].get_text(strip=True)
            target_price = rec.find_all("strong")[3].get_text(strip=True).split(", ")
            author = (
                rec.find("div", class_="col-md-6")
                .find_next("strong")
                .get_text(strip=True)
            )

            commitment_period = rec.find_all("strong")[7].get_text()
            recommendation_object = StockRecommendation(
                **{
                    "id": id,
                    "date": date,
                    "time": time,
                    "title": title,
                    "instrument": instrument,
                    "recommendation": recommendation,
                    "price": price,
                    "target_price": target_price,
                    "author": author,
                    "commitment_period": commitment_period,
                }
            )
            recommendation_list.append(recommendation_object)

        return recommendation_list
