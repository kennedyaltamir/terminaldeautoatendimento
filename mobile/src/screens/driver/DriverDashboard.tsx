import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList } from 'react-native';
import { LogOut, MapPin, Phone, Navigation } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';
import { SafeAreaView } from 'react-native-safe-area-context';

const MOCK_DELIVERIES = [
  { id: 'D01', customer: 'Maria Oliveira', address: 'Rua das Flores, 123 - Centro', total: 'R$ 78,50', status: 'ready' },
  { id: 'D02', customer: 'João Souza', address: 'Av. Paulista, 1000 - Bela Vista', total: 'R$ 45,00', status: 'delivering' },
];

export function DriverDashboard() {
  const logout = useAuthStore((state) => state.logout);

  const renderDelivery = ({ item }: { item: typeof MOCK_DELIVERIES[0] }) => (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <Text style={styles.customerName}>{item.customer}</Text>
        <Text style={styles.amount}>{item.total}</Text>
      </View>

      <View style={styles.addressRow}>
        <MapPin size={16} color="#64748b" />
        <Text style={styles.addressText}>{item.address}</Text>
      </View>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.secondaryBtn}>
          <Phone size={20} color="#ea580c" />
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.primaryBtn}>
          <Navigation size={20} color="#fff" />
          <Text style={styles.primaryBtnText}>
            {item.status === 'ready' ? 'INICIAR ROTA' : 'ABRIR MAPA'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Entregas</Text>
        <TouchableOpacity style={styles.logoutBtn} onPress={logout}>
          <LogOut color="#ef4444" size={24} />
        </TouchableOpacity>
      </View>
      
      <FlatList
        data={MOCK_DELIVERIES}
        renderItem={renderDelivery}
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
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 16, marginBottom: 16, elevation: 2 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  customerName: { fontSize: 18, fontWeight: 'bold', color: '#1e293b' },
  amount: { fontSize: 18, fontWeight: '900', color: '#22c55e' },
  addressRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 20 },
  addressText: { fontSize: 14, color: '#64748b', flex: 1 },
  footer: { flexDirection: 'row', gap: 12 },
  secondaryBtn: { width: 50, height: 50, borderRadius: 12, borderColor: '#ea580c', borderWidth: 1, justifyContent: 'center', alignItems: 'center' },
  primaryBtn: { flex: 1, backgroundColor: '#ea580c', borderRadius: 12, flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: 8 },
  primaryBtnText: { color: '#fff', fontWeight: 'bold' }
});
