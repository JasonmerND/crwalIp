# 启动bolezaixian spider的一个快捷方式

from scrapy.cmdline import execute
import os
import time



if __name__ == "__main__":
    # 每天中午12半重启
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(parent_dir)
    while True:
        try:
            # commands.getstatusoutput("scrapy crawl kuaidaili")
            os.system("scrapy crawl kuaidaili --nolog")
            # execute(["scrapy", "crawl", "kuaidaili", "--nolog"])
        except Exception as e:
            pass
        time.sleep(5)
        try:
            # commands.getstatusoutput("scrapy crawl 89ip")
            os.system("scrapy crawl 89ip --nolog")
            # execute(["scrapy", "crawl", "89ip", "--nolog"])
        except Exception as e:
            pass
        time.sleep(5)
        try:
            # commands.getstatusoutput("scrapy crawl jiangxianli")
            os.system("scrapy crawl jiangxianli --nolog")
            # execute(["scrapy", "crawl", "jiangxianli", "--nolog"])
        except Exception as e:
            pass
        time.sleep(5)
        try:
            # commands.getstatusoutput("scrapy crawl xsdaili")
            os.system("scrapy crawl xsdaili --nolog")
            # execute(["scrapy", "crawl", "jiangxianli", "--nolog"])
        except Exception as e:
            pass
        print("【{}】采集IP一轮完毕，等待30分钟".format(time.strftime(
            "%Y-%m-%d %H:%M:%S")))
        time.sleep(1800)