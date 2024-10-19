from pydantic import BaseModel


class EmailHost(BaseModel):
    mail: str
    password: str
    smtp: str
    pop3: str
    imap: str
    port: int
