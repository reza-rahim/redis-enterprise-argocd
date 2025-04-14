
### Nginx

https://kubernetes.github.io/ingress-nginx/deploy/#gce-gke <br>
Edit nginx-ingress-controller deployment, to include "--enable-ssl-passthrough" flag or patch with kubectl:

```
kubectl create ns ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/reza-rahim/redis-enterprise-argocd/refs/heads/main/nginx/deploy.yaml

kubectl get -n ingress-nginx svc

```
