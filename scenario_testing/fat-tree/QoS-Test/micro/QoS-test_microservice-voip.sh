h12 iperf -s -p 5999 -b 1M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 1M &

h11 ITGRecv -l /root/hasil_test/micro/voip &
h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')

h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob


h12 iperf -s -p 5999 -b 2M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 2M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/2 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob



h12 iperf -s -p 5999 -b 3M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 3M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/3 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob



h12 iperf -s -p 5999 -b 4M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 4M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/4 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob



h12 iperf -s -p 5999 -b 5M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 5M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/5 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob



h12 iperf -s -p 5999 -b 6M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 6M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/6 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob



h12 iperf -s -p 5999 -b 7M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 7M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/7 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob




h12 iperf -s -p 5999 -b 8M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 8M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/8 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob



h12 iperf -s -p 5999 -b 9M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 9M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/9 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob




h12 iperf -s -p 5999 -b 10M &
h10 iperf -c h12 -i 1 -t 18000 -p 5999 -b 10M &


h9 ITGSend -a 10.0.0.11 -rp 10003 VoIP -x G.711.2 -h RTP -VAD

sh tshark -i s4-eth5 -w /root/hasil_test/micro/video/10 -F pcapng -a duration:60 &



h10 getjob=$(ps | grep 'iperf' | awk  '{print $1}')
h12 getjob=$(ps | grep 'iperf' | awk  '{print $1}')


h10 sudo kill -9 $getjob
h12 sudo kill -9 $getjob