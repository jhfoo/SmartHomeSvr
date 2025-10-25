# core
import threading

devices = {}
devices_lock = threading.Semaphore()