kubectl apply -f ./flowvisor-comnetsemu-deployment.yaml
kubectl apply -f ./flowvisor-comnetsemu-service.yaml
kubectl apply -f ./lower/
kubectl apply -f ./middle/
kubectl apply -f ./upper/