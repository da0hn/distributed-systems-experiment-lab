import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';

const root = document.getElementById('root');
if (root === null) {
  throw new Error('O elemento #root nao existe em index.html');
}

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
