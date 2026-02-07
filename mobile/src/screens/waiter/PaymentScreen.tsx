import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, Alert, Share } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import QRCode from 'react-native-qrcode-svg';
import { useWaiterStore } from '../../store/waiter.store';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { ChevronLeft, Copy, CheckCircle, Share2 } from 'lucide-react-native';
import { Button } from '../../ui/components/Button';
import { Card } from '../../ui/components/Card';

export default function PaymentScreen() {
  const navigation = useNavigation<any>();
  const { paymentData, selectedTableNumber, resetWaiterFlow, clearPayment } = useWaiterStore();

  if (!paymentData) return null;

  const handleCopyCode = () => {
    // Simulação de cópia (em produção usaria Clipboard do RN)
    Alert.alert("Copiado", "Código Pix copiado para a área de transferência.");
  };

  const handleShare = async () => {
    try {
      await Share.share({
        message: `Pagamento Mesa ${selectedTableNumber}: ${paymentData.qrCode}`,
      });
    } catch (error) {
      console.error(error);
    }
  };

  const handleFinish = () => {
    Alert.alert(
      "Confirmar Recebimento",
      "Você confirma que o cliente realizou o pagamento?",
      [
        { text: "Ainda não", style: "cancel" },
        { 
          text: "Sim, Finalizar", 
          onPress: () => {
            resetWaiterFlow();
            navigation.navigate('WaiterTables');
          } 
        }
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ChevronLeft color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Pagamento Mesa #{selectedTableNumber}</Text>
      </View>

      <View style={styles.content}>
        <Card style={styles.qrCard}>
          <Text style={styles.qrLabel}>Aguardando Pagamento Pix</Text>
          
          <View style={styles.qrContainer}>
            <QRCode
              value={paymentData.qrCode}
              size={220}
              color={colors.text.primary}
              backgroundColor={colors.surface}
            />
          </View>

          <View style={styles.amountContainer}>
            <Text style={styles.amountLabel}>Valor Total</Text>
            <Text style={styles.amountValue}>R$ {paymentData.totalAmount.toFixed(2)}</Text>
          </View>
        </Card>

        <View style={styles.actions}>
          <TouchableOpacity style={styles.actionBtn} onPress={handleCopyCode}>
            <Copy size={20} color={colors.primary} />
            <Text style={styles.actionText}>Copiar Código</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionBtn} onPress={handleShare}>
            <Share2 size={20} color={colors.primary} />
            <Text style={styles.actionText}>Compartilhar</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.footer}>
          <Button 
            label="Confirmar e Liberar Mesa"
            onPress={handleFinish}
            style={styles.finishBtn}
          />
          <TouchableOpacity onPress={() => navigation.goBack()} style={styles.cancelBtn}>
            <Text style={styles.cancelText}>Voltar</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { padding: spacing.lg, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  backBtn: { padding: spacing.sm, backgroundColor: colors.surface, borderRadius: 12 },
  headerTitle: { fontSize: typography.size.sm, fontWeight: 'bold', color: colors.text.primary },
  content: { flex: 1, padding: spacing.xl, alignItems: 'center' },
  qrCard: { width: '100%', alignItems: 'center', padding: spacing.xl, backgroundColor: colors.surface },
  qrLabel: { fontSize: 12, fontWeight: 'black', color: colors.primary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: spacing.xl },
  qrContainer: { padding: spacing.lg, backgroundColor: '#FFF', borderRadius: 20, marginBottom: spacing.xl },
  amountContainer: { alignItems: 'center' },
  amountLabel: { fontSize: 12, color: colors.text.secondary, fontWeight: 'bold', textTransform: 'uppercase' },
  amountValue: { fontSize: 32, fontWeight: '900', color: colors.text.primary, marginTop: 4 },
  actions: { flexDirection: 'row', gap: spacing.md, marginTop: spacing.xl },
  actionBtn: { flex: 1, height: 56, backgroundColor: colors.surface, borderRadius: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, borderWidth: 1, borderColor: colors.border },
  actionText: { color: colors.text.primary, fontWeight: 'bold', fontSize: 12 },
  footer: { width: '100%', marginTop: 'auto', gap: spacing.md },
  finishBtn: { height: 64, borderRadius: 20, backgroundColor: colors.status.success },
  cancelBtn: { height: 48, alignItems: 'center', justifyContent: 'center' },
  cancelText: { color: colors.text.muted, fontWeight: 'bold' }
});
