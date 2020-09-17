#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author:Chuanwei
@file:nmap_to_csv.py
@time:2019/10/06
@version:2.0
@update:2020/03/13,支持扫描ip的xml处理
"""
"""
脚本主要特点：支持对域名扫描的结果的解析，使域名对应IP和端口。
使用方法：
nmap扫描输出xml文件：nmap -sS -O -sV -iL test.txt  -v -T4 -Pn -oX test.xml
单个：python nmap_to_csv.py test.xml
批量：python nmap_to_csv.py 1.xml 2.xml 3.xml
处理结果输出为csv文件，名称和源文件名称一样。
"""
import xml.etree.ElementTree as ET
import sys


def parseNmap(filename,out_filename):
    try:
        tree=ET.parse(filename)
        root=tree.getroot()
    except Exception as e:
        print (e)
    with open(out_filename,"w") as f:
        f.write("主机名,ip,端口,状态,协议,服务,版本,操作系统类型,其他信息\n")
        for host in root.iter('host'):
            if host.find('status').get('state') == 'down':
                continue
            ip=host.find('address').get('addr',None)
            print("正在读取%s相关信息！" % ip)
            try: 
                if host.find('hostnames').find('hostname') is None:
                    hostname = ip
                else:
                    hostname = host.find('hostnames').find('hostname').get('name',None)
            except Exception as e:
                print("获取%s相关信息错误！" % ip)
                continue
            if not ip and not hostname:
                continue
            if host.find('ports').find('port') == None:
                output = hostname + "," + ip + ",,,,,,," + "\n"
                f.write(output)
            else:
                for ports in host.iter('port'): 
                    port = ports.get('portid','')
                    status = ports.find('state').get('state','')
                    protocol = ports.get('protocol','') 
                    if ports.find('service') != None:
                        service = ports.find('service').get('name','')
                        product = ports.find('service').get('product','') 
                        version = ports.find('service').get('version','')
                        ostype = ports.find('service').get('ostype','')
                        extrainfo = ports.find('service').get('extrainfo','')
                    else:
                        service=''
                        product=''
                        version=''
                        ostype=''
                        extrainfo=''
                    output = hostname + "," + ip + "," + port + "," + status + "," +  protocol + "," + service + ","+ version + ","+ ostype + ","+ extrainfo + "\n"
                    f.write(output)
    print(out_filename + "文件已生成！")

def main(args):
    for xml_file in args:
        print("处理：" + xml_file)
        out_filename = xml_file.rstrip(".xml")+ ".csv"
        parseNmap(xml_file,out_filename)

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        sys.exit("使用方法: %s 1.xml 2.xml 3.xml ...... " % __file__)
    else:
        main(sys.argv[1:])
        
