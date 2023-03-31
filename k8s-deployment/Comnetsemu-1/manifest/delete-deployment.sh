kubectl delete -f ./flowvisor-comnetsemu-deployment.yaml
kubectl delete -f ./flowvisor-comnetsemu-service.yaml
kubectl delete -f ./lower/
kubectl delete -f ./middle/
kubectl delete -f ./upper/