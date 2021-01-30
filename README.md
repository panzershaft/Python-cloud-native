# Python-cloud-native
Simple python flask and django pods for a k8s cluster, which can be deployed on a kuberenetes environment

## Pre-requisites 

- Need a running Docker, and Kubernetes cluster through Docker desktop app, if running on windows.
- May need to install either kind or minikube, but the docker desktop one should do just fine.
- pip install kubernetes / pip3 install kubernetes.
  
## Executing the application
- This application is in three parts
  1. Simple flask application
  2. Django flask application
  3. Python kubernetes tool (for testing your cloud-native environment)
    
### 1. EXECUTING FLASK APPLICATION
- **NOTE**: In the pod.yaml file, the image is getting pulled from a Docker Hub repo 
  ( you can build, run and push the image in your own Docker hub repo and make the necessary changes in the pod.yaml)
````
cd flask_app
kubectl apply -f pod.yaml
kubectl apply -f nodeport.yaml
kubectl get pods
kubectl get services
http://localhost:32000/
````

### 2. EXECUTING DJANGO APPLICATION
- **NOTE**: In the pod.yaml file, the image is getting pulled from a Docker Hub repo 
  ( you can build, run and push the image in your own Docker hub repo and make the necessary changes in the pod.yaml)
  
````
cd django_project
kubectl apply -f pod.yaml
kubectl apply -f nodeport.yaml
kubectl get pods
kubectl get services
http://localhost:31000/
````

### 3. EXECUTING PYTHON KUBERNETES TOOL

- Ensure you have kubernetes library of python installed: https://github.com/kubernetes-client/python

- Run the top two pods:
````
python PythonKubePodExecTool.py 
or 
python3 PythonKubePodExecTool.py
````