# Módulo de Observabilidade

Este módulo cuida do monitoramento do sistema utilizando o Grafana.

## Conteúdo do Módulo

- **Dockerfile**: Utiliza a imagem oficial do Grafana para configurar um container de monitoramento. Se necessário, este Dockerfile pode ser customizado para incluir configurações ou dashboards específicos.
- **README.md**: Este arquivo, que contém as instruções para utilização e configuração do monitoramento.

## Como Funciona

Ao construir e executar o container via Docker Compose, o serviço de observabilidade (Grafana) ficará disponível na porta 3000. Você poderá acessar a interface web do Grafana através de [http://localhost:3000](http://localhost:3000) e configurar os dashboards desejados.

## Personalizações (Opcional)

- Para utilizar uma configuração customizada, adicione um arquivo `grafana.ini` no mesmo diretório e atualize o Dockerfile para copiá-lo para o container.
- Dashboards customizados podem ser adicionados copiando-os para um diretório que seja montado ou incluído na imagem.
