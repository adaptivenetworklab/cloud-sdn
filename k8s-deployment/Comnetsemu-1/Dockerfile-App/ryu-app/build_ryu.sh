docker image build -f middleware-upper.Dockerfile -t adaptivenetlab/middleware-upper:1.0 .
docker image build -f middleware-middle.Dockerfile -t adaptivenetlab/middleware-middle:1.0 .
docker image build -f middleware-lower.Dockerfile -t adaptivenetlab/middleware-lower:1.0 .
docker image build -f ryu-app-upper.Dockerfile -t adaptivenetlab/ryu-app-upper:1.0 .
docker image build -f ryu-app-middle.Dockerfile -t adaptivenetlab/ryu-app-middle:1.0 .
docker image build -f ryu-app-lower.Dockerfile -t adaptivenetlab/ryu-app-lower:1.0 .

