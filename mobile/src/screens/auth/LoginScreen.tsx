import React, { useState } from 'react';
import { View, StyleSheet, Text, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import { useAuthStore } from '../../store/auth.store';
import { Button } from '../../ui/components/Button';
import { Input } from '../../ui/components/Input';
import { Card } from '../../ui/components/Card';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const login = useAuthStore((state) => state.login);
  const status = useAuthStore((state) => state.status);
  const error = useAuthStore((state) => state.error);

  /**
   * DÍVIDA TÉCNICA: O status 'hydrating' está sendo reutilizado para login.
   * Em missões futuras, deve-se introduzir 'authenticating'.
   */
  const isSubmitting = status === 'hydrating';

  const handleLogin = async () => {
    if (!email || !password) return;
    try {
      await login({ email, password });
    } catch (e) {
      // Falha capturada pela Store
    }
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.brand}>MesaFlow</Text>
          <Text style={styles.tagline}>Mobile Operations</Text>
        </View>

        <Card style={styles.card}>
          <Text style={styles.title}>Acesso ao Sistema</Text>
          
          {/* Feedback de Erro Global */}
          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error.message}</Text>
            </View>
          )}
          
          <Input
            label="E-mail"
            placeholder="seu@email.com"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            editable={!isSubmitting}
          />

          <Input
            label="Senha"
            placeholder="••••••••"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            editable={!isSubmitting}
          />

          <Button
            title="Entrar"
            onPress={handleLogin}
            isLoading={isSubmitting}
            style={styles.button}
          />
        </Card>
        
        <Text style={styles.footer}>v1.0.0 • 2026</Text>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: spacing.xl,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xxxl,
  },
  brand: {
    fontSize: typography.size.xxl,
    fontWeight: typography.weight.black,
    color: colors.primary,
    letterSpacing: -1,
  },
  tagline: {
    fontSize: typography.size.sm,
    color: colors.text.secondary,
    fontWeight: typography.weight.medium,
    textTransform: 'uppercase',
  },
  card: {
    width: '100%',
  },
  title: {
    fontSize: typography.size.lg,
    fontWeight: typography.weight.bold,
    color: colors.text.primary,
    marginBottom: spacing.xl,
    textAlign: 'center',
  },
  errorContainer: {
    backgroundColor: colors.status.danger + '20', // Opacity 12%
    padding: spacing.md,
    borderRadius: spacing.sm,
    marginBottom: spacing.lg,
    borderWidth: 1,
    borderColor: colors.status.danger + '40',
  },
  errorText: {
    color: colors.status.danger,
    fontSize: typography.size.xs,
    fontWeight: typography.weight.semibold,
    textAlign: 'center',
  },
  button: {
    marginTop: spacing.md,
  },
  footer: {
    textAlign: 'center',
    marginTop: spacing.xxxl,
    color: colors.text.muted,
    fontSize: typography.size.xs,
    fontWeight: typography.weight.medium,
  }
});
