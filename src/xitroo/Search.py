import requests
from datetime import datetime
from .Inbox import Inbox as Inboxclass
from enum import Enum

class SearchMail:
    # {'totalMails': 0, 'mails': []}
    def __init__(self, mailAddress: str, session: requests.Session = requests.Session()):
        """
        SearchMail constructor.
        :param mailAddress: Email address to search Inbox from.
        :param session: ``requests.Session`` to use.
        """
        class BY(Enum):
            DATE = self._byDate
            SENDER = self._bySender
            TITLE = self._byTitle
            TEXT = self._byTextInBody

        self._mailAddress: str = mailAddress.strip()
        self._session: requests.Session = session
        self._inbox: Inboxclass = Inboxclass(self._mailAddress, self._session)
        self._mails: dict = self._inbox.getRawInbox()
        self._result: dict = {'totalMails': 0, 'mails': []}
        self.BY = BY

    def _byDate(self, mailDate: datetime) -> Inboxclass:
        """
        Search Mail by date.
        :param mailDate: mail date as **%Y-%m-%d**.
        :type mailDate: ``str``
        :return: ``Inbox``
        """
        for i in self._inbox:
            if datetime.fromtimestamp(i.getArrivalTimestamp()).date() == mailDate.date():
                self._result['totalMails'] += 1
                self._result['mails'].append(i.getIdentifier())
        return Inboxclass(inbox=self._result, session=self._session)

    def _bySender(self, sender: str) -> Inboxclass:
        """
        Search Mail by sender.
        :param sender: sender as string.
        :return: ``Inbox``
        """
        for i in self._inbox:
            if sender in i.getFromMail():
                self._result['totalMails'] += 1
                self._result['mails'].append(i.getIdentifier())
        return Inboxclass(inbox=self._result, session=self._session)

    def _byTitle(self, title: str) -> Inboxclass:
        """
        Search Mail by title.
        :param title: title as string.
        :return: ``Inbox``
        """
        for i in self._inbox:
            if title in i.getSubject():
                self._result['totalMails'] += 1
                self._result['mails'].append(i.getIdentifier())
        return Inboxclass(inbox=self._result, session=self._session)

    def _byTextInBody(self, text: str) -> Inboxclass:
        """
        Search Mail by text in body.
        :param text: text as string.
        :return: ``Inbox``
        """
        for i in self._inbox:
            if text in str(i):
                self._result['totalMails'] += 1
                self._result['mails'].append(i.getIdentifier())
        return Inboxclass(inbox=self._result, session=self._session)

    # def searchInboxRegex(self):
    #     # {'totalMails': 0, 'mails': []}
    #     class SearchRe:
    #         def __init__(self, xitroo: Xitroo):
    #
    #         def byDate(self, regex: str):
    #                 if re.search(regex, datetime.fromtimestamp(i['arrivalTimestamp']).strftime('%Y-%m-%d')):
    #
    #         def bySender(self, regex: str):
    #                 if re.search(regex, self._xitroo.Mail(id).getFromMail()):
    #
    #         def byTitle(self, regex: str):
    #                 if re.search(regex, self._xitroo.Mail(id).getSubject()):
    #
    #         def byTextInBody(self, regex: str):
    #                 if re.search(regex, self._xitroo.Mail(id).getBodyText()):
    #     return SearchRe(self)
