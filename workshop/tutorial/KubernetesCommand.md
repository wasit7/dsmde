### Kubernetes Commands

Working with Kubernetes involves using the kubectl command-line tool to interact with the cluster. Here are some commonly used kubectl commands:

## Cluster Information:
### 1. Check Cluster Info:

    ```kubectl cluster-info```
    
### 2. Display Nodes:

    ```kubectl get nodes```
### 3.Display Pods:

    ```kubectl get pods```
### 4. Display Services:

    ```kubectl get services```
## Deployment and Scaling:
### 1.Create Deployment:



        ``` kubectl create deployment <deployment-name> --image=<image>``` 
### 2. Scale Deployment:

    ```kubectl scale deployment <deployment-name> --replicas=<number>


##  Pod and Container Management:
 ### 1.Get Pod Details:

    ``` kubectl describe pod <pod-name>```
### 2. Logs from a Pod:

    ``` kubectl logs <pod-name> ```
### 3. Execute Command in Pod:

    ```kubectl exec -it <pod-name> -- <command> ```
### 4. Copy Files to/from Pod:

    ``` kubectl cp <pod-name>:/path/to/source /path/to/destination ```
## Services and Networking:
### 1.Expose Deployment as a Service:

    ``` kubectl expose deployment <deployment-name> --port=<port> --type=NodePort ```
### 2. Get Service Details:

    ``` kubectl describe service <service-name>```
### 3. Port Forwarding:

    ``` kubectl port-forward <pod-name> <local-port>:<pod-port> ``` 
### Ingress Resources:

Ingress resources define how external HTTP/S traffic should be processed. Use 
    ```kubectl get ingress ``` to view Ingress resources.
    
## Configuration and Secrets:
### 1.ConfigMaps:

    ``` kubectl get confighmap```
### 2. Secrets:

    ``` kubectl get secret```
## Namespaces
### 1.Create Namespace:
    ``` kubectl create namespace <namespace-name>``` 
### 2. Switch Namespace:

    ``` kubectl config set-context --current --namespace=<namespace-name>``` 
## Deleting Resources
### 1. Delete Deployment:

    ``` kubectl delete deployment <deployment-name>``` 
### 2. Delete Service:
    ``` kubectl delete service <service-name>``` 
### 3. Delete Pod:
    ``` kubectl delete pod <pod-name>```
### 4.Delete Namespace:
    ```kubectl delete namespace <namespace-name>``` 
## Miscellaneous:

### 1.Apply Configuration from a File:

    ``` kubectl apply -f <filename.yaml> ```