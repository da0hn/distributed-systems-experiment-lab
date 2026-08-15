# O mapa de caminhos vive num lugar só

O serviço de destino é escolhido pelo prefixo do caminho, e quem escolhe é o
`api-gateway`. O mapa está em `api-gateway/src/main/resources/application.yml`, e em
nenhum outro arquivo.

| Prefixo               | Destino       | Ordem |
|-----------------------|---------------|-------|
| `/api/lab-plane/**`   | `lab-plane`   | 10    |
| `/api/lab-journal/**` | `lab-journal` | 10    |
| `/**`                 | `frontend`    | 100   |

A ordem é explícita. Sem ela a precedência viria da posição na lista, e uma rota movida
por um motivo sem relação nenhuma com precedência mudaria o roteamento em silêncio.

Os outros pontos da borda não repetem esse mapa:

- `frontend/nginx.conf` serve os estáticos e **recusa** `/api` com 404, em vez de
  roteá-lo. Sem a recusa, o `try_files` entregaria o `index.html` com 200, e um `fetch`
  que espera JSON quebraria no parse — longe da causa, que é uma rota errada no gateway.
- `frontend/vite.config.ts` tem uma entrada só: tudo sob `/api` vai para o proxy de
  borda, e não para os serviços um a um.
- `local/traefik/dynamic.yml` casa um hostname e entrega tudo ao gateway, com a mesma
  forma do recurso de exposição do cluster.

**Nenhum filtro remove prefixo.** Cada serviço carrega o próprio prefixo em
`server.servlet.context-path`, então o caminho público e o interno são o mesmo. Com um
`StripPrefix` no gateway, toda URL absoluta gerada por um serviço — o `Location` de um
201, o link de um stream — sairia sem o prefixo. Nada falharia na subida: o cliente é
que seguiria para um caminho que o gateway não conhece.

**Um mapa em três sintaxes diverge, e a divergência só aparece em produção.** O prefixo
já viveu ao mesmo tempo no proxy do Vite, no nginx da imagem e no recurso de exposição
do cluster. Hoje vive num lugar, e o mesmo processo roteia no desenvolvimento e no
cluster. Manter o proxy no nginx também poria o pod do frontend no caminho de toda
chamada de API, o que faz de uma página estática um ponto de falha para o instrumento.

O frontend e a API dividem a mesma origem, e é o `/api` que separa a chamada de serviço
do arquivo estático. Daí não haver CORS, nem preflight, nem `withCredentials` no SSE.
