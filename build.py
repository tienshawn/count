import cv2
import threading
import time
import librtmp
import logging
import configargparse
logging.basicConfig(filename='delay.log', filemode='a', level=logging.INFO,
                    format='start: %(capture_time)s - success: %(success_time)s - last frame: %(last_frame)s - end: %(end_time)s - func: %(function_name)s')
# parser func


def parser_args():
    parser = configargparse.ArgParser(description="Capture delay NFV FIL HUST",
                                      formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s1", "--source_rtmp_1",
                        help="source stream 1 path")
    parser.add_argument("-name1", "--source_name_1",
                        help="source stream 1 path")
    parser.add_argument("-s2", "--source_rtmp_2",
                        help="source stream 2 path")
    parser.add_argument("-name2", "--source_name_2",
                        help="source stream 2 path")
    return parser.parse_args()


# parser init
args = parser_args()
source_rtmp_1 = args.source_rtmp_1
source_name_1 = args.source_name_1
source_rtmp_2 = args.source_rtmp_2
source_name_2 = args.source_name_2
url_1 = f'rtmp://{source_rtmp_1}/live/stream'
url_2 = f'rtmp://{source_rtmp_2}/live/stream'

def capture_streaming(name_of_fuction: str, url: str):
    count = 0
    #Create a connection
    conn = librtmp.RTMP(url, live=True)
    #Trying to connect
    conn.connect()
    print("connecting:", name_of_fuction)
    capture_time = time.monotonic()
    stream = conn.create_stream()
    print("connected:", name_of_fuction)
    success_time = time.monotonic()
    last_frame = 0
    end_time = 0
    while conn.connected:
        packet = conn.read_packet()
        if not conn.connected:
            end_time = time.monotonic()
            break
        else:
            last_frame = time.monotonic()
            continue
    print("disconnected:", name_of_fuction, ":", count)
    logging.info('', extra={'capture_time': f'{capture_time}', 'success_time': f'{success_time}',
                 'last_frame': f'{last_frame}', 'end_time': f'{end_time}', 'function_name': f'{name_of_fuction}'})


th1 = threading.Thread(target=capture_streaming, args=(
    source_name_1, url_1)).start()
th2 = threading.Thread(target=capture_streaming, args=(
    source_name_2, url_2)).start()

# def capture_streaming(name_of_fuction: str, url: str):
#     count = 0
#     print("connecting:", name_of_fuction)
#     capture_time = time.monotonic()
#     cap = cv2.VideoCapture(url)
#     print("connected:", name_of_fuction)
#     success_time = time.monotonic()
#     last_frame = 0
#     end_time = 0
#     while cap.isOpened():
#         success, image = cap.read()
#         count += 1
#         if success == False:
#             end_time = time.monotonic()
#             break
#         else:
#             last_frame = time.monotonic()
#             continue
#     print("disconnected:", name_of_fuction, ":", count)
#     logging.info('', extra={'capture_time': f'{capture_time}', 'success_time': f'{success_time}',
#                  'last_frame': f'{last_frame}', 'end_time': f'{end_time}', 'function_name': f'{name_of_fuction}'})
