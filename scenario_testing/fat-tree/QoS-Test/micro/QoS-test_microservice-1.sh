sh sleep 360



h4 iperf -s -p 5999 -b 1M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 1M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/1 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob




h4 iperf -s -p 5999 -b 2M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 2M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/2 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob



h4 iperf -s -p 5999 -b 3M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 3M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/3 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob



h4 iperf -s -p 5999 -b 4M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 4M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/4 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob



h4 iperf -s -p 5999 -b 5M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 5M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/5 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob



h4 iperf -s -p 5999 -b 6M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 6M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/6 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob



h4 iperf -s -p 5999 -b 7M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 7M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/7 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob




h4 iperf -s -p 5999 -b 8M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 8M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/8 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob



h4 iperf -s -p 5999 -b 9M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 9M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/9 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob




h4 iperf -s -p 5999 -b 10M &
h2 iperf -c h4 -i 1 -t 18000 -p 5999 -b 10M &

h1 sudo -u ubuntu vlc rtp://@:5004 &
h3 sudo -u ubuntu vlc -q /home/ubuntu/cloud-sdn/scenario_testing/test_services/video.mp4 --sout='#rtp{dst=10.0.0.1, port=5004, mux=ts}' --ttl 12 --no-sout-all --sout-keep &

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/10 -F pcapng -a duration:60 &

h1 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h3 getjob=$(ps aux | grep 'ubuntu vlc' | sed -n 1p | awk  '{print $2}')
h2 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h4 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h1 sudo kill -9 $getjob
h3 sudo kill -9 $getjob
h2 sudo kill -9 $getjob
h4 sudo kill -9 $getjob