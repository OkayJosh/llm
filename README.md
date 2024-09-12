
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

# Configuring the Refresh Rate:
You can set the refresh rate for the Rank monitoring dashboard or panel. The default
refresh rate is usually set to "off" (manual refresh), but you can configure it
for automatic refreshes, for example, every 5 seconds, 30 seconds, 1 minute, etc.

To configure:

Open your Grafana dashboard.
In the top-right corner, you’ll find the Refresh dropdown.
Select a predefined time range (e.g., 5s, 30s, 1m, etc.),
or enter a custom interval like 30s for 30 seconds or 1m for 1 minute.