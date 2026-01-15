
import React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { AlertTriangle, WifiOff, ShieldAlert, ServerCrash, RefreshCw } from 'lucide-react-native';
import { Button } from './Button';
import { COLORS } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';

interface ErrorStateViewProps {
  type: '403' | '500' | 'OFFLINE' | 'TIMEOUT' | 'UNKNOWN';
  message?: string;
  onRetry?: () => void;
  onAction?: () => void;
  actionLabel?: string;
}

export const ErrorStateView = ({ type, message, onRetry, onAction, actionLabel }: ErrorStateViewProps) => {
  const config = {
    '403': { icon: ShieldAlert, title: 'Acesso Negado', color: COLORS.status.danger, defaultMsg: 'Sua sessão expirou ou você não tem permissão para acessar esta área.' },
    '500': { icon: ServerCrash, title: 'Falha no Servidor', color: COLORS.status.danger, defaultMsg: 'Ocorreu um erro interno. Nossa equipe técnica já foi notificada.' },
    'OFFLINE': { icon: WifiOff, title: 'Sem Conexão', color: COLORS.status.warning, defaultMsg: 'Verifique sua internet para continuar operando.' },
    'TIMEOUT': { icon: RefreshCw, title: 'Tempo Esgotado', color: COLORS.status.info, defaultMsg: 'O servidor demorou muito para responder.' },
    'UNKNOWN': { icon: AlertTriangle, title: 'Algo deu errado', color: COLORS.text.secondary, defaultMsg: 'Ocorreu um erro inesperado.' },
  }[type];

  const Icon = config.icon;

  return (
    <View style={styles.container}>
      <View style={[styles.iconCircle, { backgroundColor: config.color + '20' }]}>
        <Icon size={48} color={config.color} />
      </View>
      <Text style={styles.title}>{config.title}</Text>
      <Text style={styles.message}>{message || config.defaultMsg}</Text>
      
      <View style={styles.actions}>
        {onRetry && (
          <Button 
            title="Tentar Novamente" 
            variant="primary" 
            onPress={onRetry} 
            style={styles.button}
          />
        )}
        {onAction && actionLabel && (
          <Button 
            title={actionLabel} 
            variant="outline" 
            onPress={onAction} 
            style={styles.button}
          />
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xxl, backgroundColor: COLORS.background },
  iconCircle: { width: 100, height: 100, borderRadius: 50, alignItems: 'center', justifyContent: 'center', marginBottom: spacing.xl },
  title: { fontSize: typography.size.xl, fontWeight: '900', color: COLORS.text.primary, marginBottom: spacing.md, textAlign: 'center' },
  message: { fontSize: typography.size.md, color: COLORS.text.secondary, textAlign: 'center', lineHeight: 24, marginBottom: spacing.xxxl },
  actions: { width: '100%', gap: spacing.md },
  button: { width: '100%' }
});

