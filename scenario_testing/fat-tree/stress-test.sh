# SLICE & SERVICE TEST FATTREE

# Video Streaming
h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout="#rtp{dst=10.0.0.1, port=5004, mux=ts}" --ttl 12 &

#Background Traffic (Sementara)
h4 iperf -s -p 5999 &
h2 iperf -c h4 -i 1 -t 1000000 -p 5999 &

#Web Service
h7 python3 -m http.server 80 &
h5 /root/pengujian_web-FatTree.sh &

#Background Traffic (Sementara)
h8 iperf -s -p 5999 &
h6 iperf -c h8 -i 1 -t 1000000 -p 5999 &

# VOIP
h11 ITGRecv -l recieve-h9-to-h11 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

#Background Traffic (Sementara)
h12 iperf -s -p 5999 &
h10 iperf -c h12 -i 1 -t 1000000 -p 5999 &