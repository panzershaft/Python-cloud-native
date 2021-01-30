# Python-cloud-native
Simple python code, which can be deployed on a kuberenetes environment

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
- Go to the django_project directory: 
````buildoutcfg
cd flask_app
````

- Build the image through: 
````buildoutcfg
docker build -t hello-api .
````

- Spin up the container: 
````buildoutcfg
docker run -p 3050:3111 hello-api
````

- **NOTE**: In the pod.yaml file, the image is getting pulled from a Docker Hub repo

- Initialize pod:
````buildoutcfg
kubectl apply -f pod.yaml
````

- Initialize NodePort:
````buildoutcfg
kubectl apply -f nodeport.yaml
````

- Check your pod:
````buildoutcfg
kubectl get pods
````

- Check your service:
````buildoutcfg
kubectl get services
````

- If you pod and service is **running**, you can access you api:
``http://localhost:32000/``

### 2. EXECUTING DJANGO APPLICATION
- Go to the django_project directory: 
````buildoutcfg
cd django_project
````

- Build the image through: 
````buildoutcfg
docker build -t django-image .
````
- Run locally first: 
````buildoutcfg
docker run -p 80:8000 django-image
http://localhost/
````
- **NOTE**: In the pod.yaml file, the image is getting pulled from a Docker Hub repo

- Initialize pod:
````buildoutcfg
kubectl apply -f pod.yaml
````

- Initialize NodePort:
````buildoutcfg
kubectl apply -f nodeport.yaml
````

- Check your pod:
````buildoutcfg
kubectl get pods
````

- Check your service:
````buildoutcfg
kubectl get services
````

- If you pod and service is **running**, you can access you api:
``http://localhost:31000/``
  
### 3. EXECUTING PYTHON KUBERNETES TOOL

- Ensure you have kubernetes library of python installed: https://github.com/kubernetes-client/python

- Run the top two pods:
````buildoutcfg
python list_all_pods.py 
or 
python3 list_all_pods.py
````