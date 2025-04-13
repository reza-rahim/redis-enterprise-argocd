```
export RECNAME=north-dev-rec;envsubst < https://raw.githubusercontent.com/reza-rahim/redis-enterprise-argocd/refs/heads/main/misc/utilty/redis-pod.yaml| kubectl apply -n north-dev  -f -
kubectl exec -it -n north-dev redis-pod -- sh
kubectl delete -n north-dev po redis-pod 

--

export RECNAME=south-dev-rec;envsubst < redis-pod.yaml | kubectl apply -n south-dev  -f -
kubectl exec -it -n south-dev redis-pod -- sh
kubectl delete -n south-dev po redis-pod 

```


