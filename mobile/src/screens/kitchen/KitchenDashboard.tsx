import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList } from 'react-native';
import { LogOut, Clock, CheckCircle2, PlayCircle } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';
import { SafeAreaView } from 'react-native-safe-area-context';

const MOCK_ORDERS = [
  { id: '101', table: '02', customer: 'Kennedy', items: ['2x X-Bacon', '1x Batata G'], status: 'preparing', time: '12:05' },
  { id: '102', table: '05', customer: 'Ana', items: ['1x Combo Kids'], status: 'pending', time: '12:10' },
  { id: '103', table: '01', customer: 'Carlos', items: ['3x Chopp 500ml'], status: 'ready', time: '12:15' },
];

export function KitchenDashboard() {
  const logout = useAuthStore((state) => state.logout);

  const renderOrder = ({ item }: { item: typeof MOCK_ORDERS[0] }) => (
    <View style={[styles.orderCard, styles[`border_${item.status}` as keyof typeof styles]]}>
      <View style={styles.orderHeader}>
        <View>
          <Text style={styles.tableText}>Mesa {item.table}</Text>
          <Text style={styles.orderId}>#{item.id} • {item.customer}</Text>
        </View>
        <View style={styles.timeBadge}>
          <Clock size={14} color="#64748b" />
          <Text style={styles.timeText}>{item.time}</Text>
        </View>
      </View>

      <View style={styles.itemsContainer}>
        {item.items.map((subItem, idx) => (
          <Text key={idx} style={styles.itemText}>{subItem}</Text>
        ))}
      </View>

      <View style={styles.actions}>
        {item.status === 'pending' && (
          <TouchableOpacity style={[styles.actionBtn, styles.btnStart]}>
            <PlayCircle color="#fff" size={20} />
            <Text style={styles.btnText}>INICIAR</Text>
          </TouchableOpacity>
        )}
        {item.status === 'preparing' && (
          <TouchableOpacity style={[styles.actionBtn, styles.btnFinish]}>
            <CheckCircle2 color="#fff" size={20} />
            <Text style={styles.btnText}>FINALIZAR</Text>
          </TouchableOpacity>
        )}
        {item.status === 'ready' && (
          <View style={styles.readyBadge}>
            <Text style={styles.readyText}>AGUARDANDO RETIRADA</Text>
          </View>
        )}
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Cozinha (KDS)</Text>
        <TouchableOpacity style={styles.logoutBtn} onPress={logout}>
          <LogOut color="#ef4444" size={24} />
        </TouchableOpacity>
      </View>
      
      <FlatList
        data={MOCK_ORDERS}
        renderItem={renderOrder}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
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
    alignItems: 'center' 
  },
  title: { color: '#fff', fontSize: 24, fontWeight: 'bold' },
  logoutBtn: { backgroundColor: '#1e293b', borderRadius: 12, padding: 10 },
  listContent: { padding: 16 },
  orderCard: { 
    backgroundColor: '#fff', 
    borderRadius: 16, 
    padding: 16, 
    marginBottom: 16,
    borderLeftWidth: 6,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4
  },
  border_pending: { borderLeftColor: '#f59e0b' },
  border_preparing: { borderLeftColor: '#3b82f6' },
  border_ready: { borderLeftColor: '#22c55e' },
  orderHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 },
  tableText: { fontSize: 20, fontWeight: '900', color: '#1e293b' },
  orderId: { fontSize: 14, color: '#64748b', marginTop: 2 },
  timeBadge: { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: '#f8fafc', padding: 6, borderRadius: 8 },
  timeText: { fontSize: 12, fontWeight: 'bold', color: '#64748b' },
  itemsContainer: { paddingVertical: 12, borderTopWidth: 1, borderBottomWidth: 1, borderColor: '#f1f5f9', gap: 6 },
  itemText: { fontSize: 16, fontWeight: '600', color: '#334155' },
  actions: { marginTop: 12 },
  actionBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, paddingVertical: 12, borderRadius: 12 },
  btnStart: { backgroundColor: '#3b82f6' },
  btnFinish: { backgroundColor: '#22c55e' },
  btnText: { color: '#fff', fontWeight: 'bold', fontSize: 14 },
  readyBadge: { backgroundColor: '#f0fdf4', padding: 10, borderRadius: 8, alignItems: 'center' },
  readyText: { color: '#166534', fontWeight: 'bold', fontSize: 12 }
});
