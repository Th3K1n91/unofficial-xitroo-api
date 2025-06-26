from xitroo import Xitroo

Email: str = Xitroo.generate(prefix="MadeBy0x-", locale="com")
# ... some code
latestmail = Xitroo(Email).waitForLatestMail().getBodyHtml()
otp: str = Xitroo.getCode(latestmail, 6)
# ... some code to input otp
