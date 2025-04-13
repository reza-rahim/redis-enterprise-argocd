```
export RECNAME=north-dev-rec;envsubst < redis-pod.yaml | kubectl apply -n north-dev  -f -
kubectl exec -it -n north-dev redis-pod -- sh

export RECNAME=south-dev-rec;envsubst < redis-pod.yaml | kubectl apply -n south-dev  -f -

kubectl exec -it -n south-dev redis-pod -- sh
```


