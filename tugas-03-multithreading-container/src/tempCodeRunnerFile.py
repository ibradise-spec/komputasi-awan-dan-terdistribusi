 with lock:
        temp = processed_count
        time.sleep(0.001)
        processed_count = temp + 1