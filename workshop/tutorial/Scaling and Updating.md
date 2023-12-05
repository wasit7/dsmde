## Scaling and Updating in Kubernetes

###  Horizontal Pod Autoscaling (HPA)
Horizontal Pod Autoscaling automatically adjusts the number of pods in a deployment or replica set based on observed CPU utilization or custom metrics.

Create a simple deployment and enable autoscaling based on CPU usage.

#### 1. Create a Deployment
 
   ```yaml
   # File: my-app-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-app-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: my-app
      template:
        metadata:
          labels:
            app: my-app
        spec:
          containers:
          - name: my-app-container
            image: nginx:1.2.1
            resources:
              requests:
                memory: "64Mi"
                cpu: "250m"
              limits:
                memory: "128Mi"
                cpu: "500m"

   ```
After creating the deployment, apply the deployment
```kubectl apply -f my-app-deployment.yaml```
The resources section within the container spec defines the requested and limit resources for CPU and memory.

### 2. Create an HPA

   
   ```yaml
    # File: my-app-hpa.yaml
    apiVersion: autoscaling/v2beta2
    kind: HorizontalPodAutoscaler
    metadata:
      name: my-app-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: my-app-deployment
      minReplicas: 2
      maxReplicas: 5
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 50


   ```
After creating the hpa, apply the deployment
```kubectl apply -f my-app-hpa.yaml```

### 3  Manual Scaling
    ```kubectl scale deployment my-app-deployment --replicas=5```


### 4 Updating in Kubernetes
    
   ```yaml
   # File: my-app-deployment-update.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-app-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: my-app
      template:
        metadata:
          labels:
            app: my-app
        spec:
          containers:
          - name: my-app-container
            image: nginx:latest
            resources:
              requests:
                memory: "64Mi"
                cpu: "250m"
              limits:
                memory: "128Mi"
                cpu: "500m"

   ```

After updating the deployment, update the deployment
```kubectl apply -f my-app-deployment-update.yaml```
We update our image from ```nginx:1.2.1 -> nginx:latest```

    


