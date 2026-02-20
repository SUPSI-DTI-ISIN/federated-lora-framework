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
            port: 3001,
            proxy: {
                '/api_mlflow': {
                    target: env.VITE_MLFLOW_SERVICE_URL,
                    changeOrigin: true,
                },
                '/api_federated_learning_management': {
                    target: env.VITE_FEDERATED_LEARNING_MANAGEMENT_SERVICE_URL,
                    changeOrigin: true,
                }
            }
        },
    }
})
