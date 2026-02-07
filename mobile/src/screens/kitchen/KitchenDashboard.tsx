
import React, { useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { FlashList } from '@shopify/flash-list';
import { LogOut, Clock, CheckCircle2, ChefHat } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';
import { useOrdersStore } from '../../store/orders.store';
import { useSessionStore } from '../../store/session.store';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { ErrorStateView } from '../../components/ui/ErrorStateView';

export function KitchenDashboard() {
  const logout = useAuthStore((state) => state.logout);
  const slug = useSessionStore((state) => state.slug);
  const { orders, isLoading, error, fetchOrders, advanceStatus } = useOrdersStore();

  useEffect(() => {
    if (slug) fetchOrders(slug);
  }, [slug]);

  if (error) return <ErrorStateView type="500" message={error} onRetry={() => slug && fetchOrders(slug)} />;

  const renderOrder = ({ item }: { item: any }) => (
    <View style={[styles.orderCard, { borderLeftColor: item.status === 'ready' ? colors.status.success : colors.primary }]}>
      <View style={styles.orderHeader}>
        <View>
          <Text style={styles.tableText}>Mesa {item.table?.table_number || 'Balcão'}</Text>
          <Text style={styles.orderId}>#{item.id.slice(0,6)} • {item.customer_name}</Text>
        </View>
        <View style={styles.timeBadge}>
          <Clock size={14} color={colors.text.muted} />
          <Text style={styles.timeText}>{item.elapsedTime || '0m'}</Text>
        </View>
      </View>
      <View style={styles.itemsContainer}>
        {item.items.map((subItem: any, idx: number) => (
          <Text key={idx} style={styles.itemText}>
            <Text style={{ fontWeight: 'bold', color: colors.primary }}>{subItem.quantity}x</Text> {subItem.product.name}
          </Text>
        ))}
      </View>
      <TouchableOpacity 
        style={styles.actionBtn} 
        onPress={() => slug && advanceStatus(item.id, item.status, slug)}
      >
        <CheckCircle2 color="#fff" size={20} />
        <Text style={styles.btnText}>AVANÇAR STATUS</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.titleRow}>
          <ChefHat color={colors.primary} size={28} />
          <Text style={styles.title}>Cozinha</Text>
        </View>
        <TouchableOpacity style={styles.logoutBtn} onPress={logout}>
          <LogOut color={colors.status.danger} size={22} />
        </TouchableOpacity>
      </View>
      
      <View style={{ flex: 1, minHeight: 2 }}>
        {isLoading ? (
          <ActivityIndicator style={{marginTop: 50}} color={colors.primary} size="large" />
        ) : (
          <FlashList
            data={orders}
            renderItem={renderOrder}
            keyExtractor={(item) => item.id}
            contentContainerStyle={styles.listContent}
            estimatedItemSize={150}
            ListEmptyComponent={
              <View style={styles.emptyContainer}>
                <ChefHat size={64} color={colors.surface} />
                <Text style={styles.emptyText}>Nenhum pedido em produção</Text>
              </View>
            }
          />
        )}
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
  titleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  title: { color: colors.text.primary, fontSize: typography.size.lg, fontWeight: '900' },
  logoutBtn: { padding: spacing.sm, backgroundColor: colors.surface, borderRadius: 12 },
  listContent: { padding: spacing.lg },
  orderCard: { backgroundColor: colors.surface, borderRadius: 16, padding: spacing.lg, marginBottom: spacing.md, borderLeftWidth: 6 },
  orderHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: spacing.md },
  tableText: { fontSize: 20, fontWeight: '900', color: colors.text.primary },
  orderId: { fontSize: 12, color: colors.text.muted, fontWeight: 'bold' },
  timeBadge: { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: colors.background, paddingHorizontal: 8, borderRadius: 8, height: 24 },
  timeText: { fontSize: 10, fontWeight: 'bold', color: colors.text.secondary },
  itemsContainer: { paddingVertical: spacing.md, borderTopWidth: 1, borderBottomWidth: 1, borderColor: colors.border, gap: 4 },
  itemText: { fontSize: 16, color: colors.text.secondary },
  actionBtn: { marginTop: spacing.md, backgroundColor: colors.primary, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, paddingVertical: 14, borderRadius: 12 },
  btnText: { color: '#fff', fontWeight: 'bold', fontSize: 14 },
  emptyContainer: { alignItems: 'center', marginTop: 100, opacity: 0.5 },
  emptyText: { color: colors.text.muted, marginTop: spacing.md, fontWeight: 'bold' }
});

