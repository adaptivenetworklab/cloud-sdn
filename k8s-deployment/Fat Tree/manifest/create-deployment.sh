kubectl apply -f ./flowvisor-comnetsemu-deployment.yaml
kubectl apply -f ./flowvisor-comnetsemu-service.yaml
kubectl apply -f ./center/
kubectl apply -f ./left/
kubectl apply -f ./right/