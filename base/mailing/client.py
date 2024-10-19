import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from base import cfg
from base.mailing.schemas import EmailHost
from base.stock.schemas import StockRecommendation


class EmailClient:
    def __init__(self) -> None:
        self.host = EmailHost(**cfg.email)
        self.receiver = cfg.EMAIL_RECIPIENT

    def send_email(self, message: str) -> None:
        with SMTP_SSL(
            self.host.smtp, self.host.port, context=self._ssl_context, timeout=10
        ) as server:
            server.login(self.host.mail, self.host.password)
            server.sendmail(
                self.host.mail,
                self.receiver,
                msg=message,
            )
            server.quit()

    @property
    def _ssl_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def create_message(self, subject: str, body: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.host.mail
        msg["To"] = self.receiver
        msg["Subject"] = subject
        body = body.encode("utf-8")
        msg.attach(MIMEText(body, "plain", "utf-8"))
        return msg.as_string()

    def create_stock_recommendation_body(
        self, recommendation: StockRecommendation
    ) -> str:
        return f"""
        Rekomendowany instrument: {recommendation.instrument}
        Rekomendacja: {recommendation.recommendation}
        Rekomendowana cena rynkowa: {recommendation.price}
        Cena docelowa: {" lub ".join(recommendation.target_price)}
        Okres obowiązywania: {recommendation.commitment_period}
        Data publikacji: {recommendation.full_datetime}
        """
