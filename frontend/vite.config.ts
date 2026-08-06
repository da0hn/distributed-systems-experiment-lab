import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// O frontend fala com dois servicos, e nao com um BFF. E a decisao E-20 de
// 2026-08-06: comando no lab-plane, leitura e streaming no lab-journal.
//
// Este proxy serve so ao `npm run dev` na maquina de quem desenvolve, onde
// os dois processos estao em localhost. Na imagem quem rotea e o nginx, e no
// cluster e o recurso de exposicao — os tres precisam declarar o mesmo mapa
// de caminhos, e divergir entre eles quebra so em producao.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api/runs': { target: 'http://localhost:8080', changeOrigin: true },
      '/api/journal': { target: 'http://localhost:8081', changeOrigin: true },
    },
  },
});
