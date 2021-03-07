import sys
import os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from config import COOKIE, OS_COOKIE
import genshin_helper as gih


def run():
    #os_rewards = gih.Hoyolab(OS_COOKIE).get_rewards()
    #print(os_rewards)
    #info_list = gih.Hoyolab(OS_COOKIE).get_info()
    #print(info)
    #d = gih.MHYLab(OS_COOKIE).data_handler()
    #a = gih.Hoyolab(OS_COOKIE).run(d)
    
    #rewards = gih.Mihoyo(COOKIE).get_rewards()
    #print(rewards)
    #r = gih.MHYBbs('COOKIE').get_roles()
    r = {'data': None, 'message': '登录失效，请重新登录', 'retcode': -100}
    d = gih.MHYBbs(COOKIE).data_handler()
    
    #d = gih.MHYBbs('COOKIE')
    
    print(d)


if __name__ == '__main__':
    run()

