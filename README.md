# kafka-event-chaos-injection
Inject exceptions to events to test the resilience of consumers

# Motivation
Test the resilience of the system against faulty events. 
The events should be part of a process to be able to test how features like exception handling and housekeeping behave.

# Idea:
Use the man in the middle attack pattern to modify Kafka events and let the modified events consume by the software under test.
Thus, the resilience of the software and of overall solutions should be tested.

Possible modifications:
* delete key value
* change datatype of value
* change value semantically (for example datetime to 01.01.1900)
* replace specific value (for example location 'Berlin' gets replaced by 'Hamburg')
* duplicate event
* etc

# Overview

![](overview.png)

## Preparation

<details><summary>CLICK ME</summary>
<p>

## kubernetes deployment
Setup docker-for-windows under docker settings. 

Dashboard can be found at [Dashboard](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/overview?namespace=default) after running command 
```
kubectl proxy
``` 

If there are issue regarding login execute commands
```
$TOKEN=((kubectl -n kube-system describe secret default | Select-String "token:") -split " +")[1]
kubectl config set-credentials docker-desktop --token="${TOKEN}"
```
Afterwards select the ./kube/config or copy the token to the login page.

### Setup local repository
[https://medium.com/htc-research-engineering-blog/setup-local-docker-repository-for-local-kubernetes-cluster-354f0730ed3a](https://medium.com/htc-research-engineering-blog/setup-local-docker-repository-for-local-kubernetes-cluster-354f0730ed3a)

### Todo: paragraph about kafka deployment

## Deploy Kafka
based on
[https://dzone.com/articles/ultimate-guide-to-installing-kafka-docker-on-kuber](https://dzone.com/articles/ultimate-guide-to-installing-kafka-docker-on-kuber)

#### Test kafka

To produce messages create a shell into one of the kafka pods
```
kubectl exec -it kafka-0 /bin/bash
```
and use the following command to create events interactively:
```
kafka-console-producer.sh --broker-list kafka:9092 --topic inbound_topic
```

To consume messages from kafka make a shell into one of the kafka pods and use command:
```
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic outbound_topic --from-beginning
```

</p>
</details>

# Build - deploy - run cycle

## Build a docker image
```
docker build -t <image-name>:<image-tag> .
```

## Push to local repository
```
docker tag <image-name>:<image-tag> <registry>/<image-name>:<image-tag>

docker tag keci:latest localhost:5000/keci:latest
```

## Deploy a pod
To create a POD use
```
apiVersion: v1
kind: Pod
metadata:
  name: keci-pod
  labels:
    app: keci
spec:
  containers:
  - name: keci-container
    image: localhost:5000/keci:latest
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 3600']
```


## Getting Started

To run the software navigate to the folder and run command  
```
python index.py
### Build docker image
docker build -t keci .

### Start interactive with command
docker run -i -t  keci /bin/bash
python src/app.py

### Start interactive 
docker run -i -t  keci
```

## Test execution
Execute command
```
pytest --cov=.
```
in the root folder of the project.

### Prerequisites

Required modules:
```
pip -install -r requirements.txt
```

### Coding style

pep8 remarks taken into account as well as pylint.

