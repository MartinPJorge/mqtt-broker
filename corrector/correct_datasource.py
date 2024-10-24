import pyshark
import sys
import json

# python3 correct_datasource.py X pcap-path solution-path

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
broker_ip = respuestas['broker_ip']
qos_grafana = respuestas['qos_grafana']
id_grafana = respuestas['id_grafana']


ok_ip = 0
ok_qos_grafana = 0
ok_id_grafana = 0
for pkt in cap:
    # Connect command
    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '1':
        ok_ip = pkt.ip.dst == respuestas['broker_ip']
        ok_qos_grafana = respuestas['qos_grafana']\
            == int(pkt[pkt.highest_layer]._all_fields['mqtt.conflag.qos'])
        ok_id_grafana = respuestas['id_grafana']\
            == pkt[pkt.highest_layer]._all_fields['mqtt.clientid']
        break


print(int(ok_ip))
print(int(ok_qos_grafana))
print(int(ok_id_grafana))






