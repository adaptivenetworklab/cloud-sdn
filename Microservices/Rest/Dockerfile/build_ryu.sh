docker image build -f middleware-left.Dockerfile -t adaptivenetlab/middleware-left:1.0 .
docker image build -f middleware-center.Dockerfile -t adaptivenetlab/middleware-center:1.0 .
docker image build -f middleware-right.Dockerfile -t adaptivenetlab/middleware-right:1.0 .
docker image build -f ryu-app-left.Dockerfile -t adaptivenetlab/ryu-app-left:1.0 .
docker image build -f ryu-app-center.Dockerfile -t adaptivenetlab/ryu-app-center:1.0 .
docker image build -f ryu-app-right.Dockerfile -t adaptivenetlab/ryu-app-right:1.0 .

