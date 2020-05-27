import time
import http
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from watchman_ai.stream.tools.video import Video


class Streamer:

    available_addresses = [
        ('127.0.0.1', 8080),
        ('127.0.0.2', 8081),
        ('127.0.0.3', 8082),
        ('127.0.0.4', 8083)
    ]

    def __init__(self, video_source, fps_limit, cmp_server_addr):
        assert len(Streamer.available_addresses) > 0, 'Lack of available streaming spots.'
        address = Streamer.available_addresses.pop(0)
        video = Video(video_source, fps_limit, cmp_server_addr)
        delay = 1. / fps_limit
        self.streamer = _ThreadedVideoStreamer(address, _VideoStreamer, video, delay)

    def run(self):
        self.streamer.run()


class _VideoStreamer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(http.HTTPStatus.OK)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=jpgboundary')
            self.end_headers()

            while True:
                tic = time.time()
                jpg, alarm = self.server.get_frame_info()  # TODO: handle alarm
                toc = time.time()
                t_diff = toc - tic
                if t_diff < self.server.delay:
                    t_wait = self.server.delay - t_diff
                    time.sleep(t_wait)
                jpg_bytes = jpg.tobytes()
                self.wfile.write(str.encode('\r\n--jpgboundary\r\n'))
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', str(len(jpg_bytes)))
                self.end_headers()
                jpg.save(self.wfile, 'JPEG')
            return
        else:
            self.send_response(http.HTTPStatus.NOT_FOUND)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return


class _ThreadedVideoStreamer(ThreadingMixIn, HTTPServer):

    def __init__(self, server_addr, streamer_class, video_source, delay):
        HTTPServer.__init__(self, server_addr, streamer_class)
        ThreadingMixIn.__init__(self)
        self.video = video_source
        self.delay = delay

    def get_frame_info(self):
        return self.video.get_frame_info()

    def run(self):
        self.serve_forever()
