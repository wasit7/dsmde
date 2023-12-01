## Helm Package Managment For Kubernetes
### 1. Helms
Helm is a package manager for Kubernetes applications. It simplifies deploying and managing applications in Kubernetes.
Helm is a way to define, install, and upgrade Kubernetes applications.

### 2. Helm Components
2.1 **Charts** : Helm packages are called charts. A chart is a collection of files that describe a set of Kubernetes resources.
    
2.2 **Release**: A specific instance of a chart running in a Kubernetes cluster.

    
### 3. Install Helm
Link -> https://helm.sh/docs/intro/install/

After installation, verify the installation with ```helm version ```


### 4. Create the Helm Chart
#### 4.1 Create a Helm Chart
Use the helm create command to generate a basic chart template.

``` helm create mychart```


#### 4.2 Chart Structure
Explore the structure of the chart, including the `Chart.yaml` file, `values.yaml`, and the `templates` directory.
```
    mychart/
    |-- .helmignore        # Specifies files to be ignored by Helm
    |-- Chart.yaml         # Metadata about the chart
    |-- values.yaml        # Default configuration values for the chart
    |-- charts/            # Directory for subcharts (dependencies)
    |-- templates/         # Kubernetes resource templates
    |   |-- deployment.yaml
    |   |-- service.yaml
    |-- charts/            # Directory containing dependent charts
    |-- templates/         # Directory containing template files
    |-- charts/            # Directory containing subcharts (if any)
    |-- templates/         # Directory containing template files for subcharts
    |-- .helmignore        # File specifying patterns to ignore when packaging


```
**.helmignore**: This file specifies patterns that Helm should ignore when packaging the chart. It's similar to .gitignore in a Git repository.

**Chart.yaml**: This file contains metadata about the chart, including the name, version, description, and other information.

**values.yaml**: This file defines the default configuration values for the chart. Users can override these values during installation or upgrade.

**charts**: This directory is used for storing subcharts, which are dependencies required by the main chart.

**templates/**: This directory contains Kubernetes resource template files. These files are typically written in YAML and define the desired state of Kubernetes objects like deployments, services, configmaps, etc.



#### 4.3 Templates and Values
 The `values.yaml` can be overridden during installation with desired values.
 The `templates` directory  defines Kubernetes resources.

### 5. Install and Manage Helm Charts
#### 5.1 To deploy a chart, 
use  ```helm install myrelease ./mychart```
#### 5.2 Upgrade a Release
```helm upgrade myrelease ./mychart```
#### 5.3 List and Delete Releases
To list the releases -> ```helm list``` <br>
To uninstall the release -> ```helm uninstall myrelease```

### 6.  Explore Helm Hub
Link -> https://artifacthub.io/
#### 6.1 Helm Dependencies 
Helm chart can depend on the other charts<br>

To build the dependency<br>
``` helm dependency buid [CHART]```

To update the dependency<br>
``` helm dependency update [CHART]```

### 7. Helm Templating 
Link -> https://helm.sh/docs/chart_template_guide

### 8. Other Useful command
When we want to add the repository, use <br>
``` helm repo add [NAME] [URL]``` <br>

To update the repo <br>
```helm repo update``` <br>

To show the values in the chart <br>
```helm show values [CHART]``` <br>












