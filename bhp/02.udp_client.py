# -*- coding:utf-8 -*-
import socket as s

target_host = "127.0.0.1"
target_port = 80

client = s.socket(s.AF_INET, s.SOCK_DGRAM)

client.sendto("AAABBBCC", (target_host, target_port))

data, addr = client.recvfrom(4096)

print data
