import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, Dimensions } from 'react-native';
import { LogOut, Clock } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';
import { SafeAreaView } from 'react-native-safe-area-context';

const { width } = Dimensions.get('window');
const COLUMN_WIDTH = (width - 60) / 2;

const MOCK_TABLES = [
  { id: 1, number: 1, status: 'free', customer: null },
  { id: 2, number: 2, status: 'occupied', customer: 'Kennedy', total: 'R$ 154,90', time: '45min' },
  { id: 3, number: 3, status: 'alert', customer: 'Mesa 3', total: 'R$ 42,00', time: '12min' },
  { id: 4, number: 4, status: 'free', customer: null },
  { id: 5, number: 5, status: 'occupied', customer: 'Ana Silva', total: 'R$ 89,00', time: '20min' },
  { id: 6, number: 6, status: 'free', customer: null },
];

export function WaiterDashboard() {
  const { logout, user } = useAuthStore();

  const renderTable = ({ item }: { item: typeof MOCK_TABLES[0] }) => (
    <TouchableOpacity 
      style={[
        styles.tableCard, 
        item.status === 'occupied' && styles.tableOccupied,
        item.status === 'alert' && styles.tableAlert
      ]}
    >
      <View style={styles.tableHeader}>
        <Text style={styles.tableNumber}>#{item.number}</Text>
        <View style={[styles.statusDot, styles[`status_${item.status}` as keyof typeof styles]]} />
      </View>

      {item.customer ? (
        <View style={styles.tableInfo}>
          <Text style={styles.customerName} numberOfLines={1}>{item.customer}</Text>
          <Text style={styles.totalAmount}>{item.total}</Text>
          <View style={styles.timeContainer}>
            <Clock size={12} color="#64748b" />
            <Text style={styles.timeText}>{item.time}</Text>
          </View>
        </View>
      ) : (
        <View style={styles.freeContainer}>
          <Text style={styles.freeText}>LIVRE</Text>
        </View>
      )}
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.welcome}>Olá, {user?.name || 'Garçom'}</Text>
          <Text style={styles.title}>Mapa de Mesas</Text>
        </View>
        <TouchableOpacity style={styles.logoutBtn} onPress={logout}>
          <LogOut color="#ef4444" size={24} />
        </TouchableOpacity>
      </View>

      <FlatList
        data={MOCK_TABLES}
        renderItem={renderTable}
        keyExtractor={(item) => item.id.toString()}
        numColumns={2}
        contentContainerStyle={styles.listContent}
        columnWrapperStyle={styles.columnWrapper}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f1f5f9' },
  header: { 
    padding: 24, 
    backgroundColor: '#0f172a', 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center',
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  welcome: { color: '#94a3b8', fontSize: 14, fontWeight: '500' },
  title: { color: '#fff', fontSize: 24, fontWeight: '900' },
  logoutBtn: { backgroundColor: '#1e293b', borderRadius: 12, padding: 10 },
  listContent: { padding: 20 },
  columnWrapper: { justifyContent: 'space-between', marginBottom: 16 },
  tableCard: { 
    width: COLUMN_WIDTH, 
    height: 150, 
    backgroundColor: '#fff', 
    borderRadius: 20, 
    padding: 16,
    justifyContent: 'space-between',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    borderWidth: 1,
    borderColor: '#e2e8f0'
  },
  tableOccupied: { borderColor: '#ea580c', borderWidth: 2 },
  tableAlert: { borderColor: '#ef4444', borderWidth: 2 },
  tableHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  tableNumber: { fontSize: 22, fontWeight: '900', color: '#1e293b' },
  statusDot: { width: 10, height: 10, borderRadius: 5 },
  status_free: { backgroundColor: '#22c55e' },
  status_occupied: { backgroundColor: '#ea580c' },
  status_alert: { backgroundColor: '#ef4444' },
  tableInfo: { gap: 4 },
  customerName: { fontSize: 14, fontWeight: 'bold', color: '#ea580c', textTransform: 'uppercase' },
  totalAmount: { fontSize: 16, fontWeight: '800', color: '#1e293b' },
  timeContainer: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  timeText: { fontSize: 12, color: '#64748b' },
  freeContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  freeText: { color: '#94a3b8', fontWeight: 'bold', letterSpacing: 1 }
});
