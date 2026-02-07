
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Dimensions } from 'react-native';
import { FlashList } from '@shopify/flash-list';
import { LogOut, Clock, User, LayoutGrid } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';

const { width } = Dimensions.get('window');
const COLUMN_WIDTH = (width - (spacing.lg * 3)) / 2;

const MOCK_TABLES = [
  { id: 1, number: 1, status: 'free', customer: null },
  { id: 2, number: 2, status: 'occupied', customer: 'Kennedy', total: 'R$ 154,90', time: '45min' },
  { id: 3, number: 3, status: 'alert', customer: 'Mesa 3', total: 'R$ 42,00', time: '12min' },
  { id: 4, number: 4, status: 'free', customer: null },
];

export function WaiterDashboard() {
  const { logout, user } = useAuthStore();

  const renderTable = ({ item }: { item: any }) => (
    <TouchableOpacity 
      style={[
        styles.tableCard, 
        item.status === 'occupied' && styles.tableOccupied,
        item.status === 'alert' && styles.tableAlert
      ]}
    >
      <View style={styles.tableHeader}>
        <Text style={styles.tableNumber}>#{item.number}</Text>
        <View style={[styles.statusDot, { backgroundColor: item.status === 'free' ? colors.status.success : item.status === 'alert' ? colors.status.danger : colors.primary }]} />
      </View>
      {item.customer ? (
        <View style={styles.tableInfo}>
          <Text style={styles.customerName} numberOfLines={1}>{item.customer}</Text>
          <Text style={styles.totalAmount}>{item.total}</Text>
          <View style={styles.timeContainer}>
            <Clock size={12} color={colors.text.muted} />
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
          <LogOut color={colors.status.danger} size={22} />
        </TouchableOpacity>
      </View>
      
      <View style={{ flex: 1, minHeight: 2 }}>
        <FlashList
          data={MOCK_TABLES}
          renderItem={renderTable}
          keyExtractor={(item) => item.id.toString()}
          numColumns={2}
          contentContainerStyle={styles.listContent}
          estimatedItemSize={150}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { 
    padding: spacing.xl, 
    backgroundColor: colors.background, 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: colors.border
  },
  welcome: { color: colors.text.muted, fontSize: 12, fontWeight: 'bold', textTransform: 'uppercase' },
  title: { color: colors.text.primary, fontSize: 24, fontWeight: '900' },
  logoutBtn: { padding: spacing.sm, backgroundColor: colors.surface, borderRadius: 12 },
  listContent: { padding: spacing.lg },
  tableCard: { 
    width: COLUMN_WIDTH, 
    height: 150, 
    backgroundColor: colors.surface, 
    borderRadius: 20, 
    padding: spacing.md,
    justifyContent: 'space-between',
    marginBottom: spacing.lg,
    marginHorizontal: spacing.xs,
    borderWidth: 1,
    borderColor: colors.border
  },
  tableOccupied: { borderColor: colors.primary, borderWidth: 2 },
  tableAlert: { borderColor: colors.status.danger, borderWidth: 2 },
  tableHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  tableNumber: { fontSize: 22, fontWeight: '900', color: colors.text.primary },
  statusDot: { width: 10, height: 10, borderRadius: 5 },
  tableInfo: { gap: 2 },
  customerName: { fontSize: 14, fontWeight: 'bold', color: colors.primary, textTransform: 'uppercase' },
  totalAmount: { fontSize: 16, fontWeight: '800', color: colors.text.primary },
  timeContainer: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  timeText: { fontSize: 12, color: colors.text.muted },
  freeContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  freeText: { color: colors.text.muted, fontWeight: 'bold', letterSpacing: 1, fontSize: 10 }
});

