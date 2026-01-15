
// DOMAIN: MOBILE
// LAST_MODIFIED: 2026-01-11 03:15:00
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

// Fix para erro de import.meta e blank screen no SDK 52
config.transformer.unstable_transformProfile = 'default';

config.resolver.nodeModulesPaths = [
  path.resolve(__dirname, 'node_modules'),
];

config.watchFolders = [
  path.resolve(__dirname),
];

module.exports = config;

