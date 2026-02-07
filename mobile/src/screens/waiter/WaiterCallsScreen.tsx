import React from 'react';
import { View, Text, StyleSheet, FlatList, SafeAreaView, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useWaiterStore, ServiceRequest } from '../../store/waiter.store';
import { Card } from '../../ui/components/Card';
import { Button } from '../../ui/components/Button';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { ChevronLeft, BellRing, CheckCircle, MessageSquare, Receipt, Sparkles } from 'lucide-react-native';

export default function WaiterCallsScreen() {
  const navigation = useNavigation();
  const { serviceRequests, resolveRequest } = useWaiterStore();

  const getIcon = (type: string) => {
    switch(type) {
      case 'bill': return <Receipt size={24} color={colors.status.success} />;
      case 'cleaning': return <Sparkles size={24} color={colors.status.info} />;
      default: return <MessageSquare size={24} color={colors.primary} />;
    }
  };

  const getLabel = (type: string) => {
    switch(type) {
      case 'bill': return 'PEDIU A CONTA';
      case 'cleaning': return 'SOLICITOU LIMPEZA';
      case 'help': return 'PRECISA DE AJUDA';
      default: return 'CHAMADO GERAL';
    }
  };

  const renderCall = ({ item }: { item: ServiceRequest }) => (
    <Card style={styles.callCard}>
      <View style={styles.callHeader}>
        <View style={styles.tableBadge}>
          <Text style={styles.tableText}>MESA {item.table}</Text>
        </View>
        <Text style={styles.timeText}>Agora</Text>
      </View>

      <View style={styles.callBody}>
        <View style={styles.iconContainer}>
          {getIcon(item.service_type)}
        </View>
        <View style={styles.contentContainer}>
          <Text style={styles.callLabel}>{getLabel(item.service_type)}</Text>
          {item.notes && <Text style={styles.notes}>"{item.notes}"</Text>}
        </View>
      </View>

      <Button 
        label="Atender Chamado"
        onPress={() => resolveRequest(item.id)}
        variant="outline"
        style={styles.resolveBtn}
      />
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ChevronLeft color={colors.text.primary} />
        </TouchableOpacity>
        <View>
          <Text style={styles.title}>Chamados Ativos</Text>
          <Text style={styles.subtitle}>{serviceRequests.length} solicitações pendentes</Text>
        </View>
      </View>

      <FlatList
        data={serviceRequests}
        renderItem={renderCall}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.empty}>
            <CheckCircle size={64} color={colors.status.success} style={{ opacity: 0.2 }} />
            <Text style={styles.emptyText}>Nenhum chamado pendente no momento.</Text>
          </View>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { padding: spacing.xl, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  backBtn: { padding: spacing.sm, backgroundColor: colors.surface, borderRadius: 12 },
  title: { fontSize: typography.size.lg, fontWeight: 'bold', color: colors.text.primary },
  subtitle: { fontSize: 10, color: colors.text.muted, textTransform: 'uppercase' },
  list: { padding: spacing.lg },
  callCard: { marginBottom: spacing.lg, borderLeftWidth: 4, borderLeftColor: colors.primary },
  callHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: spacing.md },
  tableBadge: { backgroundColor: colors.primary, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 4 },
  tableText: { color: '#FFF', fontSize: 10, fontWeight: 'black' },
  timeText: { fontSize: 10, color: colors.text.muted, fontWeight: 'bold' },
  callBody: { flexDirection: 'row', gap: spacing.md, marginBottom: spacing.lg },
  iconContainer: { width: 48, height: 48, borderRadius: 24, backgroundColor: colors.background, justifyContent: 'center', alignItems: 'center' },
  contentContainer: { flex: 1, justifyContent: 'center' },
  callLabel: { fontSize: 16, fontWeight: 'black', color: colors.text.primary },
  notes: { fontSize: 12, color: colors.text.secondary, fontStyle: 'italic', marginTop: 2 },
  resolveBtn: { height: 44, borderColor: colors.border },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingTop: 100 },
  emptyText: { color: colors.text.muted, fontSize: typography.size.sm, marginTop: spacing.lg, textAlign: 'center' }
});
import React from 'react';
import { View, Text, StyleSheet, FlatList, SafeAreaView, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useWaiterStore, ServiceRequest } from '../../store/waiter.store';
import { Card } from '../../ui/components/Card';
import { Button } from '../../ui/components/Button';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { ChevronLeft, BellRing, CheckCircle, MessageSquare, Receipt, Sparkles } from 'lucide-react-native';

export default function WaiterCallsScreen() {
  const navigation = useNavigation();
  const { serviceRequests, resolveRequest } = useWaiterStore();

  const getIcon = (type: string) => {
    switch(type) {
      case 'bill': return <Receipt size={24} color={colors.status.success} />;
      case 'cleaning': return <Sparkles size={24} color={colors.status.info} />;
      default: return <MessageSquare size={24} color={colors.primary} />;
    }
  };

  const getLabel = (type: string) => {
    switch(type) {
      case 'bill': return 'PEDIU A CONTA';
      case 'cleaning': return 'SOLICITOU LIMPEZA';
      case 'help': return 'PRECISA DE AJUDA';
      default: return 'CHAMADO GERAL';
    }
  };

  const renderCall = ({ item }: { item: ServiceRequest }) => (
    <Card style={styles.callCard}>
      <View style={styles.callHeader}>
        <View style={styles.tableBadge}>
          <Text style={styles.tableText}>MESA {item.table}</Text>
        </View>
        <Text style={styles.timeText}>Agora</Text>
      </View>

      <View style={styles.callBody}>
        <View style={styles.iconContainer}>
          {getIcon(item.service_type)}
        </View>
        <View style={styles.contentContainer}>
          <Text style={styles.callLabel}>{getLabel(item.service_type)}</Text>
          {item.notes && <Text style={styles.notes}>"{item.notes}"</Text>}
        </View>
      </View>

      <Button 
        label="Atender Chamado"
        onPress={() => resolveRequest(item.id)}
        variant="outline"
        style={styles.resolveBtn}
      />
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ChevronLeft color={colors.text.primary} />
        </TouchableOpacity>
        <View>
          <Text style={styles.title}>Chamados Ativos</Text>
          <Text style={styles.subtitle}>{serviceRequests.length} solicitações pendentes</Text>
        </View>
      </View>

      <FlatList
        data={serviceRequests}
        renderItem={renderCall}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.empty}>
            <CheckCircle size={64} color={colors.status.success} style={{ opacity: 0.2 }} />
            <Text style={styles.emptyText}>Nenhum chamado pendente no momento.</Text>
          </View>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { padding: spacing.xl, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  backBtn: { padding: spacing.sm, backgroundColor: colors.surface, borderRadius: 12 },
  title: { fontSize: typography.size.lg, fontWeight: 'bold', color: colors.text.primary },
  subtitle: { fontSize: 10, color: colors.text.muted, textTransform: 'uppercase' },
  list: { padding: spacing.lg },
  callCard: { marginBottom: spacing.lg, borderLeftWidth: 4, borderLeftColor: colors.primary },
  callHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: spacing.md },
  tableBadge: { backgroundColor: colors.primary, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 4 },
  tableText: { color: '#FFF', fontSize: 10, fontWeight: 'black' },
  timeText: { fontSize: 10, color: colors.text.muted, fontWeight: 'bold' },
  callBody: { flexDirection: 'row', gap: spacing.md, marginBottom: spacing.lg },
  iconContainer: { width: 48, height: 48, borderRadius: 24, backgroundColor: colors.background, justifyContent: 'center', alignItems: 'center' },
  contentContainer: { flex: 1, justifyContent: 'center' },
  callLabel: { fontSize: 16, fontWeight: 'black', color: colors.text.primary },
  notes: { fontSize: 12, color: colors.text.secondary, fontStyle: 'italic', marginTop: 2 },
  resolveBtn: { height: 44, borderColor: colors.border },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingTop: 100 },
  emptyText: { color: colors.text.muted, fontSize: typography.size.sm, marginTop: spacing.lg, textAlign: 'center' }
});
