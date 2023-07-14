h4 iperf -s -p 5999 -b 15M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 15M &
h8 iperf -s -p 5999 -b 15M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 15M &
h12 iperf -s -p 5999 -b 15M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 15M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-15 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/15 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 80




h4 iperf -s -p 5999 -b 20M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 20M &
h8 iperf -s -p 5999 -b 20M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 20M &
h12 iperf -s -p 5999 -b 20M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 20M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-20 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/20 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60



h4 iperf -s -p 5999 -b 25M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 25M &
h8 iperf -s -p 5999 -b 25M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 25M &
h12 iperf -s -p 5999 -b 25M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 25M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-25 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/25 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60




h4 iperf -s -p 5999 -b 30M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 30M &
h8 iperf -s -p 5999 -b 30M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 30M &
h12 iperf -s -p 5999 -b 30M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 30M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-30 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/30 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60




h4 iperf -s -p 5999 -b 35M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 35M &
h8 iperf -s -p 5999 -b 35M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 35M &
h12 iperf -s -p 5999 -b 35M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 35M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-35 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/35 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60





h4 iperf -s -p 5999 -b 40M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 40M &
h8 iperf -s -p 5999 -b 40M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 40M &
h12 iperf -s -p 5999 -b 40M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 40M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-40 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/40 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60






h4 iperf -s -p 5999 -b 45M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 45M &
h8 iperf -s -p 5999 -b 45M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 45M &
h12 iperf -s -p 5999 -b 45M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 45M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-45 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/45 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60





h4 iperf -s -p 5999 -b 50M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 50M &
h8 iperf -s -p 5999 -b 50M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 50M &
h12 iperf -s -p 5999 -b 50M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 50M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-50 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/50 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60





h4 iperf -s -p 5999 -b 55M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 55M &
h8 iperf -s -p 5999 -b 55M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 55M &
h12 iperf -s -p 5999 -b 55M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 55M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-55 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/55 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60





h4 iperf -s -p 5999 -b 60M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 60M &
h8 iperf -s -p 5999 -b 60M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 60M &
h12 iperf -s -p 5999 -b 60M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 60M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/QoS-mono-voip-60 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5 -i s6-eth6  -w /root/hasil_test/mono/QoS_test/60 -F pcapng -a duration:60 &

sh sleep 105

h1 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h1 getps=$(ps aux | grep 'ubuntu vlc -q' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps | grep 'sudo' | sed -n 1p | awk  '{print $1}')
h3 getps=$(ps aux | grep 'ubuntu vlc rtp' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h1 sudo kill -9 $getps
h3 sudo kill -9 $getps
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob

h7 getjob=$(ps | grep 'xterm' | awk  '{print $1}')
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h7 sudo kill -9 $getjob
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob

h11 getjob=$(ps | grep 'ITGRecv' | awk  '{print $1}')
h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h11 sudo kill -9 $getjob
h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob

sh sleep 60