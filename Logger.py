import os
import sys
import traceback
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
            try:
                gen=func(*args,**kwargs)
            except Exception as e:
                errMsg=self.error_message(e)
                self.logger.warning('[%s] %s'% (self.title ,str(errMsg)))
                return False,str(errMsg)
            
            try:
                while True:
                    msg=next(gen)
                    self.pin(msg)
                    
            except StopIteration as result:
                return result.value
            
            except Exception as e:
                errMsg=self.error_message(e)
                self.logger.warning('[%s] %s'% (self.title ,str(errMsg)))
                return False,str(errMsg)
                
            finally:
                self.logger.info('[%s] end.'% self.title)
            
        return deli_args
    
    def pin(self,msg):
        self.logger.info('[%s] msg : %s '% (self.title,msg))
        
    def error_message(self,e):
        error_class = e.__class__.__name__
        detail = e.args[0]
        cl, exc, tb = sys.exc_info()
        lastCallStack = traceback.extract_tb(tb)[-1]
        fileName = lastCallStack[0]
        lineNum = lastCallStack[1]
        funcName = lastCallStack[2]
        return "\"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            
            
if __name__=='__main__':
    
    logger=Logger('just for test')
    
    @logger.catch
    def person_age(age):
        for i in range(age):
            if i==18:
                yield f'????????????, ?????? {i} ???'
                
            elif i==30:
                yield f'??????????????????, ????????? {i} ???'
                
            elif i==40:
                yield f'?????????????????????, ??????????????? {i} ???'
                
            elif i==55:
                yield f'???????????????, ????????? {i} ???, ????????????!'
                
        return i
    
    person_age(45)