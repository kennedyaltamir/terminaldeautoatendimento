
import React, { useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, ActivityIndicator, Linking } from 'react-native';
import { LogOut, MapPin, Phone, Navigation, RefreshCw } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';
import { useLogisticsStore } from '../../store/logistics.store';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../../theme/tokens';
import { ErrorStateView } from '../../components/ui/ErrorStateView';
import { useScreenLog } from '../../hooks/useScreenLog';

export function DriverDashboard() {
  useScreenLog("DriverDashboard"); // L5 Telemetry

  const logout = useAuthStore((state) => state.logout);
  const { deliveries, isLoading, fetchDeliveries } = useLogisticsStore();
  const [error, setError] = React.useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setError(false);
    try {
      await fetchDeliveries();
    } catch (e) {
      setError(true);
    }
  };

  const openMap = (address: string) => {
    const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`;
    Linking.openURL(url);
  };

  const renderDelivery = ({ item }: { item: any }) => (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <Text style={styles.customerName}>{item.customer_name}</Text>
        <Text style={styles.amount}>R$ {item.total_amount?.toFixed(2)}</Text>
      </View>
      
      <View style={styles.addressRow}>
        <MapPin size={16} color="#64748b" />
        <Text style={styles.addressText}>{item.delivery_address}</Text>
      </View>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.secondaryBtn}>
          <Phone size={20} color={COLORS.primary} />
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.primaryBtn}
          onPress={() => openMap(item.delivery_address)}
        >
          <Navigation size={20} color="#fff" />
          <Text style={styles.primaryBtnText}>
            {item.status === 'ready' ? 'INICIAR ROTA' : 'ABRIR MAPA'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  if (error) {
    return (
      <ErrorStateView 
        type="UNKNOWN" 
        message="Não foi possível carregar as entregas."
        onRetry={loadData}
      />
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Entregas</Text>
        <View style={{ flexDirection: 'row', gap: 10 }}>
          <TouchableOpacity style={styles.iconBtn} onPress={loadData}>
            <RefreshCw color="#fff" size={24} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.iconBtn} onPress={logout}>
            <LogOut color="#ef4444" size={24} />
          </TouchableOpacity>
        </View>
      </View>

      {isLoading ? (
        <ActivityIndicator style={{ marginTop: 50 }} color={COLORS.primary} size="large" />
      ) : (
        <FlatList
          data={deliveries}
          renderItem={renderDelivery}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <Text style={styles.emptyText}>Nenhuma entrega pendente.</Text>
          }
        />
      )}
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
  iconBtn: { backgroundColor: '#1e293b', borderRadius: 12, padding: 10 },
  listContent: { padding: 16 },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 16, marginBottom: 16, elevation: 2 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  customerName: { fontSize: 18, fontWeight: 'bold', color: '#1e293b' },
  amount: { fontSize: 18, fontWeight: '900', color: '#22c55e' },
  addressRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 20 },
  addressText: { fontSize: 14, color: '#64748b', flex: 1 },
  footer: { flexDirection: 'row', gap: 12 },
  secondaryBtn: { width: 50, height: 50, borderRadius: 12, borderColor: COLORS.primary, borderWidth: 1, justifyContent: 'center', alignItems: 'center' },
  primaryBtn: { flex: 1, backgroundColor: COLORS.primary, borderRadius: 12, flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: 8 },
  primaryBtnText: { color: '#fff', fontWeight: 'bold' },
  emptyText: { textAlign: 'center', marginTop: 50, color: '#64748b' }
});

