const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  // aqui você vai expondo as funções conforme precisar
  // exemplo: chamar o backend Python
  ping: () => ipcRenderer.invoke("ping")
});