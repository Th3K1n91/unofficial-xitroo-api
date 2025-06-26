import base64
import requests
import os
import re
from .endpoints import *

class Mail:
    def __init__(self, mailId: str,
                 session: requests.Session = requests.Session(),
                 locale: str = 'com'):
        """
        Mail constructor.
        :param mailId: Mail id to identify mail to read.
        :param session: Optional ``requests.Session`` object.
        :param locale: Optional locale to identify mail to.
        """
        self._locale: str = locale.strip()
        self._session: requests.Session = session
        self._mailId: str = mailId.strip()

    def getBodyHtml(self) -> str:
        """
        Get body html content.
        :return: ``str``
        """
        return base64.b64decode(self.getRawMail()['bodyHtml']).decode('utf-8')

    def getBodyHtmlStrict(self) -> str:
        """
        Get strict body html content.
        :return: ``str``
        """
        return base64.b64decode(self.getRawMail()['bodyHtmlStrict']).decode('utf-8')

    def getBodyText(self) -> str:
        """
        Get text content.
        :return: ``str``
        """
        return base64.b64decode(self.getRawMail()['bodyText']).decode('utf-8')

    def getContentType(self) -> str:
        """
        Get content type.
        :return: ``str``
        """
        return self.getRawMail()['contentType']

    def getExpiration(self) -> float:
        """
        Get expiration timestamp.
        :return: :class:`float`
        """
        return self.getRawMail()['expireTimestamp']

    def getFromMail(self) -> str:
        """
        Get mail sender.
        :return: ``str``
        """
        return self.getRawMail()['from']

    def getRawHeader(self) -> str:
        """
        Get raw header content.
        :return: ``str``
        """
        return self.getRawMail()['rawHeader']

    def getArrivalTimestamp(self) -> float:
        """
        Get arrival timestamp.
        :return: ``str``
        """
        return self.getRawMail()['arrivalTimestamp']

    def compareTimeTo(self, Mailobj: __init__) -> float:
        """
        Calculates timestamp between ``self`` and ``Mailobj``.
        :param Mailobj: Another Mail object.
        :return: ``float`` value between ``self`` and ``Mailobj``.
        """
        return self.getArrivalTimestamp() - Mailobj.getArrivalTimestamp()

    def getSubject(self) -> str:
        """
        Get subject.
        :return: ``str``
        """
        return base64.b64decode(self.getRawMail()['subject']).decode('utf-8')

    def getAttachments(self) -> list:
        """
        Get attachments.
        :return: ``list``
        """
        return self.getRawMail()['attachments']

    def downloadAttachment(self, filetodownload: str, path: str = None) -> bool:
        """
        Download attachments to ``path``.
        :param filetodownload: Attachment to download.
        :param path: Path where to save the downloaded file.
        :return: ``bool`` indicating success or failure.
        """
        fpath = filetodownload if path is None else os.path.join(path, filetodownload)
        # Check for Dupe
        # if os.path.exists(fpath):
        #     return False
        params: dict[str, str] = {
            "locale": self._locale,
            "filename": filetodownload,
            "id": self._mailId,
        }
        r: requests.Response = self._session.get(ATTACHMENT, params=params)
        if r.status_code != 200:
            return False
        data = r.json()["data"]
        with open(fpath, 'wb') as f:
            f.write(base64.b64decode(data))
            f.close()
        return True

    def readAttachment(self, filetoread: str, encoding: str = 'utf-8') -> str:
        """
        Read attachment of ``filetoread`` to desired ``encoding``.
        :param filetoread: Attachment to read.
        :param encoding: Encoding to use when reading the attachment.
        :return: ``str``
        """
        params: dict[str, str] = {
            "locale": self._locale,
            "filename": filetoread,
            "id": self._mailId,
        }
        r: requests.Response = self._session.get(ATTACHMENT, params=params)
        if r.status_code != 200:
            return "Error reading attachment"
        return base64.b64decode(r.json()["data"]).decode(encoding)

    def delete(self) -> bool:
        """
        Delete Mail from inbox.
        :return: ``bool`` if successful or not.
        """
        params = {
            "locale": self._locale,
            "id": self._mailId
        }
        r: requests.Response = self._session.get(DELETE, params=params)
        if r.status_code != 200:
            return False
        return True

    def reply(self, text: str) -> bool:
        """
        Reply to Mail with html or plain text.
        :param text: Text to reply with.
        :return: ``bool`` if successful or not.
        """
        raise NotImplementedError()

    def getCode(self, codelength: int = 6) -> str:
        """
        Static Method to get code from ``mailId`` with ``codelength`` to identify the code.
        :param codelength: Optional length of code to parse. Default is 6.
        :return: Verification Code.
        """
        return re.search('\\d{' + str(codelength) + '}', self.getBodyText()).group(0)

    def getRawMail(self) -> dict:
        """
        Get raw mail content.
        :return: ``dict``
        """
        params: dict[str, str] = {
            "locale": self._locale,
            "id": self._mailId
        }
        return self._session.get(MAIL, params=params).json()

    def getIdentifier(self) -> dict[str: str | float]:
        raw = self.getRawMail()
        return {'_id': self._mailId,
                'arrivalTimestamp': raw['arrivalTimestamp'],
                'from': raw['from']}

    def getId(self) -> str:
        return self._mailId

    def __str__(self):
        return self.getBodyHtml()
