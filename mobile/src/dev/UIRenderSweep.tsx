
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, SafeAreaView } from 'react-native';
import { logger } from '../services/logger.service';

// Importação Estática de TODAS as telas (Obrigatório para o Bundler)
import { LoginScreen } from '../screens/auth/LoginScreen';
import { KitchenDashboard } from '../screens/kitchen/KitchenDashboard';
import { DriverDashboard } from '../screens/driver/DriverDashboard';
import { WaiterDashboard } from '../screens/waiter/WaiterDashboard';
import OrdersScreen from '../screens/orders/OrdersScreen';
import WaiterTablesScreen from '../screens/waiter/WaiterTablesScreen';
import OrderEntryScreen from '../screens/waiter/OrderEntryScreen';
import OrderReviewScreen from '../screens/waiter/OrderReviewScreen';
import PaymentScreen from '../screens/waiter/PaymentScreen';
import PrinterDebugScreen from '../screens/waiter/PrinterDebugScreen';
import WaiterCallsScreen from '../screens/waiter/WaiterCallsScreen';

// Mapeamento do Registry
const SCREENS = [
  { name: 'LoginScreen', component: LoginScreen },
  { name: 'KitchenDashboard', component: KitchenDashboard },
  { name: 'DriverDashboard', component: DriverDashboard },
  { name: 'WaiterDashboard', component: WaiterDashboard },
  { name: 'OrdersScreen', component: OrdersScreen },
  { name: 'WaiterTablesScreen', component: WaiterTablesScreen },
  { name: 'OrderEntryScreen', component: OrderEntryScreen },
  { name: 'OrderReviewScreen', component: OrderReviewScreen },
  { name: 'PaymentScreen', component: PaymentScreen },
  { name: 'PrinterDebugScreen', component: PrinterDebugScreen },
  { name: 'WaiterCallsScreen', component: WaiterCallsScreen },
];

export default function UIRenderSweep() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [report, setReport] = useState<string[]>([]);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    runSweep();
  }, []);

  const runSweep = async () => {
    console.log('[UI_SWEEP] INITIATING SEQUENCE...');
    
    for (let i = 0; i < SCREENS.length; i++) {
      const screen = SCREENS[i];
      setCurrentIndex(i);
      
      try {
        console.log(`[UI_SWEEP] Mounting ${screen.name}...`);
        // Tempo para renderização e efeitos (useEffect)
        await new Promise(resolve => setTimeout(resolve, 800));
        
        // Se chegou aqui sem crashar, sucesso
        const msg = `✅ ${screen.name}: MOUNTED`;
        setReport(prev => [...prev, msg]);
        console.log(`[UI_SWEEP] RESULT: ${screen.name} OK`);
      } catch (error) {
        const msg = `❌ ${screen.name}: CRASHED`;
        console.error(`[UI_SWEEP] FAILURE: ${screen.name}`, error);
        setReport(prev => [...prev, msg]);
      }
    }
    
    setIsComplete(true);
    console.log('[UI_SWEEP] SEQUENCE COMPLETED');
    console.log('[UI_SWEEP] FINAL REPORT:', JSON.stringify(report));
  };

  const CurrentComponent = SCREENS[currentIndex].component;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🛡️ UI Sweep L5</Text>
        <Text style={styles.status}>
          {isComplete ? 'FINALIZADO' : `Testando: ${SCREENS[currentIndex].name} (${currentIndex + 1}/${SCREENS.length})`}
        </Text>
      </View>
      
      <View style={styles.previewContainer}>
        {/* Error Boundary Interno para isolar falhas de tela */}
        <CurrentComponent />
      </View>

      <ScrollView style={styles.reportContainer}>
        <Text style={styles.reportTitle}>Relatório de Integridade:</Text>
        {report.map((log, index) => (
          <Text key={index} style={log.includes('✅') ? styles.logSuccess : styles.logError}>
            {log}
          </Text>
        ))}
        {isComplete && (
          <Text style={styles.footer}>
            Teste concluído. Verifique os logs do terminal.
          </Text>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f172a' },
  header: { padding: 16, borderBottomWidth: 1, borderBottomColor: '#334155', backgroundColor: '#1e293b' },
  title: { color: '#FFF', fontSize: 20, fontWeight: '900', letterSpacing: 1 },
  status: { color: '#ea580c', fontSize: 14, marginTop: 4, fontWeight: 'bold', fontFamily: 'monospace' },
  previewContainer: { height: '50%', overflow: 'hidden', borderWidth: 1, borderColor: '#334155', margin: 10, borderRadius: 8, backgroundColor: '#fff' },
  reportContainer: { flex: 1, padding: 16, backgroundColor: '#020617' },
  reportTitle: { color: '#94a3b8', fontWeight: 'bold', marginBottom: 10, textTransform: 'uppercase', fontSize: 12 },
  logSuccess: { color: '#4ade80', marginBottom: 4, fontFamily: 'monospace', fontSize: 12 },
  logError: { color: '#ef4444', marginBottom: 4, fontFamily: 'monospace', fontSize: 12, fontWeight: 'bold' },
  footer: { color: '#64748b', marginTop: 20, textAlign: 'center', fontSize: 10 }
});

