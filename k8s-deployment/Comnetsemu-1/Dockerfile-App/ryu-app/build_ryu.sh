docker image build -f middleware-upper.Dockerfile -t adaptivenetlab/middleware-upper:2.0 .
docker image build -f middleware-middle.Dockerfile -t adaptivenetlab/middleware-middle:2.0 .
docker image build -f middleware-lower.Dockerfile -t adaptivenetlab/middleware-lower:2.0 .
docker image build -f ryu-app-upper.Dockerfile -t adaptivenetlab/ryu-app-upper:2.0 .
docker image build -f ryu-app-middle.Dockerfile -t adaptivenetlab/ryu-app-middle:2.0 .
docker image build -f ryu-app-lower.Dockerfile -t adaptivenetlab/ryu-app-lower:2.0 .

