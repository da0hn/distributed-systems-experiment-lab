import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// O frontend fala com dois servicos, e nao com um BFF. E a decisao E-20 de
// 2026-08-06: comando no lab-plane, leitura e streaming no lab-journal.
//
// O que mudou em 2026-08-15 e que ele nao os endereca mais um a um. Existe um
// modulo api-gateway neste reactor, e o servico de destino e escolhido pelo
// prefixo do caminho. Este proxy passou de duas entradas a uma: tudo sob
// `/api` vai para o gateway, e quem sabe o mapa e ele.
//
// O ganho e que o mapa de caminhos deixou de existir em tres lugares. Antes
// estava aqui, no nginx da imagem e no recurso de exposicao do cluster, em
// tres sintaxes; hoje esta no `application.yml` do gateway, e o mesmo
// processo roteia nos dois ambientes. Este arquivo nao carrega mais rota.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // A porta esta escrita aqui, e nao lida do ambiente. Ler exigiria
      // `process.env` e, com ele, `@types/node` — dependencia nova para um
      // numero que muda quando alguem edita `GATEWAY_PORT` no compose, o que
      // nao acontece. O acoplamento e este: se aquele default mudar, este
      // numero muda junto.
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
});
