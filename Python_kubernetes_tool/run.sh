cd ..
cd Django_project
kubectl apply -f pod.yaml
kubectl apply -f nodeport.yaml
cd ..
cd Flask_app
kubectl apply -f pod.yaml
kubectl apply -f nodeport.yaml
exit
