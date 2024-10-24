import pyshark
import sys
import json

# python3 correct_connect.py X pcap-path solution-path

X = int(sys.argv[1])
pcap_path = sys.argv[2]

# Open saved trace file 
cap = pyshark.FileCapture(pcap_path)

# Open solution file
solution_path = sys.argv[3]
respuestas_json = f'{solution_path}/respuestas-{X}.json'
with open(respuestas_json) as f:
    respuestas = json.load(f)


# Student Answer
answer_tcp_dst_port = respuestas['ack_tcp_dst_port']


ok = 0
for pkt in cap:
    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '2':
        ok = int(pkt.tcp.dstport) == int(answer_tcp_dst_port)
        break


print(int(ok))






