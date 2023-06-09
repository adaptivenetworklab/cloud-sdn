sh sleep 20

h4 iperf -s -p 5999 -b 2500K &
h2 iperf -c h4 -i 1 -t 1000000 -p 5999 -b 1500K &

h8 iperf -s -p 5999 -b 2500K &
h6 iperf -c h8 -i 1 -t 1000000 -p 5999 -b 2500K &

h12 iperf -s -p 5999 -b 1500K &
h10 iperf -c h12 -i 1 -t 1000000 -p 5999 -b 1500K &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout "#rtp{dst=10.0.0.1, port=5004, mux=ts}" --ttl 12 --no-sout-all --sout-keep &

h7 python3 -m http.server 80 &
h5 /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l recieve-h9-to-h11 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6 -i s8-eth6 | tee hasil_tshark &