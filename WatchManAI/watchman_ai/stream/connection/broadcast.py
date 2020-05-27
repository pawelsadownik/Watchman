import imagezmq
import socket


class Broadcaster:

    def __init__(self, server_addr):
        self.sender = imagezmq.ImageSender(connect_to=f'tcp://{server_addr}:5555')
        self.host_name = socket.gethostname()

    def classify_img(self, img):
        response = self.sender.send_image(self.host_name, img)
        parsed_response = self._get_parsed_response(response)
        return parsed_response

    def _get_parsed_response(self, response):
        return response
