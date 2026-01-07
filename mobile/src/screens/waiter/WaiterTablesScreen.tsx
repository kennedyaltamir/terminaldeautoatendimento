import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, SafeAreaView, TouchableOpacity, RefreshControl } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useWaiterStore } from '../../store/waiter.store';
import { useSessionStore } from '../../store/session.store';
import { api } from '../../services/api';
import { Card } from '../../ui/components/Card';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { LayoutGrid, User, ChevronRight, BellRing } from 'lucide-react-native';
import { logger } from '../../services/logger.service';

const TAG = 'WaiterTablesScreen';

export default function WaiterTablesScreen() {
  const navigation = useNavigation<any>();
  const [tables, setTables] = useState<any[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const slug = useSessionStore(state => state.slug);
  const { selectTable, setSession, serviceRequests } = useWaiterStore();

  const fetchTables = async () => {
    if (!slug) return;
    try {
      const response = await api.get(`/admin/tables/dashboard`);
      setTables(response.data);
    } catch (e) {
      logger.error(TAG, 'Erro ao carregar mesas', e);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchTables();
  }, [slug, serviceRequests]); // Recarrega se houver novos chamados

  const onRefresh = () => {
    setRefreshing(true);
    fetchTables();
  };

  const handleTableSelect = (item: any) => {
    selectTable(item.id, item.table_number);
    if (item.active_session) {
      setSession(item.active_session.session_token);
    } else {
      setSession(null);
    }
    navigation.navigate('OrderEntry');
  };

  const renderTable = ({ item }: { item: any }) => {
    const isOccupied = item.status === 'occupied' || item.status === 'alert';
    const hasAlert = item.status === 'alert' || serviceRequests.some(r => r.table === item.table_number);
    
    return (
      <TouchableOpacity 
        style={styles.tableWrapper}
        onPress={() => handleTableSelect(item)}
      >
        <Card style={[
          styles.tableCard, 
          isOccupied && styles.tableOccupied,
          hasAlert && styles.tableAlert
        ]}>
          <View style={styles.cardHeader}>
            <Text style={[styles.tableNumber, (isOccupied || hasAlert) && styles.textWhite]}>
              #{item.table_number}
            </Text>
            <View style={[
              styles.statusDot, 
              { backgroundColor: hasAlert ? colors.status.danger : isOccupied ? colors.status.warning : colors.status.success }
            ]} />
          </View>

          {hasAlert ? (
            <View style={styles.alertBox}>
              <BellRing size={16} color="#FFF" />
              <Text style={styles.alertText}>CHAMADO</Text>
            </View>
          ) : isOccupied ? (
            <View style={styles.sessionInfo}>
              <View style={styles.infoRow}>
                <User size={12} color={colors.text.secondary} />
                <Text style={styles.customerName} numberOfLines={1}>
                  {item.active_session?.customer_name}
                </Text>
              </View>
              <Text style={styles.totalSpent}>
                R$ {Number(item.active_session?.total_spent).toFixed(2)}
              </Text>
            </View>
          ) : (
            <Text style={styles.freeText}>LIVRE</Text>
          )}
          
          <View style={styles.cardFooter}>
            <ChevronRight size={16} color={(isOccupied || hasAlert) ? colors.text.secondary : colors.text.muted} />
          </View>
        </Card>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>Salão</Text>
          <Text style={styles.subtitle}>Gestão de Mesas</Text>
        </View>
        <TouchableOpacity 
          onPress={() => navigation.navigate('WaiterCalls')}
          style={styles.callBadge}
        >
          <BellRing size={24} color={serviceRequests.length > 0 ? colors.status.danger : colors.text.muted} />
          {serviceRequests.length > 0 && (
            <View style={styles.badgeCount}>
              <Text style={styles.badgeText}>{serviceRequests.length}</Text>
            </View>
          )}
        </TouchableOpacity>
      </View>

      <FlatList
        data={tables}
        renderItem={renderTable}
        keyExtractor={(item) => item.id.toString()}
        numColumns={2}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { 
    padding: spacing.xl, 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: colors.border
  },
  title: { fontSize: typography.size.lg, fontWeight: typography.weight.black, color: colors.text.primary },
  subtitle: { fontSize: 10, color: colors.text.muted, textTransform: 'uppercase', fontWeight: typography.weight.bold },
  callBadge: { position: 'relative', padding: 4 },
  badgeCount: { position: 'absolute', top: 0, right: 0, backgroundColor: colors.status.danger, borderRadius: 10, width: 18, height: 18, justifyContent: 'center', alignItems: 'center', borderWidth: 2, borderColor: colors.background },
  badgeText: { color: '#FFF', fontSize: 8, fontWeight: 'bold' },
  listContent: { padding: spacing.md },
  tableWrapper: { flex: 1, padding: spacing.xs },
  tableCard: { height: 140, justifyContent: 'space-between', backgroundColor: colors.surface, borderColor: colors.border },
  tableOccupied: { borderColor: colors.primary + '50' },
  tableAlert: { borderColor: colors.status.danger, backgroundColor: colors.status.danger + '20' },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  tableNumber: { fontSize: typography.size.xl, fontWeight: typography.weight.black, color: colors.text.secondary },
  textWhite: { color: colors.text.primary },
  statusDot: { width: 8, height: 8, borderRadius: 4 },
  alertBox: { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: colors.status.danger, padding: 6, borderRadius: 8 },
  alertText: { color: '#FFF', fontSize: 10, fontWeight: 'black' },
  sessionInfo: { marginTop: spacing.sm },
  infoRow: { flexDirection: 'row', alignItems: 'center', gap: 4, marginBottom: 2 },
  customerName: { fontSize: typography.size.xs, color: colors.text.secondary, flex: 1 },
  totalSpent: { fontSize: typography.size.md, fontWeight: typography.weight.bold, color: colors.status.success },
  freeText: { fontSize: 10, fontWeight: typography.weight.black, color: colors.text.muted, letterSpacing: 1 },
  cardFooter: { alignItems: 'flex-end' }
});
