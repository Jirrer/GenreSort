import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default ({ mode }) => {
  // Load env from one directory above
  const env = loadEnv(mode, path.resolve(__dirname, '..'), '')
  const apiUrl = env.VITE_API_URL

  if (!apiUrl) throw new Error("VITE_API_URL is not defined!")

  return defineConfig({
    plugins: [react()],
    server: {
      proxy: {
        '/passInPlaylist': {
          target: apiUrl,
          changeOrigin: true,
          secure: false,
        },
        '/pingServer': {
          target: apiUrl,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  })
}
