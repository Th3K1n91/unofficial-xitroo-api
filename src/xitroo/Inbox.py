import time
import requests
from .exceptions import EmailNotFound, GETRequestException
from .endpoints import *
from .Mail import Mail as Mailclass

class Inbox:
    def __init__(self, mailAddress: str = None,
                 session: requests.Session = requests.Session(),
                 inbox: dict = None,
                 locale: str = "com"):
        """
        Inbox constructor.
        :param str mailAddress: Mail address required if inbox is None
        :param Session session: Optional :class:`requests.Session`
        :param dict inbox: Optional dict of Inbox.
        :param str locale: Optional locale to use for inbox.
        """
        self._session: requests.Session = session
        self._locale: str = locale.strip()

        if mailAddress is None and inbox is None:
            raise ValueError("Either mailAddress or inbox must be specified.")

        self._mailAddress: str = mailAddress.strip() if mailAddress else None
        self._inbox: dict = inbox if inbox is not None else self.getRawInbox()

    def getRawInbox(self, mailsPerPage=25) -> dict:
        """
        Get raw Inbox.
        :param int mailsPerPage: Number of mails to fetch.
        :return: Dictionary of raw Inbox.
        :raises GETRequestException: Rate Limit/Bad Internet connection.
        """
        params: dict[str, str] = {
            "locale": self._locale,
            "mailAddress": self._mailAddress,
            "mailsPerPage": mailsPerPage,
            "minTimestamp": "0",
            "maxTimestamp": time.time()
        }
        reqeust: requests.Response = self._session.get(MAILS, params=params)
        if reqeust.status_code != 200:
            raise GETRequestException("raw Inbox", reqeust.text, reqeust.status_code)
        content: dict = reqeust.json()
        # Translate for later usage #1
        if "type" in content:
            return {'totalMails': 0, 'mails': []}
        return content

    def getTotalMails(self) -> int:
        """
        Get total number of mails.
        :return: ``int``
        """
        return len(self)

    def getRawMails(self) -> dict:
        """
        Get raw mails.
        :return: ``dict``
        """
        return self._inbox['mails']

    def getRawMail(self, index: int) -> dict:
        """
        Get raw mail by index.
        :param index: Index of mail to fetch.
        :return: ``dict``
        :raises EmailNotFound: If index is out of range.
        """
        if len(self) == 0:
            raise EmailNotFound(f"Inbox from {self._mailAddress} does not contain any mail.")
        return self._inbox['mails'][index]

    def getMail(self, index: int) -> Mailclass:
        """
        Get ``Mail`` object by index.
        :param index: Index of mail to fetch.
        :return: ``Mail``
        :raises EmailNotFound: if index is out of range
        """
        if len(self) <= index:
            raise EmailNotFound(f"Mail Index({index}) does not exists for {self._mailAddress}")
        return self[index]

    def getMailFirst(self) -> Mailclass | None:
        """
        Get first mail.
        :return: ``Mail``
        """
        if len(self) == 0:
            return None
        return self[0]

    def getMailLast(self) -> Mailclass | None:
        """
        Get last mail.
        :return: ``Mail``
        """
        if len(self) == 0:
            return None
        return self[-1]

    def __getitem__(self, item: int) -> Mailclass:
        return Mailclass(self._inbox["mails"][item]["_id"], self._session)

    def __str__(self) -> str:
        return str(self._inbox['mails'])

    def __len__(self) -> int:
        return self._inbox['totalMails']

    def __eq__(self, other) -> bool:
        return self._inbox == other._inbox