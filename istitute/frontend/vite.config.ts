import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig(({mode}) => {
    const env = loadEnv(mode, process.cwd(), 'VITE_');
    return {
        plugins: mode === 'test'
            ? []
            : [react(), tailwindcss()],
        server: {
            host: '0.0.0.0',
            port: 3000,
            proxy: {
                '/api_inference': {
                    target: env.VITE_INFERENCE_SERVICE_URL,
                    changeOrigin: true,
                },
                '/api_data': {
                    target: env.VITE_DATA_SERVICE_URL,
                    changeOrigin: true,
                },
                '/api_model': {
                    target: env.VITE_MODEL_SERVICE_URL,
                    changeOrigin: true,
                }
            }
        },
    }
})
