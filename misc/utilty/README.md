```
export RECNAME=south-dev-rec;envsubst < redis-pod.yaml | kubectl apply -n south-dev  -f -

kubectl exec -it -n south-dev redis-pod -- sh
```


