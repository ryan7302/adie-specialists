import time

class Arachne:
    # ... other methods ...
    
    def run_tests(self):
        raise NotImplementedError("You need to implement this method")
        
    def run_tests_with_retry(self, max_attempts=3, sleep_time=5):
        for i in range(max_attempts):
            try:
                return self.run_tests()
            except Exception as e:
                if i == max_attempts - 1:
                    raise e
                else:
                    time.sleep(sleep_time)
                    
        # If the loop completes without raising an exception, it means one of the attempts succeeded
        return True