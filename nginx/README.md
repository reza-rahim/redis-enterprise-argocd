
### Nginx

https://kubernetes.github.io/ingress-nginx/deploy/#gce-gke

```
kubectl create ns ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/reza-rahim/redis-enterprise-argocd/refs/heads/main/nginx/deploy.yaml

kubectl get -n ingress-nginx svc

```
