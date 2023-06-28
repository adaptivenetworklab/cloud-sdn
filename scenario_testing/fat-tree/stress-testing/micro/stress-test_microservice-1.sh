sh sleep 360

h4 iperf -s -p 5999 -b 1M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 1M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w hasil_tshark-1 -F pcapng &