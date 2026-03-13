import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        post_visit: resolve(__dirname, 'Post_Visit_Screen.html'),
        symptom_input: resolve(__dirname, 'Symptom_Voice_Input.html'),
        token_welcome: resolve(__dirname, 'Token_Registration_Welcome.html'),
        whatsapp: resolve(__dirname, 'WhatsApp_Integration.html'),
        health_brief: resolve(__dirname, 'Your_Health_Brief.html'),
        alert: resolve(__dirname, 'Your_Turn_Alert.html')
      }
    }
  }
});
