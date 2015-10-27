id: "webserver-controller"
kind: "ReplicationController"
apiVersion: "v1beta1"
desiredState:
  replicas: 1
  replicaSelector:
    selectorname: "webserver"
  podTemplate:
    desiredState:
      manifest:
        version: "v1beta1"
        id: "webserver-controller"
        containers:
          - name: "apache-frontend"
            image: "jeffbean/jeffbean"
            ports:
              - containerPort: 8001
                hostPort: 80
    labels:
      name: "webserver"
      selectorname: "webserver"
      uses: "db"
  labels:
    name: "webserver"