import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, SafeAreaView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useWaiterStore } from '../../store/waiter.store';
import { useSessionStore } from '../../store/session.store';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { ChevronLeft, Printer, CheckCircle, WifiOff } from 'lucide-react-native';
import { Button } from '../../ui/components/Button';
import { Card } from '../../ui/components/Card';
import { logger } from '../../services/logger.service';

const TAG = 'OrderReviewScreen';

export default function OrderReviewScreen() {
  const navigation = useNavigation<any>();
  const slug = useSessionStore(state => state.slug);
  
  const { 
    selectedTableNumber, 
    cart, 
    getCartTotal, 
    submitOrder, 
    isSubmitting,
    updateQuantity,
    resetWaiterFlow
  } = useWaiterStore();

  const [showSuccess, setShowSuccess] = useState(false);
  const [isOfflineMode, setIsOfflineMode] = useState(false);

  const handleConfirm = async () => {
    if (!slug) return;
    
    const result = await submitOrder(slug);
    if (result.success) {
      setIsOfflineMode(result.offline);
      setShowSuccess(true);
    } else {
      Alert.alert("Erro", "Não foi possível processar o pedido. Verifique os itens.");
    }
  };

  const handleFinish = () => {
    resetWaiterFlow();
    navigation.navigate('WaiterTables');
  };

  const renderItem = ({ item }: { item: any }) => (
    <Card style={styles.itemCard}>
      <View style={styles.itemInfo}>
        <Text style={styles.itemName}>{item.name}</Text>
        <Text style={styles.itemPrice}>R$ {(item.price * item.quantity).toFixed(2)}</Text>
      </View>
      {!showSuccess && (
        <View style={styles.counter}>
          <TouchableOpacity onPress={() => updateQuantity(item.productId, -1)} style={styles.counterBtn}>
            <Text style={styles.counterSymbol}>-</Text>
          </TouchableOpacity>
          <Text style={styles.counterText}>{item.quantity}</Text>
          <TouchableOpacity onPress={() => updateQuantity(item.productId, 1)} style={styles.counterBtn}>
            <Text style={styles.counterSymbol}>+</Text>
          </TouchableOpacity>
        </View>
      )}
    </Card>
  );

  if (showSuccess) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.successContainer}>
          {isOfflineMode ? (
            <WifiOff size={80} color={colors.status.warning} />
          ) : (
            <CheckCircle size={80} color={colors.status.success} />
          )}
          
          <Text style={styles.successTitle}>
            {isOfflineMode ? "Pedido em Fila" : "Pedido Enviado!"}
          </Text>
          
          <Text style={styles.successSubtitle}>
            {isOfflineMode 
              ? "Sem internet no momento. O pedido foi salvo no dispositivo e será enviado automaticamente."
              : `A cozinha já recebeu o pedido da Mesa #${selectedTableNumber}`
            }
          </Text>
          
          <View style={styles.successActions}>
            {!isOfflineMode && (
              <Button 
                label="Imprimir Ticket"
                variant="outline"
                onPress={() => Alert.alert("Impressão", "Buffer gerado.")}
                style={styles.printBtn}
              />
            )}
            <Button 
              label="Finalizar Atendimento"
              onPress={handleFinish}
              style={styles.finishBtn}
            />
          </View>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ChevronLeft color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Revisar Pedido - Mesa #{selectedTableNumber}</Text>
      </View>

      <FlatList 
        data={cart}
        renderItem={renderItem}
        keyExtractor={(item) => item.productId.toString()}
        contentContainerStyle={styles.list}
      />

      <View style={styles.footer}>
        <View style={styles.totalRow}>
          <Text style={styles.totalLabel}>Total do Pedido</Text>
          <Text style={styles.totalValue}>R$ {getCartTotal().toFixed(2)}</Text>
        </View>

        <Button 
          label="Confirmar e Enviar"
          onPress={handleConfirm}
          isLoading={isSubmitting}
          disabled={cart.length === 0}
          style={styles.submitBtn}
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
  list: { padding: spacing.lg },
  itemCard: { flexDirection: 'row', alignItems: 'center', marginBottom: spacing.md, padding: spacing.md },
  itemInfo: { flex: 1 },
  itemName: { fontSize: 16, fontWeight: 'bold', color: colors.text.primary },
  itemPrice: { fontSize: 14, color: colors.text.secondary, marginTop: 2 },
  counter: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, backgroundColor: colors.background, padding: 4, borderRadius: 12 },
  counterBtn: { width: 28, height: 28, borderRadius: 8, backgroundColor: colors.surface, alignItems: 'center', justifyContent: 'center' },
  counterSymbol: { color: colors.primary, fontWeight: 'bold', fontSize: 18 },
  counterText: { color: colors.text.primary, fontWeight: 'bold', minWidth: 20, textAlign: 'center' },
  footer: { padding: spacing.xl, backgroundColor: colors.surface, borderTopLeftRadius: 32, borderTopRightRadius: 32, elevation: 10 },
  totalRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: spacing.xl },
  totalLabel: { fontSize: typography.size.md, color: colors.text.secondary, fontWeight: 'medium' },
  totalValue: { fontSize: typography.size.xl, color: colors.text.primary, fontWeight: '900' },
  submitBtn: { height: 64, borderRadius: 20 },
  successContainer: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xxl },
  successTitle: { fontSize: 28, fontWeight: '900', color: colors.text.primary, marginTop: spacing.xl },
  successSubtitle: { fontSize: 16, color: colors.text.secondary, textAlign: 'center', marginTop: spacing.md, lineHeight: 24 },
  successActions: { width: '100%', marginTop: spacing.xxxl, gap: spacing.md },
  printBtn: { borderColor: colors.border },
  finishBtn: { backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border }
});
