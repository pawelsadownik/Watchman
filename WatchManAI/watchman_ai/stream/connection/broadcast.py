import imagezmq
import socket


class Broadcaster:
    """
    Sends images to computation server and waits for its response.
    """
    def __init__(self, server_addr):
        """
        Creates Broadcaster.

        :param server_addr: ip address of computational server
        :type server_addr: str
        """
        self.sender = imagezmq.ImageSender(connect_to=f'tcp://{server_addr}:5555')
        self.host_name = socket.gethostname()

    def classify_img(self, img):
        """
        Sends image to the server, waits for answer and passes it back to the caller.

        :param img: opencv image which should be processed by computational server
        :type img: numpy.array
        :return:list of bounding boxes, where each consists of (top left x co-ordinate, top left y co-ordinate,
                bottom right x co-ordinate, bottom right y co-ordinate), and flag type (yellow or red)
        :rtype: list(list), str
        """
        response = self.sender.send_image(self.host_name, img)
        return self._get_parsed_response(response)

    def _get_parsed_response(self, response):
        return [], ''
