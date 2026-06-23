const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const { exec } = require("child_process");
let backendProcess;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  win.loadFile("frontend/dist/index.html");
}

app.whenReady().then(() => {
  const backendPath = app.isPackaged
    ? path.join(process.resourcesPath, "backend.exe")
    : path.join(__dirname, "backend.exe");

  backendProcess = spawn(backendPath, [], {
    windowsHide: true
  });

  createWindow();
});

app.on("before-quit", () => {
  exec("taskkill /F /IM backend.exe /T");
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});