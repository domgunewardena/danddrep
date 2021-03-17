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

class Notification:

    def __init__(self, name, app_url):

        self.name = name
        self.app_url = app_url

    def generate_html_message(self, lines):

        message = ''

        for line in lines:
            message += '<p style="font-size:15px;">' + line + '</p> <br style=\'display:block; content:""; margin-top:10px;\'>'

        return message

    def generate_html(self, lines):

        message = self.generate_html_message(lines)

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
                <b>Hi """ + self.name + """,</b>
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
            "> """ + message + """

              <br style='
              display:block;
              content:"";
              margin-top:40px;
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

    def generate_text_message(self, lines):

        message = ''
        for line in lines:
            message += line + """

            """

        return message

    def generate_text(self, lines):

        message = self.generate_text_message(lines)

        return """
        Hi """ + self.name + """,

        """ + message + self.app_url


class ManagerNotification(Notification):

    def __init__(self, restaurant, manager, app_url):

        super().__init__(manager, app_url)

        self.restaurant = restaurant
        self.possessive = self.get_possessive()

    def get_possessive(self):

        if self.restaurant[len(self.restaurant)-1] == 's':
            return "'"
        else:
            return  "'s"



class NoteNotification(ManagerNotification):

    def __init__(self, restaurant, manager, note, app_url):

        super().__init__(restaurant, manager, app_url)

        self.note = note
        self.lines = [
            'Annabel has left you a new note on ' + self.restaurant + self.possessive + ' reviews from last week:',
            '\'' + self.note + '\'',
            "To open the app and submit your comments on last week's reviews, just click on the link below."
        ]
        self.html = self.generate_html(self.lines)
        self.text = self.generate_text(self.lines)

class NudgeNotification(ManagerNotification):

    def __init__(self, restaurant, manager, app_url):

        super().__init__(restaurant, manager, app_url)

        self.lines = [
            'Annabel has nudged you to submit ' + self.restaurant + self.possessive + ' reviews from last week.',
            "To open the app and submit your comments on last week's reviews, just click on the link below."
        ]

        self.html = self.generate_html(self.lines)
        self.text = self.generate_text(self.lines)

class SubmittedNotification(Notification):

    def __init__(self, ops_director, app_url):

        super().__init__(ops_director, app_url)

        self.lines = [
            'All the reviews from last week have now been submitted by the GMs.',
            "To open the app and review last week's submissions, just click on the link below."
        ]

        self.html = self.generate_html(self.lines)
        self.text = self.generate_text(self.lines)

class ReviewsNotification(Notification):

    def __init__(self, name, app_url):

        super().__init__(name, app_url)

        self.lines = [
            "Last week's reviews have now been collected.",
            "To open the app and see last week's reviews, just click on the link below."
        ]

        self.html = self.generate_html(self.lines)
        self.text = self.generate_text(self.lines)
