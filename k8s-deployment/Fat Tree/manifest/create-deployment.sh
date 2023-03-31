kubectl apply -f ./flowvisor-deployment.yaml
kubectl apply -f ./flowvisor-service.yaml
kubectl apply -f ./center/
kubectl apply -f ./left/
kubectl apply -f ./right/