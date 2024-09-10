Prerequisites
Kubernetes 1.23+
Helm 3.8.0+
how to install helm:
 curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh 
./get_helm.sh
PV provisioner support in the underlying infrastructure

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add grafana https://grafana.github.io/helm-charts


helm dependency update ./llm-app

helm install --generate-name --debug ./llm-app


install grafana with postgres as a datasource:

helm install my-grafana grafana/grafana \
  --set datasources.datasources\\.yaml.apiVersion=1 \
  --set datasources.datasources\\.yaml.datasources[0].name=PostgreSQL \
  --set datasources.datasources\\.yaml.datasources[0].type=postgres \
  --set datasources.datasources\\.yaml.datasources[0].url=<POSTGRES_URL>:<POSTGRES_PORT> \
  --set datasources.datasources\\.yaml.datasources[0].database=<POSTGRES_DB> \
  --set datasources.datasources\\.yaml.datasources[0].user=<POSTGRES_USER> \
  --set datasources.datasources\\.yaml.datasources[0].secureJsonData.password=<POSTGRES_PASSWORD> \
  --set datasources.datasources\\.yaml.datasources[0].access=proxy \
  --set datasources.datasources\\.yaml.datasources[0].isDefault=true \
  --set dashboards.default.my-dashboard.json="{ \
      \"id\": 1, \
      \"title\": \"PostgreSQL Dashboard\", \
      \"panels\": [ \
        { \
          \"type\": \"table\", \
          \"title\": \"Sample SQL Query\", \
          \"targets\": [ \
            { \
              \"rawSql\": \"SELECT * FROM my_table LIMIT 10\", \
              \"refId\": \"A\", \
              \"datasource\": \"PostgreSQL\" \
            } \
          ], \
          \"gridPos\": { \"h\": 10, \"w\": 24, \"x\": 0, \"y\": 0 } \
        } \
      ] \
    }"


# replcae the rawSql with the ranking query

# update the secrets in Kubernetes, you modify the secret using the kubectl command:

kubectl create secret generic db-secrets --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -

# verify secret creation:

kubectl get secret db-secrets -o yaml

# Rolling Updates and Pod Restarts
kubectl rollout restart deployment/llm-web
kubectl rollout restart deployment/celery-worker
kubectl rollout restart deployment/celery-beat

# access to the service
minikube turnnel

# to see the env in the pod
kubectl exec -it <pod-name> -- printenv | grep DJANGO_ALLOWED_HOSTS


helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install my-grafana grafana/grafana \
  --set datasources.datasources\\.yaml.apiVersion=1 \
  --set datasources.datasources\\.yaml.datasources[0].name=PostgreSQL \
  --set datasources.datasources\\.yaml.datasources[0].type=postgres \
  --set datasources.datasources\\.yaml.datasources[0].url=postgres_service \
  --set datasources.datasources\\.yaml.datasources[0].database=llm \
  --set datasources.datasources\\.yaml.datasources[0].user=code \
  --set datasources.datasources\\.yaml.datasources[0].secureJsonData.password=1AFUSGlJujzrLgs5iitHW7Buxi4pkUKh \
  --set datasources.datasources\\.yaml.datasources[0].access=proxy \
  --set datasources.datasources\\.yaml.datasources[0].isDefault=true


2XVW8KdpQqXKR9vj8oOTyKQyqH9assitiws8HIeR



from application.llm_service import LLMPerformanceService

LLMPerformanceService().generate_performance_metrics.delay()


from application.llm_service import LLMPerformanceService

LLMPerformanceService().generate_performance_metrics()