
# Prerequisites
- docker
- docker compose

## How to start llm:
```bash
docker compose up
```

find endpoints at
[ranking.http](ranking.http)

## How to stop llm:
```bash
docker compose down
```

## Activate the Rank monitoring:
Go to http://localhost:3004/ login with username `admin` and password `grafana`

go to dashboard click on import dashboard![import-dashbord.png](import-dashbord.png)

copy the json file at [dashboard.json](provisioning/dashboard/dashboard.json) and click load

Congratulations!