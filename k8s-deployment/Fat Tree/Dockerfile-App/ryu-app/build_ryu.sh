docker image build -f middleware-left.Dockerfile -t adaptivenetlab/middleware-left:wf1.0 .
docker image build -f middleware-center.Dockerfile -t adaptivenetlab/middleware-center:wf1.0 .
docker image build -f middleware-right.Dockerfile -t adaptivenetlab/middleware-right:wf1.0 .
docker image build -f ryu-app-left.Dockerfile -t adaptivenetlab/ryu-app-left:wf1.0 .
docker image build -f ryu-app-center.Dockerfile -t adaptivenetlab/ryu-app-center:wf1.0 .
docker image build -f ryu-app-right.Dockerfile -t adaptivenetlab/ryu-app-right:wf1.0 .