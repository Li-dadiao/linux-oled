import oled as OLED
import socket

from datetime import datetime
from datetime import timedelta
def get_host_ip():  # 获取 本地 IP
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
  finally:
    s.close()
  return ip

def __main__():
    OLED.Init()
    OLED.Clear()
    ip = get_host_ip()  # 获取本地 IP
    curr_time=datetime.now() # 现在的时间
    today=(curr_time.strftime("%Y-%m-%d"))# 调用strftime方法就是对时间进行格式化
    today = "DATE:" + today
    OLED.ShowString(22,0,"S805-Linux",16,1)
    OLED.ShowString(0,16,ip,16,1) #显示 本地 ip
    OLED.ShowString(0,16*2,today,16,1)
    OLED.ShowString(0,16*3,"Good Good Study",16,1)
    OLED.Refresh()
__main__()