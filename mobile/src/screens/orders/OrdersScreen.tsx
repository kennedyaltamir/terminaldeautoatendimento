import React, { useEffect } from 'react';
import { View, Text, StyleSheet, SafeAreaView, ActivityIndicator, Pressable } from 'react-native';
import { FlashList } from '@shopify/flash-list';
import { useOrdersStore, Order } from '../../store/orders.store';
import { useSessionStore } from '../../store/session.store';
import { useSettingsStore } from '../../store/settings.store';
import { Card } from '../../ui/components/Card';
import { Button } from '../../ui/components/Button';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { RefreshCw, WifiOff, AlertCircle, ChefHat, Bell, BellOff } from 'lucide-react-native';
import LoadingScreen from '../common/LoadingScreen';

export default function OrdersScreen() {
  const { 
    orders, 
    isLoading, 
    isSyncing, 
    isSocketConnected, 
    isHydrated,
    error, 
    fetchOrders, 
    advanceStatus 
  } = useOrdersStore();

  const { isSilentMode, toggleSilentMode } = useSettingsStore();
  const slug = useSessionStore(state => state.slug);

  useEffect(() => {
    if (isHydrated && slug) {
      fetchOrders(slug);
    }
  }, [isHydrated, slug]);

  if (!isHydrated) {
    return <LoadingScreen />;
  }

  const getSLAColor = (status?: string) => {
    switch (status) {
      case 'BREACHED': return colors.status.danger;
      case 'CRITICAL': return colors.status.warning;
      case 'WARNING': return colors.status.info;
      default: return colors.status.success;
    }
  };

  const renderOrder = ({ item }: { item: Order }) => (
    <Card style={[styles.orderCard, { borderLeftWidth: spacing.xs, borderLeftColor: getSLAColor(item.slaStatus) }]}>
      <View style={styles.cardHeader}>
        <View>
          <Text style={styles.orderId}>#{item.id.slice(0, 4)}</Text>
          <Text style={styles.customerName}>{item.customer_name || 'Balcão'}</Text>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: getSLAColor(item.slaStatus) + '20' }]}>
          <Text style={[styles.statusText, { color: getSLAColor(item.slaStatus) }]}>
            {item.remainingTime}
          </Text>
        </View>
      </View>

      <View style={styles.itemsContainer}>
        {item.items.map((i, index) => (
          <Text key={index} style={styles.itemText}>
            <Text style={{ fontWeight: 'bold', color: colors.text.primary }}>{i.quantity}x</Text> {i.product.name}
          </Text>
        ))}
      </View>

      <View style={styles.cardFooter}>
        <Text style={styles.elapsedText}>Há {item.elapsedTime}</Text>
        <Button 
          title="Avançar" 
          variant="primary" 
          style={styles.actionButton}
          onPress={() => slug && advanceStatus(item.id, item.status, slug)}
        />
      </View>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      {!isSocketConnected && !isLoading && (
        <View style={styles.offlineBanner}>
          <WifiOff size={12} color="#FFF" />
          <Text style={styles.offlineText}>Conexão Perdida</Text>
        </View>
      )}

      <View style={styles.screenHeader}>
        <View>
          <Text style={styles.title}>KDS Mobile</Text>
          <View style={styles.subtitleRow}>
            <Text style={styles.subtitle}>{slug}</Text>
            {isSyncing && (
              <View style={styles.syncIndicator}>
                <RefreshCw size={10} color={colors.primary} />
                <Text style={styles.syncText}>Sincronizando</Text>
              </View>
            )}
          </View>
        </View>

        <View style={styles.headerActions}>
          {isLoading && <ActivityIndicator size="small" color={colors.primary} style={{ marginRight: spacing.md }} />}

          <Pressable 
            onPress={toggleSilentMode}
            style={({ pressed }) => [
              styles.silentToggle, 
              isSilentMode && styles.silentToggleActive,
              pressed && { opacity: 0.7 }
            ]}
          >
            {isSilentMode ? (
              <BellOff size={20} color={colors.status.danger} />
            ) : (
              <Bell size={20} color={colors.text.secondary} />
            )}
          </Pressable>
        </View>
      </View>

      {error && orders.length === 0 ? (
        <View style={styles.centerContent}>
          <AlertCircle size={48} color={colors.status.danger} style={{ marginBottom: spacing.md }} />
          <Text style={styles.errorTitle}>Falha de Conexão</Text>
          <Text style={styles.errorSubtitle}>{error}</Text>
          <Button 
            title="Tentar Novamente" 
            variant="outline" 
            style={{ marginTop: spacing.xl }}
            onPress={() => slug && fetchOrders(slug)} 
          />
        </View>
      ) : (
        <View style={styles.listContainer}>
          <FlashList
            data={orders}
            renderItem={renderOrder}
            keyExtractor={(item) => item.id}
            contentContainerStyle={styles.listContent}
            estimatedItemSize={180}
            showsVerticalScrollIndicator={false}
            ListEmptyComponent={
              !isLoading ? (
                <View style={styles.centerContent}>
                  <ChefHat size={64} color={colors.text.muted} style={{ opacity: 0.1, marginBottom: spacing.md }} />
                  <Text style={styles.emptyText}>Fila de produção vazia.</Text>
                </View>
              ) : null
            }
          />
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  listContainer: { flex: 1, minHeight: 2 }, // Fix para FlashList em Android
  offlineBanner: {
    backgroundColor: colors.status.danger,
    paddingVertical: 4,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: spacing.xs,
  },
  offlineText: {
    color: '#FFF',
    fontSize: 9,
    fontWeight: '900',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  screenHeader: { 
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.lg,
    borderBottomWidth: 1, 
    borderBottomColor: colors.border,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
  title: { 
    fontSize: typography.size.lg, 
    fontWeight: typography.weight.black, 
    color: colors.text.primary,
    letterSpacing: -0.5,
  },
  subtitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 2,
  },
  subtitle: {
    fontSize: 10,
    color: colors.text.muted,
    textTransform: 'uppercase',
    fontWeight: typography.weight.bold,
  },
  syncIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: spacing.sm,
    backgroundColor: colors.primary + '15',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  syncText: {
    fontSize: 8,
    color: colors.primary,
    fontWeight: typography.weight.black,
    marginLeft: 4,
    textTransform: 'uppercase',
  },
  headerActions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  silentToggle: {
    padding: spacing.sm,
    borderRadius: 12,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
  },
  silentToggleActive: {
    borderColor: colors.status.danger + '50',
    backgroundColor: colors.status.danger + '10',
  },
  listContent: { padding: spacing.lg, paddingBottom: 100 },
  orderCard: { marginBottom: spacing.lg, elevation: 2, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: spacing.md },
  orderId: { fontSize: typography.size.xs, color: colors.text.muted, fontWeight: typography.weight.bold },
  customerName: { fontSize: typography.size.md, color: colors.text.primary, fontWeight: typography.weight.black },
  statusBadge: { 
    paddingHorizontal: spacing.sm, 
    paddingVertical: 2, 
    borderRadius: 6,
    borderWidth: 1,
    borderColor: 'transparent'
  },
  statusText: { fontSize: 10, fontWeight: typography.weight.black },
  itemsContainer: { marginVertical: spacing.sm },
  itemText: { fontSize: typography.size.sm, color: colors.text.secondary, marginBottom: 4 },
  cardFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: spacing.md, borderTopWidth: 1, borderTopColor: colors.border + '50', paddingTop: spacing.md },
  elapsedText: { fontSize: typography.size.xs, color: colors.text.muted, fontWeight: typography.weight.semibold },
  actionButton: { height: 44, paddingHorizontal: spacing.xl, borderRadius: 10 },
  centerContent: { flex: 1, padding: spacing.xxxl, alignItems: 'center', justifyContent: 'center' },
  emptyText: { color: colors.text.muted, fontSize: typography.size.sm, fontWeight: '500' },
  errorTitle: { color: colors.text.primary, fontSize: typography.size.md, fontWeight: '900', marginBottom: spacing.xs },
  errorSubtitle: { color: colors.text.secondary, fontSize: typography.size.sm, textAlign: 'center', maxWidth: '80%' }
});
