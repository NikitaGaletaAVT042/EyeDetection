from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from plyer import camera

import cv2
import numpy as np

KV = '''
BoxLayout:
    orientation: 'vertical'

    Image:
        id: camera_image
        size_hint_y: 7

    MDRaisedButton:
        text: 'Start'
        on_press: app.start_detection()

    MDRaisedButton:
        text: 'Stop'
        on_press: app.stop_detection()
'''

class EyeDetectionApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.layout = self.root
        self.camera_image = self.layout.ids.camera_image

        # Запуск обновления изображения
        Clock.schedule_interval(self.update_image, 1.0 / 30.0)

        # Переменная для хранения состояния поиска глаз
        self.detecting_eyes = False

    def update_image(self, dt):
        if self.detecting_eyes:
            # Получение кадра с камеры
            frame = self.get_frame_from_camera()

            # Преобразование кадра в текстуру Kivy
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr'
            )
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camera_image.texture = image_texture

    def get_frame_from_camera(self):
        # Получение кадра с камеры с помощью plyer.camera
        frame = camera.take_picture()

        # Ваш код обработки кадра
        return frame

    def start_detection(self):
        self.detecting_eyes = True
        toast("Eye detection started.")

    def stop_detection(self):
        self.detecting_eyes = False
        toast("Eye detection stopped.")

if __name__ == '__main__':
    EyeDetectionApp().run()
