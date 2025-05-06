# Prometheus Monitoring Setup

Esta pasta contém os arquivos necessários para configurar um servidor Prometheus usando Docker para monitorar o sistema.

## Visão Geral

O Prometheus é uma ferramenta open-source de monitoramento e alerta. Esta configuração foi criada para colher métricas, incluindo dados do `postgres_exporter`, que monitora o PostgreSQL.

## Arquivos

- **Dockerfile**: Define como construir a imagem Docker do Prometheus.
- **config.yml**: Arquivo de configuração do Prometheus que especifica as configurações globais e os alvos de captura de métricas.
- **readme.md**: Este arquivo com orientações e instruções.

## Configuração (config.yml)

```yaml
global:
  scrape_interval: 15s  # Intervalo entre as coletas de métricas

scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']
