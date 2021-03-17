import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class AppEmail:

    def __init__(self, subject, recipient, html, text):

        self.sender = 'D&D Rep'
        self.recipient = recipient
        self.subject = subject
        self.html = html
        self.text = text

    def send(self):

        # msg = EmailMultiAlternatives(self.subject, self.text, self.sender, [self.recipient])
        # msg.attach_alternative(self.html, 'text/html')
        # msg.send()

        sender_email = "domgunewardenadev@gmail.com"
        receiver_email = self.recipient
        password = os.environ.get('EMAIL_PASSWORD')

        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.sender
        message["To"] = self.recipient

        part1 = MIMEText(self.text, "plain")
        part2 = MIMEText(self.html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email,
                receiver_email,
                message.as_string()
            )

class NoteNotification:

    def __init__(self, restaurant, manager, note, app_url):

        self.restaurant = restaurant
        self.manager = manager
        self.note = note
        self.app_url = app_url

        self.possessive = self.get_possessive()
        self.html = self.generate_html()
        self.text = self.generate_text()

    def get_possessive(self):

        if self.restaurant[len(self.restaurant)-1] == 's':
            return "'"
        else:
            return  "'s"


    def generate_html(self):

        return """
        <html>
          <body>
          <div class="container"
          style="
          background-color:#f2f2f2;
          ">

            <div class="container"
            style="
            background-color:#3480eb;
            padding: 20px;
            padding-left:60px;
            margin: 0 auto;
            width:80%;
            font-family:Arial;
            ">
              <p style="
              font-size:20px;
              font-family:Helvetica;
              color:white;
              ">
                <b>Hi """ + self.manager + """,</b>
              </p>
            </div>

            <div class="container"
            style="
            background-color:white;
            padding: 20px;
            padding-left:60px;
            margin: 0 auto;
            width:80%;
            font-family:Arial;
            ">
              <p style="font-size:15px;">
                Annabel has left you a new note on """ + self.restaurant + self.possessive + """ reviews from last week:
              </p>

              <br style='
              display:block;
              content:"";
              margin-top:10px;
              '>

              <p style="font-size:15px;">
                '""" + self.note + """'
              </p>

              <br style='
              display:block;
              content:"";
              margin-top:10px;
              '>

              <p style="font-size:15px;">
                To open the app and submit your comments on last week's reviews, just click on the button below
              </p>

              <br style='
              display:block;
              content:"";
              margin-top:50px;
              '>

              <button
              style="
              background-color:green;
              padding:10px 20px 10px 20px;
              font-size:20px;
              color:white;
              ">
              <a
              href='""" + self.app_url + """'
              style="
              color:white;
              text-decoration:none;
              "
              >D&D Rep</a></button>

            </div>

          </div>

          </body>
        </html>
        """

    def generate_text(self):

        return """
        Hi """ + self.manager + """,

        Annabel has left a new note on """ + self.restaurant + self.possessive + """ reviews from last week:

        '""" + self.note + """'

        To submit your comments on last week's reviews, visit the app:

        """ + self.app_url
