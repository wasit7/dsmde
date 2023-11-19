### Section 3: Kubernetes Commands

#### Objective
This section aims to equip participants with the skills to efficiently use `kubectl`, the command-line interface for interacting with Kubernetes clusters. Understanding `kubectl` is essential for deploying, managing, and troubleshooting Kubernetes resources.

#### Background Knowledge
Participants should be familiar with basic command-line interface operations and have a rudimentary understanding of Kubernetes' architecture and its components, such as pods, deployments, and services. This foundational knowledge is crucial for understanding the context and implications of the commands executed using `kubectl`.

#### Theories
`kubectl` is the Swiss Army knife of Kubernetes, offering a wide array of functionalities through various commands and flags. It allows users to deploy applications, inspect and manage cluster resources, and view logs. Key concepts include:

- **Kubernetes API:** `kubectl` interacts with the Kubernetes API server to manage the resources within a Kubernetes cluster. Understanding the API resource types is fundamental to using `kubectl` effectively.
- **Resource Management:** Kubernetes treats almost everything as a resource (e.g., pods, services, deployments). `kubectl` commands are used to create, view, modify, and delete these resources.
- **Imperative vs. Declarative Commands:** `kubectl` supports both imperative commands (e.g., `kubectl create`) and declarative commands using YAML files (e.g., `kubectl apply`).
- **Namespaces:** Kubernetes uses namespaces to organize resources into non-overlapping groups. `kubectl` commands can be scoped to specific namespaces.
- **Labels and Selectors:** Labels are key/value pairs attached to resources. `kubectl` can use selectors to perform actions on a specific set of resources.

#### Example Code
1. **Viewing Resources:**
    ```bash
    kubectl get pods                   # List all pods in the default namespace
    kubectl get pods -n mynamespace    # List pods in a specific namespace
    kubectl get pod mypod -o yaml      # Get detailed information about a specific pod in YAML format
    ```

2. **Creating and Managing Resources:**
    ```bash
    kubectl create -f my-deployment.yaml   # Create resources defined in a YAML file
    kubectl apply -f my-deployment.yaml    # Apply a configuration to a resource from a YAML file
    kubectl delete pod mypod               # Delete a specific pod
    ```

3. **Debugging and Diagnostics:**
    ```bash
    kubectl logs mypod                        # Fetch logs of a pod
    kubectl describe pod mypod                # Show detailed information about a pod
    kubectl exec -it mypod -- /bin/bash       # Execute an interactive bash shell on the pod
    ```

#### Expected Results
By the end of this section, participants will have a solid grasp of:

- Basic and advanced `kubectl` commands and their uses.
- How to interact with the Kubernetes API to manage resources.
- Techniques for inspecting, troubleshooting, and managing Kubernetes resources effectively.
- Understanding of how to apply changes to the cluster and roll out updates to applications.

This knowledge is fundamental for anyone working with Kubernetes, as it forms the basis of day-to-day operations in managing Kubernetes clusters and applications. Participants will gain confidence in using `kubectl` to control every aspect of their Kubernetes environment.