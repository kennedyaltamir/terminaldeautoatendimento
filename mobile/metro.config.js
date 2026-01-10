const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

// Obtém a configuração padrão do Expo para o Metro
const config = getDefaultConfig(__dirname);

// Garante que o Metro foque apenas na pasta mobile e ignore a raiz do projeto para evitar conflitos de node_modules
config.resolver.nodeModulesPaths = [
  path.resolve(__dirname, 'node_modules'),
];

config.watchFolders = [
  path.resolve(__dirname),
];

module.exports = config;
