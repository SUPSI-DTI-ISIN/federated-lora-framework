import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig(({mode}) => {
    const env = loadEnv(mode, process.cwd(), '');

    return {
        plugins: mode === 'test'
            ? []
            : [react()],
        define: {
            'import.meta.env.MODE': JSON.stringify(mode)
        },
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
                }
            }
        },
    }
})
