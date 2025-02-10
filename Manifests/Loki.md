
# Loki Installation and Usage Guide

## Overview
This guide provides detailed instructions for installing and configuring Loki for log aggregation and visualization. It includes steps for:
- Installing Loki using the Grafana Loki Helm chart.
- Configuring Persistent Volumes (PVs) for Loki components.
- Creating a custom Python logging handler using `python-logging-loki`.
- Connecting Loki to Grafana.

---

## Installing Loki Using Helm
Use the official Grafana Loki Helm chart from Bitnami.

### Steps:
1. Add the Bitnami Helm repository (if not already added):
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```

2. Install the Grafana Loki chart:
   ```bash
   helm install my-release oci://registry-1.docker.io/bitnamicharts/grafana-loki
   ```

For additional configuration, refer to the [Grafana Loki Helm chart documentation](https://github.com/bitnami/charts/tree/main/bitnami/grafana-loki/#installing-the-chart).

---

## Configuring Persistent Volumes (PVs)
Persistent Volumes are required for Loki's components: Ingester, Compactor, and Querier.

### PV for Ingester
- **Purpose**: This PV is used by the Loki Ingester component to store ingested log data before they are compacted and queried.

### PV for Compactor
- **Purpose**: This PV is used by the Loki Compactor component to process and compact log data for efficient storage.

### PV for Querier
- **Purpose**: This PV is used by the Loki Querier component to process and serve log queries.

### PV Template
Use the following template to create the required PVs:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: loki-pv-<component>  
spec:
  capacity:
    storage: 8Gi  
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: path/to/your/storage/<component>  
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - <your worker node>  
```

Save this template as separate YAML files for each component (e.g., `ingester-pv.yaml`, `compactor-pv.yaml`, `querier-pv.yaml`) and apply them using:
```bash
kubectl apply -f <filename>.yaml
```

---

## Creating a Python Logging Handler for Loki
Use the `python-logging-loki` library to create a logging handler.

### Installation
Install the library:
```bash
pip install python-logging-loki==0.3.1
```

### Example Code
Use the following code to create a Loki handler in your Python application:
```python
import logging
from logging_loki import LokiHandler

# Configure Loki handler
handler = LokiHandler(
    url="https://my-loki-instance/loki/api/v1/push",  
    tags={"application": "my-app"},
    auth=("username", "password"),  
    version="1",
)

# Set up logger
logger = logging.getLogger("my-logger")
logger.addHandler(handler)

# Example log
logger.error(
    "Something happened",
    extra={"tags": {"service": "my-service"}},
)
```
For more details, refer to the [python-logging-loki documentation](https://pypi.org/project/python-logging-loki/).

---

## Connecting Loki to Grafana
To visualize logs, connect Loki as a data source in Grafana.

### Steps:
1. Access your Grafana instance.
2. Navigate to **Configuration** > **Data Sources**.
3. Add a new data source:
   - **Type**: `Loki`
   - **URL**: `http://loki-grafana-loki-query-frontend:3100`
4. Save and test the connection.

### Querying Logs in Grafana
- Use the Explore section in Grafana to query and visualize logs collected by Loki.

---

## Summary
This README outlines the steps to:
- Install and configure Loki using Helm.
- Set up Persistent Volumes for Loki's Ingester, Compactor, and Querier components.
- Create a Python logging handler to push logs to Loki.
- Connect and visualize logs in Grafana.

