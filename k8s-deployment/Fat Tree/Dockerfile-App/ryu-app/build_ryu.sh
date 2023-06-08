docker image build -f middleware-left.Dockerfile -t adaptivenetlab/middleware-left:sw1.0 .
docker image build -f middleware-center.Dockerfile -t adaptivenetlab/middleware-center:sw1.0 .
docker image build -f middleware-right.Dockerfile -t adaptivenetlab/middleware-right:sw1.0 .
docker image build -f ryu-app-left.Dockerfile -t adaptivenetlab/ryu-app-left:sw1.0 .
docker image build -f ryu-app-center.Dockerfile -t adaptivenetlab/ryu-app-center:sw1.0 .
docker image build -f ryu-app-right.Dockerfile -t adaptivenetlab/ryu-app-right:sw1.0 .