# Project: Kubernetes Hello World Project based on Flask Microservices
A Kubernetes Hello World Project for Python Flask.  This project uses a simple Flask app that returns correct change as the base project and converts it to Kubernetes.

![Alt Image text](https://github.com/AndreBluhm/Project_Kubernetes-Microservices-Flask/blob/main/Coursera_Cloud-Virtualization-Containers-APIs.png?raw=true "Optional Title")

## Assets in Repo

* `Makefile`:  Builds project
* `Dockerfile`:  Container configuration
* `app.py`:  Flask app
* `kube-hello-change.yaml`: Kubernetes YAML Config

## Get Started

* Create Python virtual environment `python3 -m venv ~/.kube-hello && source ~/.kube-hello/bin/activate`
* Run `make all` to install python libraries, lint project, including `Dockerfile` and run tests

## Build and Run Docker Container

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

* To build the image locally do the following.

`docker build -t flask-change:latest .` or run `make build` which has the same command.

* To verify container run `docker image ls`

* To run do the following:  `docker run -p 8080:8080 flask-change` or run `make run` which has the same command

* In a separate terminal invoke the web service via curl, or run `make invoke` which has the same command 

`curl http://127.0.0.1:8080/change/1/34`

```bash
[
  {
    "5": "quarters"
  }, 
  {
    "1": "nickels"
  }, 
  {
    "4": "pennies"
  }
]
```

* Stop the running docker container by using `control-c` command

## Running Kubernetes Locally

* Verify Kubernetes is working via docker-desktop context

```bash
(.kube-hello) ➜  kubernetes-hello-world-python-flask git:(main) kubectl get nodes
NAME             STATUS   ROLES    AGE   VERSION
docker-desktop   Ready    master   30d   v1.19.3
```

* Run the application in Kubernetes using the following command which tells Kubernetes to setup the load balanced service and run it:  

`kubectl apply -f kube-hello-change.yaml` or run `make run-kube` which has the same command

You can see from the config file that a load-balancer along with three nodes is the configured application.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-flask-change-service
spec:
  selector:
    app: hello-python
  ports:
  - protocol: "TCP"
    port: 8080
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-python
spec:
  selector:
    matchLabels:
      app: hello-python
  replicas: 3
  template:
    metadata:
      labels:
        app: hello-python
    spec:
      containers:
      - name: flask-change
        image: flask-change:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
```

* Verify the container is running

`kubectl get pods`

Here is the output:

```bash
NAME                            READY   STATUS    RESTARTS   AGE
flask-change-7b7d7f467b-26htf   1/1     Running   0          8s
flask-change-7b7d7f467b-fh6df   1/1     Running   0          7s
flask-change-7b7d7f467b-fpsxr   1/1     Running   0          6s
```

* Describe the load balanced service:

`kubectl describe services hello-python-service`

You should see output similar to this:

```bash
Name:                     hello-python-service
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=hello-python
Type:                     LoadBalancer
IP Families:              <none>
IP:                       10.101.140.123
IPs:                      <none>
LoadBalancer Ingress:     localhost
Port:                     <unset>  8080/TCP
TargetPort:               8080/TCP
NodePort:                 <unset>  30301/TCP
Endpoints:                10.1.0.27:8080,10.1.0.28:8080,10.1.0.29:8080
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

Invoke the endpoint to curl it:  

`make invoke`

```bash
curl http://127.0.0.1:8080/change/1/34
[
  {
    "5": "quarters"
  }, 
  {
    "1": "nickels"
  }, 
  {
    "4": "pennies"
  }
]
```

To cleanup the deployment do the following: `kubectl delete deployment hello-python`

## References

* Azure [Kubernetes deployment strategy](https://azure.microsoft.com/en-us/overview/kubernetes-deployment-strategy/)
* Service [Cluster Config](https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/) YAML file
* [Kubernetes.io Hello World](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)
