h4 iperf -s -p 5999 -b 1M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 1M &
h8 iperf -s -p 5999 -b 1M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 1M &
h12 iperf -s -p 5999 -b 1M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 1M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-1 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/1 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115




h4 iperf -s -p 5999 -b 2M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 2M &
h8 iperf -s -p 5999 -b 2M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 2M &
h12 iperf -s -p 5999 -b 2M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 2M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-2 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/2 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115



h4 iperf -s -p 5999 -b 3M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 3M &
h8 iperf -s -p 5999 -b 3M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 3M &
h12 iperf -s -p 5999 -b 3M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 3M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-3 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/3 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115




h4 iperf -s -p 5999 -b 4M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 4M &
h8 iperf -s -p 5999 -b 4M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 4M &
h12 iperf -s -p 5999 -b 4M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 4M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-4 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/4 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115




h4 iperf -s -p 5999 -b 5M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 5M &
h8 iperf -s -p 5999 -b 5M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 5M &
h12 iperf -s -p 5999 -b 5M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 5M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-5 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/5 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115





h4 iperf -s -p 5999 -b 6M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 6M &
h8 iperf -s -p 5999 -b 6M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 6M &
h12 iperf -s -p 5999 -b 6M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 6M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-6 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/6 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115






h4 iperf -s -p 5999 -b 7M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 7M &
h8 iperf -s -p 5999 -b 7M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 7M &
h12 iperf -s -p 5999 -b 7M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 7M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-7 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/7 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115





h4 iperf -s -p 5999 -b 8M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 8M &
h8 iperf -s -p 5999 -b 8M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 8M &
h12 iperf -s -p 5999 -b 8M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 8M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-8 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/8 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115





h4 iperf -s -p 5999 -b 9M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 9M &
h8 iperf -s -p 5999 -b 9M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 9M &
h12 iperf -s -p 5999 -b 9M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 9M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-9 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/9 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115





h4 iperf -s -p 5999 -b 10M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 10M &
h8 iperf -s -p 5999 -b 10M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 10M &
h12 iperf -s -p 5999 -b 10M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 10M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

h11 ITGRecv -l /home/ubuntu/hasil_test/stress-micro-voip-10 &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD &

sh tshark -i s4-eth5  -i s6-eth6  -w /root/hasil_test/micro/stress_test/10 -F pcapng -a duration:60 &

sh sleep 120

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

sh sleep 115