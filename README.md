# 功能
1)将nmap扫描的xml结果解析为csv

2)主要特点是支持对域名扫描结果的解析，使域名对应IP和端口
# 扫描结果
字段：主机名,ip,端口,状态,协议,服务,版本,操作系统类型,其他信息
# 使用方法
`
nmap -sS -O -sV -iL test.txt  -v -T4 -Pn -oX test.xml
python nmap_to_csv.py test.xml
python nmap_to_csv.py test1.xml test2.xml
`
