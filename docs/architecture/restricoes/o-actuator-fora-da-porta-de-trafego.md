# O Actuator não fica na porta de tráfego

Os três serviços que a borda alcança expõem `health` e `info` numa porta própria, que o
gateway não roteia. O `api-gateway` expõe também o endpoint `gateway`.

| Serviço             | Porta de tráfego | Porta de gestão           |
|---------------------|------------------|---------------------------|
| `api-gateway`       | 8000             | `${MANAGEMENT_PORT:9000}` |
| `lab-plane`         | 8080             | `${MANAGEMENT_PORT:9080}` |
| `lab-journal`       | 8081             | `${MANAGEMENT_PORT:9081}` |
| `system-under-test` | 8082             | nenhuma; não é roteado    |

**O motivo é `show-details: always`.** O health de cada serviço entrega o estado da
conexão de banco a quem alcançar a URL. Sob o `context-path`, o Actuator cairia em
`/api/lab-plane/actuator/**` — dentro do prefixo que o gateway publica — e o detalhe
atravessaria a fronteira junto com o tráfego normal. Numa porta que o gateway não
roteia, a probe continua funcionando de dentro e nada disso é alcançável de fora.

O `system-under-test` não define porta de gestão, e não precisa: nenhuma rota do gateway
chega até ele ([o sistema medido](o-sistema-medido-nao-conhece-o-instrumento.md)).
