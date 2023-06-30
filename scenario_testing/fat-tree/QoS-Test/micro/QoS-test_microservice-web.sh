h8 iperf -s -p 5999 -b 1M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 1M &

h7 xterm -e python3 -m http.server 80 &
h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/1 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 2M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 2M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/2 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 3M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 3M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/3 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 4M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 4M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/4 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 5M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 5M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/5 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 6M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 6M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/6 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 7M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 7M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/7 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 8M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 8M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/8 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 9M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 9M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/9 -F pcapng -a duration:45
h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob




h8 iperf -s -p 5999 -b 10M &
h6 iperf -c h8 -i 1 -t 18000 -p 5999 -b 10M &

h5 xterm -e /root/pengujian_web-FatTree.sh &

sh tshark -i s6-eth6 -i s2-eth6 -w /root/hasil_test/micro/web/10 -F pcapng -a duration:45

h6 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h8 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h6 sudo kill -9 $getjob
h8 sudo kill -9 $getjob