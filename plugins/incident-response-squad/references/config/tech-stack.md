# Tech Stack — incident-response-squad

## Monitoramento & Métricas
- **Datadog** — Monitoramento de infraestrutura, APM, métricas customizadas
- **Prometheus** — Métricas open-source com PromQL
- **Grafana** — Visualização de métricas e dashboards de incidente
- **CloudWatch** — Métricas e alarmes AWS nativos
- **New Relic** — APM e observabilidade full-stack
- **Zabbix** — Monitoramento de infraestrutura on-premise

## Plataformas de Log
- **ELK Stack** (Elasticsearch + Logstash + Kibana) — Logs centralizados e busca full-text
- **Splunk** — Enterprise log analytics e SIEM
- **CloudWatch Logs** — Logs AWS nativos (Lambda, ECS, EC2)
- **Grafana Loki** — Logs para stack Grafana (label-based)
- **Datadog Log Management** — Logs integrados com métricas e APM
- **Fluentd / Fluent Bit** — Coletores de log open-source

## Gestão de Incidentes & Alertas
- **PagerDuty** — Gestão de alertas, on-call schedules, escalonamento
- **OpsGenie** (Atlassian) — Alertas, escalonamento e resposta
- **VictorOps** (Splunk On-Call) — Incident management
- **FireHydrant** — Plataforma de gerenciamento de incidentes
- **incident.io** — Gestão de incidentes integrada ao Slack

## Status Pages
- **Statuspage.io** (Atlassian) — Status page externo/interno
- **Atlassian Statuspage** — Comunicação de status para clientes
- **Cachet** — Status page open-source self-hosted
- **Instatus** — Status page moderno e rápido

## Distributed Tracing
- **Jaeger** — Distributed tracing open-source
- **Zipkin** — Distributed tracing
- **AWS X-Ray** — Tracing para aplicações AWS
- **Datadog APM** — Traces integrados com métricas

## Orquestração & Infraestrutura
- **Kubernetes** — Orquestração de containers
- **AWS ECS/EKS** — Serviços de container AWS
- **Terraform** — Infrastructure as Code
- **Ansible** — Automação de configuração

## Comunicação
- **Slack** — Canal principal de comunicação de incidentes (#incidents)
- **Microsoft Teams** — Comunicação corporativa
- **Email** — Notificações formais de alta severidade

## Runbook & Automação
- **Rundeck** — Automação de runbooks
- **AWS Systems Manager** — Run Command, Automation
- **PagerDuty Rundeck** — Runbooks integrados com alertas
- **Bash/Python scripts** — Automação customizada
