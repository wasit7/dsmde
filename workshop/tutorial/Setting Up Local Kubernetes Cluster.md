# Setting Up the Local Cluster

Minikube is a tool that allows you to run a single-node Kubernetes cluster locally on your machine. It's a great way to get started with Kubernetes for development and testing purposes. Here's a step-by-step guide to setting up a Kubernetes cluster with Minikube




Minikube is a tool that allows you to run a single-node Kubernetes cluster locally on your machine. It's a great way to get started with Kubernetes for development and testing purposes. Here's a step-by-step guide to setting up a Kubernetes cluster with Minikube:

## Prerequisites:
### 1. Hypervisor:

Minikube supports various hypervisors like VirtualBox, HyperKit, KVM, etc. Choose and install one based on your platform.
### 2. kubectl:

Install kubectl, the Kubernetes command-line tool, on your machine.
### Steps:
### 1. Install Minikube:

Download and install Minikube from the official Minikube releases page.
For the installations -> ``` https://minikube.sigs.k8s.io/docs/start/```
### 2. Start Minikube:

Open a terminal and run the following command to start Minikube:

```minikube start --driver=<your-driver>```
Replace <your-driver> with the name of your hypervisor (e.g., virtualbox, hyperkit, kvm2).
### 3. Check Cluster Status:

Verify that Minikube and kubectl are configured correctly:

    ```kubectl cluster-info```
### 4. Access Kubernetes Dashboard (Optional):

If you want to use the Kubernetes dashboard, run the following command:

 ```minikube dashboard```
This opens the Kubernetes dashboard in your default web browser.
### 5. Deploy and Manage Applications:

You can now use kubectl to deploy and manage applications on your Minikube cluster. For example, to deploy an example application:

kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4
Check the deployment status:


        ```kubectl get deployments```
### 6. Expose the Deployment:

Expose the deployment to create a service:


        ```kubectl expose deployment hello-minikube --type=NodePort --port=8080```
### 7. Access the Service:

Get the URL to access the service:

minikube service hello-minikube
This opens the service in your default web browser.
### 8 .Stop Minikube:

When you're done, you can stop Minikube:

    ```minikube stop```
### 9. Delete Minikube Cluster:

If you want to delete the Minikube cluster entirely:

        ```minikube delete```

