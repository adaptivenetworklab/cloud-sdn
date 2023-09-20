docker image build -f middleware-left.Dockerfile -t adaptivenetlab/middleware-left:wnf1.0 .
docker image build -f middleware-center.Dockerfile -t adaptivenetlab/middleware-center:wnf1.0 .
docker image build -f middleware-right.Dockerfile -t adaptivenetlab/middleware-right:wnf1.0 .
docker image build -f ryu-app-left.Dockerfile -t adaptivenetlab/ryu-app-left:wnf1.0 .
docker image build -f ryu-app-center.Dockerfile -t adaptivenetlab/ryu-app-center:wnf1.0 .
docker image build -f ryu-app-right.Dockerfile -t adaptivenetlab/ryu-app-right:wnf1.0 .