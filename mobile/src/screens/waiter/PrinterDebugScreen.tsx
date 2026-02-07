import React, { useState } from 'react';
import { View, Text, StyleSheet, SafeAreaView, FlatList, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { bluetoothService, BluetoothDevice } from '../../services/bluetooth.service';
import { PrinterService } from '../../services/printer.service';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { ChevronLeft, Printer, RefreshCw, Play } from 'lucide-react-native';
import { Button } from '../../ui/components/Button';
import { Card } from '../../ui/components/Card';
import { logger } from '../../services/logger.service';

const TAG = 'PrinterDebugScreen';

export default function PrinterDebugScreen() {
  const navigation = useNavigation();
  const [devices, setDevices] = useState<BluetoothDevice[]>([]);
  const [isScanning, setIsScanning] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleScan = async () => {
    setIsScanning(true);
    try {
      const found = await bluetoothService.scanDevices();
      setDevices(found);
    } finally {
      setIsScanning(false);
    }
  };

  const handleTestPrint = async () => {
    if (!selectedId) return Alert.alert("Aviso", "Selecione uma impressora primeiro.");

    const mockOrder = {
      id: "TEST-123",
      table_number: 99,
      total_amount: 10.00,
      items: [{ name: "Teste de Impressão", quantity: 1, price: 10.00 }]
    };

    try {
      const success = await PrinterService.printOrder(mockOrder, "MesaFlow Debug", selectedId);
      if (success) {
        Alert.alert("Sucesso", "Comando enviado para a impressora.");
      } else {
        Alert.alert("Erro", "Falha ao comunicar com o hardware.");
      }
    } catch (e) {
      logger.error(TAG, 'Erro no teste de impressão', e);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ChevronLeft color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Debug de Hardware</Text>
      </View>

      <View style={styles.content}>
        <Card style={styles.infoCard}>
          <Text style={styles.infoTitle}>Teste de Impressão Bluetooth</Text>
          <Text style={styles.infoDesc}>Use esta tela para validar a conexão com impressoras térmicas físicas.</Text>
        </Card>

        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Dispositivos Encontrados</Text>
          <TouchableOpacity onPress={handleScan} disabled={isScanning}>
            {isScanning ? <ActivityIndicator size="small" color={colors.primary} /> : <RefreshCw size={20} color={colors.primary} />}
          </TouchableOpacity>
        </View>

        <FlatList 
          data={devices}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <TouchableOpacity onPress={() => setSelectedId(item.id)}>
              <Card style={[styles.deviceCard, selectedId === item.id && styles.deviceSelected]}>
                <Printer size={24} color={selectedId === item.id ? colors.primary : colors.text.muted} />
                <View style={{ flex: 1 }}>
                  <Text style={styles.deviceName}>{item.name}</Text>
                  <Text style={styles.deviceAddress}>{item.address}</Text>
                </View>
              </Card>
            </TouchableOpacity>
          )}
          ListEmptyComponent={
            <Text style={styles.emptyText}>Nenhuma impressora pareada ou encontrada.</Text>
          }
        />

        <Button 
          label="Disparar Teste de Impressão"
          onPress={handleTestPrint}
          disabled={!selectedId}
          style={styles.printBtn}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { padding: spacing.lg, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  backBtn: { padding: spacing.sm, backgroundColor: colors.surface, borderRadius: 12 },
  headerTitle: { fontSize: typography.size.sm, fontWeight: 'bold', color: colors.text.primary },
  content: { flex: 1, padding: spacing.xl },
  infoCard: { marginBottom: spacing.xl, backgroundColor: colors.surface },
  infoTitle: { color: colors.text.primary, fontWeight: 'bold', fontSize: 16 },
  infoDesc: { color: colors.text.secondary, fontSize: 12, marginTop: 4 },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: spacing.lg },
  sectionTitle: { color: colors.text.muted, fontSize: 10, fontWeight: 'black', textTransform: 'uppercase', letterSpacing: 1 },
  deviceCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.sm, borderWeight: 1, borderColor: 'transparent' },
  deviceSelected: { borderColor: colors.primary, backgroundColor: colors.primary + '10' },
  deviceName: { color: colors.text.primary, fontWeight: 'bold' },
  deviceAddress: { color: colors.text.muted, fontSize: 10, marginTop: 2 },
  emptyText: { color: colors.text.muted, textAlign: 'center', marginTop: 40, fontSize: 12 },
  printBtn: { marginTop: 'auto', height: 64, borderRadius: 20 }
});
