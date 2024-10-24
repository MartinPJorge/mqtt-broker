import pyshark
import sys
import json

# python3 correct_subscribe.py X pcap-path solution-path

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
ok_columna = respuestas['columna_dibujada'] == 'Idx'


a_subs_req = False
a_subs_ack = False
for pkt in cap:
    # Subscribe req
    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '8':
        a_subs_req = True

    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '9':
        a_subs_ack = True


print(int(ok_columna))
print(int(a_subs_req and int(respuestas['request_ack_types'][0]) == 8\
            and a_subs_ack and int(respuestas['request_ack_types'][1]) == 9 ))






