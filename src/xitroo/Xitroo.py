import random
import re
import string
import time
import requests
from .endpoints import *
from .exceptions import *
from .Mail import Mail as Mailclass
from .Inbox import Inbox as Inboxclass
from .Captcha import Captcha as Captchaclass
from .Search import SearchMail as Searchclass
from collections.abc import MutableMapping

class Xitroo:
    def __init__(self, mailAddress: str, header: MutableMapping[str, str | bytes] = {}, session: requests.Session = None):
        """
        ``Xitroo`` API constructor.
        :param mailAddress: Mail address to check for or send mails, e.g. "test123@xitro.com".
        :param header: Optional headers to send with request.
        :param session: Optional ``requests.Session`` object.
        :raises InvalidLocale: Raised if chosen locale is invalid.
        """
        self._l: list[str] = ["de", "fr", "com"]
        self._locale: str = mailAddress.strip().split(".")[-1]
        self._header: MutableMapping[str, str | bytes] = header
        self._mailAddress: str = mailAddress.strip()
        self._session: requests.Session = requests.Session() if session is None else session

        if self._locale not in self._l:
            raise InvalidLocale("Error Locale: mailAddress must end with any locale from list: " + ", ".join(self._l) + " (Choosen: " + mailAddress.split('.')[-1] + ")")

        if len(self._header) != 0:
            self._session.headers.update(self._header)

    def getMailAddress(self) -> str:
        """
        Returns the mail address of the current ``Xitroo`` object.
        :return: ``str``
        """
        return self._mailAddress

    def setMailAddress(self, mailAddress: str) -> None:
        """
        :param mailAddress: Sets the mail address to your given argument.
        """
        mailAddress: str = mailAddress.strip()
        self._locale: str = mailAddress.split(".")[-1]
        self._mailAddress: str = mailAddress

    def getHeader(self) -> MutableMapping[str, str | bytes]:
        """
        Returns the header of the current ``requests.Session`` instance.
        :return: collections.abc.MutableMapping[str, str | bytes]
        """
        return self._header

    def setHeader(self, header: MutableMapping[str, str | bytes]) -> None:
        """
        :param header: Sets the header of the current ``requests.Session`` instance.
        :type header: collections.abc.MutableMapping[str, str | bytes]
        """
        self._header: MutableMapping[str, str | bytes] = header
        self._session.headers.update(self._header)

    def getSession(self) -> requests.Session:
        """
        Returns the ``requests.Session`` instance.
        :return: ``requests.Session``
        """
        return self._session

    def setSession(self, session: requests.Session) -> None:
        """
        :param session: Sets the ``requests.Session`` instance.
        """
        self._session: requests.Session = session
        self._header: MutableMapping[str, str | bytes] = self._session.headers

    def Mail(self, mailId: str) -> Mailclass:
        """
        Create Mail Object to read mail.
        :param mailId: Identifier to read mail from.
        :return: ``Mail`` Object.
        """
        return Mailclass(mailId, self._session, self._locale)

    def Inbox(self, inbox: dict = None) -> Inboxclass:
        """
        Create Inbox Object to read Inbox.
        :param inbox: Optional Inbox dict if there is one. Should look like this {'totalMails': 0, 'mails': []}.
        :return: ``Inbox`` Object
        """
        return Inboxclass(self._mailAddress, self._session, inbox, self._locale)

    def Captcha(self) -> Captchaclass:
        """
        Create Captcha Object to get or verify captcha.
        :return: ``Captcha`` Object
        """
        return Captchaclass(self._session, self._locale)

    # Rewrite Search
    def searchInbox(self) -> Searchclass:
        """
        Create Search Object to search Inbox.
        :return: ``Search`` Object
        """
        return Searchclass(self._mailAddress, self._session)

    def getRawInbox(self, mailsPerPage=25) -> dict:
        """
        Read current Inbox to dict.
        :param mailsPerPage: Optional Number of mails to read from Inbox.
        :return: ``dict`` of Inbox.
        """
        return self.Inbox().getRawInbox(mailsPerPage)

    def getRawMail(self, mailId: str) -> dict:
        """
        Read Mail from mailId to dict.
        :param mailId: Identifier to read mail from.
        :return: ``dict`` of Mail.
        """
        return self.Mail(mailId).getRawMail()

    def _verifyCaptchaAsUserInput(self) -> str:
        captchaid: str = ""
        solution: str = ""
        r = {"authSuccess": False}
        while not r["authSuccess"]:
            reload: bool = True
            params: dict[str, str] = {"locale": self._locale}
            while reload:
                r: dict = self._session.get(GETCAPTCHA, headers=self._header, params=params).json()
                captchaid: str = r["authID"]
                captcha: str = r["captchaCode"]
                print(captcha)
                solution: str = input("Solve Captcha (r for reload, e for exit): ")
                if solution != "r":
                    reload = False
                if solution == "e":
                    return ""
            params.update({
                "authID": captchaid,
                "captchaSolution": solution
            })
            r: dict = self._session.get(SENDCAPTCHA, headers=self._header, params=params).json()
            if not r["authSuccess"]:
                print("Captcha failed")
        return captchaid

    def sendMail(self, recipient: str, subject: str, Text: str, mode: int = 1, id: str = "") -> bool:
        """
        Send Mail as mailaddress in constructor to ``recipient`` with given ``subject`` and ``Text``.
        :param recipient: Recipient email address.
        :param subject: Subject to send with.
        :param Text: Text to send.
        :param mode: Optional send mode. - **1**: manual userinput to get captcha id; **0**: no userinput, but requires captcha id. Create captcha id with ``Xitroo.Captcha`` :class:`Captchaclass`.
        :param id: Optional captcha id which is required to send mail if mode 0 is selected.
        :return: ``bool`` - True if sent successfully, false otherwise.
        """
        if mode:
            id: str = self._verifyCaptchaAsUserInput()
        params: dict[str, str] = {"locale": self._locale}
        if not id:
            return False
        data: dict[str, str] = {
            "authID": id,
            "bodyText": Text,
            "from": self._mailAddress,
            "recipient": recipient,
            "replyMailID": "",
            "subject": subject
        }
        r: requests.Response = self._session.post(SENDMAIL, headers=self._header, params=params, data=data)
        if r.status_code != 200:
            return False
        return True

    @staticmethod
    def generate(prefix: str = "", suffix: str = "", locale: str = "de", randomletterscount: int = 10) -> str:
        """
        Static Method to Generate random email String of given ``length``, ``prefix``, ``suffix`` and ``locale``.
        :param prefix: Optional prefix to generate email String.
        :param suffix: Optional suffix to generate email String.
        :param locale: Optional locale to generate domain of email string. [de, fr, com] only are **supported**.
        :param randomletterscount: Optional number of random letters to generate into email String.
        :return: Email ``str``.
        """
        return prefix + "".join(random.choices(string.ascii_letters, k=randomletterscount)) + suffix + "@xitroo." + locale

    @staticmethod
    def getCode(body: str, codelength: int = 6) -> str:
        """
        Static Method to get code from given ``body`` and ``codelength`` to identify the code.
        :param body: Bodytext of email.
        :param codelength: Optional length of code to parse. Default = 6.
        :return: Verification Code.
        """
        return re.search('\\d{' + str(codelength) + '}', body).group(0)

    def getLatestMail(self) -> Mailclass | None:
        """
        Get latest Mail from mailaddress.
        :return: ``Mail`` Object of latest Mail or ``None`` if no latest Mail is found.
        """
        return self.Inbox().getMailFirst()

    def waitForLatestMail(self, maxTime=60, sleepTime=5, checkMail=100) -> Mailclass | None:
        """
        Wait until latest Mail.
        :param maxTime: Optional maximum time of the difference between current time and latest Mail received mail time to get only new mail.
        :param sleepTime: Optional sleep time in seconds between checking latest mail.
        :param checkMail: Optional Interval to check if latest Mail is found.
        :return: ``Mail`` Object of latest Mail.
        """
        for i in range(checkMail):
            latest = self.getLatestMail()
            if latest:
                if not(latest.getRawMail()["arrivalTimestamp"] + maxTime < time.time()):
                    return latest
            #print("Waiting for latest mail...")
            time.sleep(sleepTime)

    def __getitem__(self, item: int) -> Mailclass:
        return self.Inbox()[item]

    def __len__(self) -> int:
        return len(self.Inbox())

    def __str__(self) -> str:
        return str(self.getRawInbox())

    def __eq__(self, other) -> bool:
        return self._mailAddress == other._mailAddress
