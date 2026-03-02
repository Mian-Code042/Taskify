import multiprocessing
import os

bind = "0.0.0.0:" + os.environ.get("PORT", "10000")
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "gthread"
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
