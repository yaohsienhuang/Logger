import os
import logging
from logging.handlers import TimedRotatingFileHandler

class init_logging:
    def __init__(self,logger_name,log_folder):
        
        if not os.path.isdir(log_folder):
                os.makedirs(log_folder, exist_ok=True)
        
        self.logger= logging.getLogger(__name__)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            handler = TimedRotatingFileHandler(f'{log_folder}/{logger_name}.log', when='midnight')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            handler.suffix = '%Y%m%d'
            self.logger.addHandler(handler)
            self.logger.handler_set = True

class Logger(init_logging):
    def __init__(self,logger_name,log_folder='log/'):
        super().__init__(logger_name,log_folder)
        
    def catch(self,func):
        def deli_args(*args,**kwargs):
            self.title=func.__name__
            self.logger.info('[%s] start...'%self.title)
            progress_generator=func(*args,**kwargs)
            try:
                while True:
                    msg=next(progress_generator)
                    self.pin(msg)
                    
            except StopIteration as result:
                return result.value
            
            except Exception as e:
                self.logger.warning('[%s] %s'% (self.title ,str(e)))
                
            finally:
                self.logger.info('[%s] end.'% self.title)
            
        return deli_args
    
    def pin(self,msg):
        self.logger.info('[%s] msg : %s '% (self.title,msg))
            
            
if __name__=='__main__':
    
    logger=Logger('just for test')
    
    @logger.catch
    def person_age(age):
        for i in range(age):
            if i==18:
                yield f'我正年輕, 我才 {i} 歲'
                
            elif i==30:
                yield f'我正努力賺錢, 我已經 {i} 歲'
                
            elif i==40:
                yield f'我體力大不如前, 原來我已經 {i} 歲'
                
            elif i==55:
                yield f'身體變差了, 我已經 {i} 歲, 快退休了!'
                
        return i
    
    person_age(45)