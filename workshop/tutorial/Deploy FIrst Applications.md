## Deploy First Application Django

### Requirements:
### 1. Dockerized Django App:

Ensure your Django application is containerized. Create a Dockerfile that specifies how to build your Django image.
### 2. Kubernetes Cluster:

Set up a Kubernetes cluster. For this example, we'll assume you have a running Kubernetes cluster with kubectl configured.

## Steps:
### 1.  Create Docker Image:
Ensure your Django application is Dockerized. Here's a simplified Dockerfile
    
   ```Dockerfile
   # Dockerfile
   FROM python:3.8
   ENV PYTHONUNBUFFERED 1
   RUN mkdir /app
   WORKDIR /app
   COPY requirements.txt /app/
   RUN pip install -r requirements.txt
   COPY . /app/
   ```
### 2. Create Kubernetes Deployment:
        
        ```yaml
       # deployment.yaml
       apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: my-django-app
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: my-django-app
          template:
            metadata:
              labels:
                app: my-django-app
            spec:
              containers:
              - name: my-django-app
                image: your-registry/my-django-app:latest  
                ports:
                - containerPort: 8000      

        ```
Apply the deployment via ``` kubectl apply -f deployment.yaml ```

### 3. Create the Service 
        ``` yaml
        #service.yaml
        apiVersion: v1
        kind: Service
        metadata:
          name: my-django-app-service
        spec:
          selector:
            app: my-django-app
          ports:
            - protocol: TCP
              port: 80
              targetPort: 8000
          type: NodePort

        ```
Apply the deployment via ``` kubectl apply -f service.yaml ```

### 4. Check Deployment and Service:
        ```kubectl get pods ```
        ``` kubectl get services```
### 5. Access Django Application:
Once the NodePort IP is available, access your Django application in a web browser:
        ``` http://<minikube-ip>:node-port/ ```
    

        
