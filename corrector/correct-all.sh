#!/bin/bash

# ./correct-all.sh path-to-entregas-dir

entregas=$1 # path to DIR with ONLY ZIPs of entregas

# Create CSV with corrections
echo "student,grupo,ack_tcp_dst_port,broker_ip,qos_grafana,id_grafana,columna_dibujada,request_ack_types,campo_json,pub_x,pub_xm5,total" > notas.csv


# Put there just the files avoiding folder recursion
mkdir /tmp/clean-entregas

for entrega in `ls $entregas`; do
    # UNZIP submited LAB
    out_zip=/tmp/${entrega::-4}
    unzip $entregas/$entrega -d $out_zip 

    # Create correction DIR
    clean_out=/tmp/clean-entregas/${entrega::-4}
    mkdir $clean_out

    # Copy the JSONs, PCAPNG and LOGs
    for ext in `echo json pcapng log jpeg png`; do
        for file in `find $out_zip -name *$ext`; do
            # Get filename: https://stackoverflow.com/a/32372307
            fname=`echo "$file" | sed "s/.*\///"`
            cp $file $clean_out/$fname
        done
    done

    # Copy the vitals signs dataset
    cp Human_vital_signs_R.csv $clean_out
done



# Correct each submission, one by one
for submission in `ls /tmp/clean-entregas`; do
    X=${submission:6:10} # get group number X
    group_dir="/tmp/clean-entregas/"$submission

    total=0

    # Print name
    echo ============
    echo = GRUPO $X =
    echo ============

    # Correct the connect
    connect=`python3 correct_connect.py $X "$group_dir"/publish-broker-grupo$X.pcapng $group_dir`
    echo -e "\tack_tcp_dst_port: $connect"
    total=$(( total + connect ))

    # Correct the datasource setup
    datasource=`python3 correct_datasource.py $X "$group_dir"/connect-data-source-grupo$X.pcapng $group_dir`
    i=0
    datas_all=""
    questions=( "broker_ip" "qos_grafana" "id_grafana" )
    for datasi in `echo $datasource`; do
        echo -e "\t${questions[i]}: $datasi"
        datas_all=$datas_all"$datasi,"
        i=$(( i + 1 ))
        total=$(( total + datasi ))
    done

    # Correct dashboard creation/subscription
    sub=`python3 correct_subscribe.py $X "$group_dir"/data-source-subscribe-grupo$X.pcapng $group_dir "$group_dir"/sub-grupo$X.log`
    i=0
    sub_all=""
    questions=( "columna_dibujada" "request_ack_types" )
    for subi in `echo $sub`; do
        echo -e "\t${questions[i]}: $subi"
        sub_all=$sub_all"$subi,"
        i=$(( i + 1 ))
        total=$(( total + subi ))
    done

    # JSON publication
    pub=`python3 correct_publish_json.py $X "$group_dir"/publish-json-grupo$X.pcapng $group_dir`
    pub_all=""
    questions=( "campo_json" "pub_x" "pub_xm5" )
    i=0
    for pubi in `echo $pub`; do
        echo -e "\t${questions[i]}: $pubi"
        pub_all=$pub_all"$pubi,"
        i=$(( i + 1 ))
        total=$(( total + pubi ))
    done

    # Serie temporal
    serie=0
    for f in `ls "$group_dir"/serie-temporal*`; do
        serie=1
    done
    total=$(( total + serie ))


    # Output final mark
    for student in `grep alumna $group_dir/respuestas-$X.json | cut -d'"' -f4 | sed 's/ /_/g'`; do
        echo $student,$X,$connect,$datas_all$sub_all$pub_all$serie,$total >> notas.csv
    done
done


