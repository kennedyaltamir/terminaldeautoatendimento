import React from 'react';
import { View, StyleSheet, Text, SafeAreaView } from 'react-native';
import { useAuthStore } from '../../store/auth.store';
import { Button } from '../../ui/components/Button';
import { Card } from '../../ui/components/Card';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';

export default function HomeScreen() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.welcomeSection}>
          <Text style={styles.greeting}>Olá,</Text>
          <Text style={styles.userName}>{user?.email || 'Operador'}</Text>
        </View>

        <Card style={styles.statusCard}>
          <View style={styles.statusRow}>
            <View style={styles.indicator} />
            <Text style={styles.statusText}>Sessão Operacional Autorizada</Text>
          </View>
          <Text style={styles.subtext}>Ambiente de produção conectado.</Text>
        </Card>

        <View style={styles.actionSection}>
          <Button 
            title="Sair do Aplicativo" 
            variant="ghost" 
            onPress={logout} 
          />
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    flex: 1,
    padding: spacing.xl,
  },
  welcomeSection: {
    marginTop: spacing.xxl,
    marginBottom: spacing.xxxl,
  },
  greeting: {
    fontSize: typography.size.md,
    color: colors.text.secondary,
    fontWeight: typography.weight.medium,
  },
  userName: {
    fontSize: typography.size.xl,
    color: colors.text.primary,
    fontWeight: typography.weight.bold,
  },
  statusCard: {
    marginBottom: spacing.xl,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  indicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.status.success,
    marginRight: spacing.sm,
  },
  statusText: {
    color: colors.text.primary,
    fontSize: typography.size.sm,
    fontWeight: typography.weight.semibold,
  },
  subtext: {
    color: colors.text.muted,
    fontSize: typography.size.xs,
    fontWeight: typography.weight.medium,
  },
  actionSection: {
    marginTop: 'auto',
  }
});
