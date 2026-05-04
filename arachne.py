def retry_tests(self):
        attempt = 0
        while attempt < 5:
            if self.run_tests():
                return True
            time.sleep(10)
            attempt += 1
        return False