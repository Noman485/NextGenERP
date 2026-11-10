import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

const apiTarget = process.env.API_PROXY_TARGET ?? 'http://127.0.0.1:8000'
const apiPaths = '^/(auth|products|categories|suppliers|orders|purchase-orders|inventory-transactions|assistant|health|ml)(/.*)?$'

// SPA routes share names with API paths (e.g. /products, /suppliers). A full page
// load or refresh must return index.html, while fetch/XHR calls go to the API.
function isDocumentNavigation(request) {
  if (request.method !== 'GET' && request.method !== 'HEAD') return false
  const accept = request.headers.accept ?? ''
  return accept.includes('text/html')
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // The project lives in a OneDrive folder, where native file events are
    // unreliable on Windows. Polling keeps HMR in sync with saved edits.
    watch: {
      usePolling: true,
      interval: 300,
    },
    proxy: {
      [apiPaths]: {
        target: apiTarget,
        changeOrigin: true,
        bypass(request) {
          return isDocumentNavigation(request) ? '/index.html' : undefined
        },
      },
    },
  },
})
