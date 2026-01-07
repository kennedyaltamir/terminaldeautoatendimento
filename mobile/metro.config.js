const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);

// Removido alias problemático que forçava versão Web do Lucide no Native
config.resolver.alias = {};

// FORÇA A TRANSPILAÇÃO DE MÓDULOS ESM NO NODE_MODULES
config.transformer.unstable_allowModuleTransforms = true; 

module.exports = config;
