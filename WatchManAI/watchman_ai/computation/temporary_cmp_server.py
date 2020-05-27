import imagezmq
import cv2


image_hub = imagezmq.ImageHub()
while True:
    host_name, img = image_hub.recv_image()
    cv2.imshow(host_name, img)
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')
