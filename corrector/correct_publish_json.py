import pyshark
import sys
import json

# python3 correct_publish_json.py X pcap-path solution-path

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


check_X = X % 10
check_Xm5 = (X+5) % 10

ok_X = False
ok_Xm5 = False
PUB_counter = 0
for pkt in cap:
    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '3':

        
        if check_X in [PUB_counter, PUB_counter+1]:
            ok_X = int(pkt[pkt.highest_layer]._all_fields['mqtt.len'])\
                == int(respuestas['pub_x']) or ok_X

        if check_Xm5 in [PUB_counter, PUB_counter+1]:
            ok_Xm5 = int(pkt[pkt.highest_layer]._all_fields['mqtt.len'])\
                == int(respuestas['pub_xm5']) or ok_Xm5


        PUB_counter += 1


print(int(respuestas['campo_json'] in ['Message', 'message']))
print(int(ok_X))
print(int(ok_Xm5))






