### Kubernetes Demo Project Along with Helm

To build a simple django applications along with the helm chart. We need to create a simple django applications
Here is the demo link for the applications 
    https://gitlab.com/kyawsoebtr/infra_demo_docs/-/tree/development?ref_type=heads


### Dockerizations
After getting simple django applications, we need to containerize with the Docker as below

 
   ```Dockerfile
   # Dockerfile
        FROM python:3.8-slim
        RUN apt-get update --fix-missing
        
        RUN apt install -y git netcat-traditional
        
        WORKDIR /backend
        ADD ./requirements.txt requirements.txt
        RUN pip install -r requirements.txt
        ADD . /backend/
        WORKDIR /backend
   ```
After containerization, need to push to the container registry.

### Creating the Helm Chart
So Lets create the helm project for the sample django applications <br>
 ``` helm create demo-infra```


```
    demo-infra/
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

In the directory of the **templates**, we create a sample folder called **backend** which will include our deployment, service, ingress, service, job etc........

Demo Link -> https://gitlab.com/kyawsoebtr/infra_demo_docs/-/tree/development/kubernetes/helm/demo-infra?ref_type=heads <br>

### Adding the Dependencies
Before doing anything, lets add the postgres dependency in the **Chart.yaml** .
```yml
    apiVersion: v2
    name: demo-infra
    description: A Helm chart for Kubernetes
    
  
    type: application
    
   
    version: 0.1.0
   
    appVersion: "1.16.0"
    
    
    dependencies: 
      - name: postgresql
        version: ">=8.0.0"
        repository: https://charts.bitnami.com/bitnami
        condition: postgresql.enabled
  
```

After adding the dependencies, we need to build the dependency.

The command is -> ``` helm dependency build .``` where . is the helm chart directoy <br>

### Creating the Deployment
After building the dependencies, go the **backend** directory, we can create our deployment for the django applications with new file **deployment.yml**.

```yml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: {{ include "demo-infra.fullname" . }}-backend
      labels:
        service.type: backend
        {{- include "demo-infra.labels" . | nindent 4 }}
    spec:
      {{- if not .Values.autoscaling.enabled }}
      replicas: {{ .Values.replicaCount }}
      {{- end }}
      selector:
        matchLabels:
          service.type: backend
    
          {{- include "demo-infra.selectorLabels" . | nindent 6 }}
      template:
        metadata:
          {{- with .Values.podAnnotations }}
          annotations:
            {{- toYaml . | nindent 8 }}
          {{- end }}
          labels:
            service.type: backend
            {{- include "demo-infra.selectorLabels" . | nindent 8 }}
        spec:
          {{- with .Values.imagePullSecrets }}
          imagePullSecrets:
            {{- toYaml . | nindent 8 }}
          {{- end }}
         
         
            # serviceAccountName: {{ include "demo-infra.serviceAccountName" . }}
          securityContext:
            {{- toYaml .Values.podSecurityContext | nindent 8 }}
          
          initContainers:
            - name: wait-for-db
              image: "{{ include "common.images.image" (dict "imageRoot" .Values.postgresql.image "global" .Values.global) }}"
              imagePullPolicy: "{{ .Values.postgresql.image.pullPolicy }}"
              command:
                - /bin/bash
                - -ec
                - |
                  #!/bin/bash
                  set -o errexit
                  set -o nounset
                  set -o pipefail
                  . /opt/bitnami/scripts/libos.sh
                  . /opt/bitnami/scripts/liblog.sh
                  . /opt/bitnami/scripts/libpostgresql.sh
                  check_postgresql_connection() {
                      echo "SELECT 1" | postgresql_remote_execute "$POSTGRESQL_CLIENT_DATABASE_HOST" "$POSTGRESQL_CLIENT_DATABASE_PORT_NUMBER" "$POSTGRESQL_CLIENT_DATABASE_NAME" "$POSTGRESQL_CLIENT_POSTGRES_USER" "$POSTGRESQL_CLIENT_CREATE_DATABASE_PASSWORD"
                  }
                  info "Connecting to the PostgreSQL instance $POSTGRESQL_CLIENT_DATABASE_HOST:$POSTGRESQL_CLIENT_DATABASE_PORT_NUMBER"
                  if ! retry_while "check_postgresql_connection"; then
                      error "Could not connect to the database server"
                      return 1
                  else
                      info "Connected to the PostgreSQL instance"
                  fi
              env:
              - name: POSTGRESQL_CLIENT_DATABASE_HOST
                value: "{{ .Release.Name }}-postgresql" # db service
              - name: POSTGRESQL_CLIENT_DATABASE_PORT_NUMBER
                value: "5432"
              - name: POSTGRESQL_CLIENT_DATABASE_NAME
                value: "{{ .Values.postgresql.auth.database }}"
              - name: POSTGRESQL_CLIENT_POSTGRES_USER
                value: "{{ .Values.postgresql.auth.username }}"
              - name: POSTGRESQL_CLIENT_CREATE_DATABASE_PASSWORD
                valueFrom:
                  secretKeyRef:
                    name: {{ .Release.Name}}-postgresql
                    key: password
         
          containers:
              
            - name: {{ .Chart.Name }}
              securityContext:
                {{- toYaml .Values.securityContext | nindent 12 }}
              image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag | default .Chart.AppVersion }}"
              imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
              command:
                - sh
                - runserver.sh
              ports:
                - name: http
                  containerPort: 8000
                  protocol: TCP
    
              envFrom:
                - configMapRef:
                    name: {{ include "demo-infra.fullname" . }}-backend-configmap
                    optional: false
              env:
                - name: DB_HOST
                  value: "{{ .Release.Name}}-postgresql" #db service
                - name: POSTGRES_DB
                  value: {{.Values.postgresql.auth.database}}
                - name: DB_PORT
                  value: "5432"
                - name: POSTGRES_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: {{ .Release.Name}}-postgresql
                      key:  password
                - name: POSTGRES_USER
                  value: {{.Values.postgresql.auth.username}}
             
                #cross-origin
                - name: CSRF_TRUSTED_ORIGINS
                  value: "http://{{ index .Values.ingress.backend.hosts 0 "host" }}"
              
             
    
              {{- if .Values.enableProbes }}
              readinessProbe:
                httpGet:
                  path: /admin
                  port: http
              livenessProbe:
                httpGet:
                  path: /admin
                  port: http
              {{- end }}
              
              
              
          {{- with .Values.nodeSelector }}
          nodeSelector:
            {{- toYaml . | nindent 8 }}
          {{- end }}
          {{- with .Values.affinity }}
          affinity:
            {{- toYaml . | nindent 8 }}
          {{- end }}
          {{- with .Values.tolerations }}
          tolerations:
            {{- toYaml . | nindent 8 }}
          {{- end }}

```
###  Creating the Service
For service,
```yml
    apiVersion: v1
    kind: Service
    metadata:
      name: {{ include "demo-infra.fullname" . }}-service
      labels:
        service.type: backend
        {{- include "demo-infra.labels" . | nindent 4 }}
    spec:
      type: {{ .Values.backend.service.type }}
      ports:
        - port: {{ .Values.backend.service.port }}
          targetPort: http
          protocol: TCP
          name: http
      selector:
        service.type: backend
        {{- include "demo-infra.selectorLabels" . | nindent 4 }}

```
### Creating the Ingress
For ingress,

```yml
    {{- if .Values.ingress.enabled -}}
    {{- $fullName := include "demo-infra.fullname" . -}}
    {{- $svcPort := .Values.backend.service.port -}}
    {{- if and .Values.ingress.className (not (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion)) }}
      {{- if not (hasKey .Values.ingress.annotations "kubernetes.io/ingress.class") }}
      {{- $_ := set .Values.ingress.annotations "kubernetes.io/ingress.class" .Values.ingress.className}}
      {{- end }}
    {{- end }}
    {{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
    apiVersion: networking.k8s.io/v1
    {{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
    apiVersion: networking.k8s.io/v1beta1
    {{- else -}}
    apiVersion: extensions/v1beta1
    {{- end }}
    kind: Ingress
    metadata:
      name: {{ $fullName }}
      labels:
        service.type: backend
        {{- include "demo-infra.labels" . | nindent 4 }}
      {{- with .Values.ingress.annotations }}
      annotations:
        {{- toYaml . | nindent 4 }}
      {{- end }}
    spec:
      {{- if and .Values.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
      ingressClassName: {{ .Values.ingress.className }}
      {{- end }}
      {{- if .Values.ingress.tls }}
      tls:
        {{- range .Values.ingress.tls }}
        - hosts:
            {{- range .hosts }}
            - {{ printf "%s-%s" "api" . | quote }} 
            {{- end }}
          secretName: {{ .secretName }}
        {{- end }}
      {{- end }}
      rules:
        {{- range .Values.ingress.backend.hosts }}
        - host:  {{ printf "%s" .host | quote }} 
          http:
            paths:
              {{- range .paths }}
              - path: {{ .path }}
                {{- if and .pathType (semverCompare ">=1.18-0" $.Capabilities.KubeVersion.GitVersion) }}
                pathType: {{ .pathType }}
                {{- end }}
                backend:
                  {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
                  service:
                    name: {{ $fullName }}-service
                    port:
                      number: {{ $svcPort }}
                  {{- else }}
                  serviceName: {{ $fullName }}-service
                  servicePort: {{ $svcPort }}
                  {{- end }}
              {{- end }}
        {{- end }}
    {{- end }}
```
### Creating the HPA,
Fro HPA,

```yml
    {{- if .Values.autoscaling.enabled }}
    apiVersion: autoscaling/v2beta1
    kind: HorizontalPodAutoscaler
    metadata:
      name: {{ include "demo-infra.fullname" . }}
      labels:
        service.type: backend
        {{- include "demo-infra.labels" . | nindent 4 }}
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: {{ include "demo-infra.fullname" . }}-backend
      minReplicas: {{ .Values.autoscaling.minReplicas }}
      maxReplicas: {{ .Values.autoscaling.maxReplicas }}
      metrics:
        {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
        - type: Resource
          resource:
            name: cpu
            targetAverageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
        {{- end }}
        {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
        - type: Resource
          resource:
            name: memory
            targetAverageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
        {{- end }}
    {{- end }}


```
### Creating the Job
For Job,

```yml
    
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: {{ include "demo-infra.fullname" . }}-django-migrations
      labels:
        {{- include "demo-infra.labels" . | nindent 4 }}
      annotations:
        helm.sh/hook: post-install,post-upgrade
    spec:
      template:
        spec:
          {{- with .Values.imagePullSecrets }}
          imagePullSecrets:
            {{- toYaml . | nindent 8 }}
          {{- end }}
          initContainers:
            - name: wait-for-postgresql
              image: busybox
              command: ["sh", "-c", "until nc -zv {{ .Release.Name }}-postgresql 5432; do sleep 1; done"]
           
          containers:
            - name: {{ include "demo-infra.fullname" . }}-django-migrations
              image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag | default .Chart.AppVersion }}"
              imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
              command: 
                - "/bin/sh"
                - "-c"
                - |
                  python manage.py makemigrations
                  python manage.py migrate
              envFrom:
                - configMapRef:
                    name: {{ include "demo-infra.fullname" . }}-backend-configmap
                    optional: false
              env:
                - name: DB_HOST
                  value: "{{ .Release.Name}}-postgresql" #db service
                - name: POSTGRES_DB
                  value: {{.Values.postgresql.auth.database}}
                - name: DB_PORT
                  value: "5432"
                - name: POSTGRES_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: {{ .Release.Name}}-postgresql
                      key:  password
                - name: POSTGRES_USER
                  value: {{.Values.postgresql.auth.username}}
                
          restartPolicy: Never


```
### Modifying the values.yml

The key point in here is that We can modify the desired values in the **values.yml** file for making changes on the every componets like services, deployment. For examples, we can change our image, tag, postgres version, and the ingress name that we want to setup etc...

And the **values.yml** file look like below

```yml
    
           # Default values for streamlit.
        # This is a YAML-formatted file.
        # Declare variables to be passed into your templates.
        
        global:
          storageClass: local-path
          
        replicaCount: 1
        
        imagePullSecrets:
          - name: gitlab
        nameOverride: ""
        fullnameOverride: "demo-infra"
        
        serviceAccount:
          # Specifies whether a service account should be created
          create: true
          # Annotations to add to the service account
          annotations: {}
          # The name of the service account to use.
          # If not set and create is true, a name is generated using the fullname template
          name: ""
        
        podAnnotations: {}
        
        podSecurityContext: {}
          # fsGroup: 2000
        
        securityContext: {}
          # capabilities:
          #   drop:
          #   - ALL
          # readOnlyRootFilesystem: true
          # runAsNonRoot: true
          # runAsUser: 1000
        
        
        
        ingress:
          enabled: true
          # className: "nginx"
          annotations: {}
            # kubernetes.io/ingress.class: nginx
            # kubernetes.io/tls-acme: "true"
          #........Frontend Host................#######
          
          backend:
            hosts:
              - host: demo-infra.samu.local
                paths:
                  - path: /
                    pathType: ImplementationSpecific
          tls: []
          #  - secretName: chart-example-tls
          #    hosts:
          #      - chart-example.local
        
        # We usually recommend not to specify default resources and to leave this as a conscious
          # choice for the user. This also increases chances charts run on environments with little
          # resources, such as Minikube. If you do want to specify resources, uncomment the following
          # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
          
        resources:
          limits:
            cpu: 300m
            memory: 384Mi
          requests:
            cpu: 300m
            memory: 384Mi
        
        autoscaling:
          enabled: false
          minReplicas: 1
          maxReplicas: 100
          targetCPUUtilizationPercentage: 80
          # targetMemoryUtilizationPercentage: 80
        
        nodeSelector: {}
        
        tolerations: []
        
        affinity: {}
        
        nginx:
          image:
            repository: nginx
            tag: latest
            pullPolicy: IfNotPresent
          service:
            type: LoadBalancer
            port: 8089
          
        enableProbes: true
        
        backend:
          image:
            repository: registry.gitlab.com/kyawsoebtr/infra_demo_docs/backend
            pullPolicy: Always
            # Overrides the image tag whose default is the chart appVersion.
            tag: "v2" 
          service:
            type: ClusterIP
            port: 8000
          env:
            PROJECT_NAME: "demo-infra"
            COMPOSE_PROJECT_NAME: "demo-infra"
            STATE : "dev"
        
            DJANGO_SECRET: "django-insecure-wg^%+ars38!mkmwy+%8w3p48%5)4v-)__ele$$z%!_8l&7!+wq"
        
            DJANGO_ALLOW_ASYNC_UNSAFE: "true"
            PYTHONUNBUFFERED : "1"    
        
        externalDatabase:
          host: "demo_infra"
          port: 5432
          user: demo_infra
          database: demo_infra
          password: ""
          existingSecret: ""
          existingSecretPasswordKey: ""
        
        postgresql:
          enabled: true
          image:
            registry: docker.io
            repository: bitnami/postgresql
            tag: 15.3.0-debian-11-r18
            digest: ""
          auth:
            username: demo_infra
            password: ""
            database: demo_infra
            postgres-password: ""
          architecture: standalone
          service:
            ports:
              postgresql: 5432
            
```

### Installing the application with helm
After that, we can install our django applications with the one command

Before doing that, lets quickly create a namespace <br>
``` kubeclt create namespace demo-infra```

Go to the helm project directory, <br>
``` helm install demo-infra . -n demo-infra```

#### Checking the componentes
After installing, we can see our deployment is successful,
To check for its working or not,
``` kubectl get services -n demo-infra``` <br>
```kubectl get pods -n demo-infra``` <br>
     ```kubectl ge ingress -n demo-infra ```<br>

### Uninstalling the helm releases

OK so finally, we can uninstall our helm deployment,

``` helm uninstall demo-infra -n demo-infra```


### Video References
    https://www.loom.com/share/40f1efa6a1f144318a931f116bdc9595
    
    








 

