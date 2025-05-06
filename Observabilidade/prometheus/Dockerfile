FROM prom/prometheus

COPY config.yml /etc/prometheus/prometheus.yml

EXPOSE 9090

CMD ["--config.file=/etc/prometheus/prometheus.yml"]
