
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import * as Sentry from '@sentry/react-native';
import { COLORS } from '../../theme/tokens';

/**
 * Componente de Diagnóstico para validar Telemetria.
 * NÃO DEVE SER EXIBIDO EM PRODUÇÃO PARA USUÁRIOS FINAIS.
 */
export const CrashTester = () => {
  const forceJsCrash = () => {
    throw new Error("MesaFlow Test Crash (JS)");
  };

  const forceNativeCrash = () => {
    Sentry.nativeCrash();
  };

  const forceApiError = () => {
    Sentry.captureMessage("Teste de Mensagem Manual");
    alert("Mensagem enviada ao Sentry");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🔧 Telemetry Diagnostics</Text>
      
      <TouchableOpacity style={[styles.btn, { backgroundColor: '#ef4444' }]} onPress={forceJsCrash}>
        <Text style={styles.text}>💥 Force JS Crash</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.btn, { backgroundColor: '#b91c1c' }]} onPress={forceNativeCrash}>
        <Text style={styles.text}>💣 Force Native Crash</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.btn, { backgroundColor: '#3b82f6' }]} onPress={forceApiError}>
        <Text style={styles.text}>📨 Send Test Message</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: '#1e293b', borderRadius: 12, margin: 10 },
  title: { color: '#fff', fontWeight: 'bold', marginBottom: 15, textAlign: 'center' },
  btn: { padding: 15, borderRadius: 8, marginBottom: 10, alignItems: 'center' },
  text: { color: '#fff', fontWeight: 'bold' }
});

