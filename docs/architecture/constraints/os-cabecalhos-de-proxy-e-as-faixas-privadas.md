# Os cabeçalhos de proxy só são confiáveis dentro das faixas privadas

Dois proxies ficam entre o navegador e cada serviço, e nenhum processo enxerga o pedido
original. Duas linhas de configuração tratam disso, e elas trabalham em par.

`spring.cloud.gateway.server.webflux.trusted-proxies`, no `api-gateway`, casa as três
faixas privadas da RFC 1918 — que é onde vivem tanto a rede do Compose quanto a do
cluster. `server.forward-headers-strategy: framework` está no `api-gateway`, no
`lab-plane` e no `lab-journal`.

**Sem `trusted-proxies`, o gateway não confia em proxy nenhum, e o efeito é
silencioso.** Ele descarta os `X-Forwarded-*` que recebe e não emite os que deveria
emitir. O serviço de destino recebe a requisição sem saber quem pediu nem por qual
esquema, o roteamento funciona e o status é 200.

**Sem `forward-headers-strategy`, o Spring monta URL absoluta a partir do que enxerga**
— `http://api-gateway:8000` —, e não a partir do que o navegador pediu. O primeiro lugar
onde isso quebra é o `redirect_uri` de OIDC, que o provedor recusa por não casar com o
registrado.

**A restrição que fica é o alcance.** Confiar em `X-Forwarded-*` só é seguro porque a
origem está restrita às faixas privadas; qualquer cliente que alcançasse o processo
poderia forjar o próprio endereço. Publicar o gateway direto na internet exige rever as
duas linhas juntas, e não uma delas.
