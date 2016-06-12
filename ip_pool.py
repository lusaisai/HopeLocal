from settings import google_ips, ip_check_interval
import threading
import time
import socket
import heapq

google_ips = google_ips.split("|")
google_ips_heap = [(0, google_ips[0])]


class CheckTime(threading.Thread):
    def __init__(self, ip, target_list):
        threading.Thread.__init__(self)
        self.ip = ip
        self.target_list = target_list

    def run(self):
        try:
            socket.setdefaulttimeout(5)
            start = time.time()
            socket.create_connection((self.ip, 443))
            end = time.time()
            rtt = int((end-start)*1000)  # milliseconds
            self.target_list.append((rtt, self.ip))

        except (socket.timeout, OSError) as err:
            pass


class MaintainIPPool:
    def __init__(self):
        pass

    @staticmethod
    def build_heap():
        google_ips_with_time = []
        threads = [CheckTime(ip, google_ips_with_time) for ip in google_ips]
        for thread in threads:
            thread.start()
            time.sleep(0.1)  # Slowly starts the threads

        for thread in threads:
            thread.join()

        heapq.heapify(google_ips_with_time)
        global google_ips_heap
        google_ips_heap = google_ips_with_time

    def run(self):
        while True:
            self.build_heap()
            time.sleep(ip_check_interval)
