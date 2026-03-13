import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        analytics: resolve(__dirname, 'Analytics_Page.html'),
        emergency: resolve(__dirname, 'Emergency_Alert_Panel.html'),
        dashboard: resolve(__dirname, 'Main_Dashboard.html'),
        triage: resolve(__dirname, 'Patient_Symptom_Summaries.html')
      }
    }
  }
});
