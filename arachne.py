def validate_config(self):
    if 'daemon_interval' not in self.config or (isinstance(self.config['daemon_interval'], int) and self.config['daemon_interval'] > 0):
        return False
    
    if ('test_command' not in self.config or not isinstance(self.config['test_command'], str)) or \
       ('retries' not in self.config or not isinstance(self.config['retries'], int) or self.config['retries'] < 1):
        return False
    
    if 'retries' in self.config and (not isinstance(self.config['test_command'], str) or len(self.config['test_command'].strip()) == 0):
        return False
        
    if 'test_command' in self.config and (not isinstance(self.config['retries'], int) or not 1 <= self.config['retries'] <= 10):
        return False
    
    return True