"""
SMS to Email Forwarder - Android App
Автоматическая пересылка SMS на email
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import smtplib
from email.mime.text import MIMEText
from jnius import autoclass

# Android классы
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class SMSForwarderApp(App):
    def build(self):
        self.processed_ids = set()
        self.running = False
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Поля настроек
        layout.add_widget(Label(text='Email отправителя (Gmail):', size_hint_y=0.1))
        self.email_input = TextInput(hint_text='your@gmail.com', size_hint_y=0.1)
        layout.add_widget(self.email_input)
        
        layout.add_widget(Label(text='Пароль приложения:', size_hint_y=0.1))
        self.password_input = TextInput(password=True, hint_text='app password', size_hint_y=0.1)
        layout.add_widget(self.password_input)
        
        layout.add_widget(Label(text='Email получателя:', size_hint_y=0.1))
        self.to_input = TextInput(hint_text='recipient@example.com', size_hint_y=0.1)
        layout.add_widget(self.to_input)
        
        # Кнопки
        self.btn = Button(text='Запустить мониторинг', size_hint_y=0.15)
        self.btn.bind(on_press=self.toggle_monitoring)
        layout.add_widget(self.btn)
        
        self.status = Label(text='Остановлено', size_hint_y=0.15)
        layout.add_widget(self.status)
        
        return layout
    
    def toggle_monitoring(self, instance):
        if not self.running:
            if not self.email_input.text or not self.password_input.text:
                self.status.text = 'Заполните все поля!'
                return
            self.running = True
            self.btn.text = 'Остановить'
            self.status.text = 'Мониторинг активен'
            Clock.schedule_interval(self.check_sms, 5)
        else:
            self.running = False
            self.btn.text = 'Запустить мониторинг'
            self.status.text = 'Остановлено'
            Clock.unschedule(self.check_sms)
    
    def check_sms(self, dt):
        try:
            Uri = autoclass('android.net.Uri')
            cursor = PythonActivity.mActivity.getContentResolver().query(
                Uri.parse('content://sms/inbox'),
                None, None, None, 'date DESC LIMIT 1'
            )
            
            if cursor and cursor.moveToFirst():
                sms_id = cursor.getInt(cursor.getColumnIndex('_id'))
                
                if sms_id not in self.processed_ids:
                    sender = cursor.getString(cursor.getColumnIndex('address'))
                    body = cursor.getString(cursor.getColumnIndex('body'))
                    timestamp = cursor.getString(cursor.getColumnIndex('date'))
                    
                    self.send_email(sender, body, timestamp)
                    self.processed_ids.add(sms_id)
                
                cursor.close()
        except Exception as e:
            self.status.text = f'Ошибка: {str(e)[:30]}'
    
    def send_email(self, sender, message, timestamp):
        try:
            msg = MIMEText(f"От: {sender}\nВремя: {timestamp}\n\n{message}", "plain", "utf-8")
            msg["Subject"] = f"SMS от {sender}"
            msg["From"] = self.email_input.text
            msg["To"] = self.to_input.text
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.email_input.text, self.password_input.text)
                server.send_message(msg)
            
            self.status.text = f'Переслано: {sender}'
        except Exception as e:
            self.status.text = f'Ошибка отправки: {str(e)[:20]}'


if __name__ == '__main__':
    SMSForwarderApp().run()
