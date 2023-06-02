sh sleep 10

h4 ITGRecv -l ~/Hasil_Pengambilan_Data/Fat-Tree/BGT/mono/recieve-h2-to-h4_50 &
h2 ITGSend -T TCP -a 10.0.0.4 -c 50000 -C 1000 -t 35000 &

h8 ITGRecv -l ~/Hasil_Pengambilan_Data/Fat-Tree/BGT/mono/recieve-h6-to-h8_50 &
h6 ITGSend -T TCP -a 10.0.0.8 -c 50000 -C 1000 -t 35000 &

h12 ITGRecv -l ~/Hasil_Pengambilan_Data/Fat-Tree/BGT/mono/recieve-h10-to-h12_50 &
h10 ITGSend -T TCP -a 10.0.0.12 -c 50000 -C 1000 -t 35000 &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout="#rtp{dst=10.0.0.1, port=5004, mux=ts}" --ttl 12 --no-sout-all --sout-keep &

h7 python3 -m http.server 80 &
h5 /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l recieve-h9-to-h11 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6 -i s8-eth6 | tee hasil_tshark &
