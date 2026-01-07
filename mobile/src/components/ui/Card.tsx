import React from 'react';
import { View, StyleSheet, ViewStyle } from 'react-native';
import { COLORS, RADIUS, SPACING } from '../../theme/tokens';

/**
 * @file Card.tsx
 * @description Componente de superfície para agrupamento de conteúdo.
 */

interface CardProps {
  children: React.ReactNode;
  style?: ViewStyle;
  variant?: 'default' | 'outline';
}

export const Card = ({ children, style, variant = 'default' }: CardProps) => {
  return (
    <View style={[
      styles.base,
      variant === 'outline' && styles.outline,
      style
    ]}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  base: {
    backgroundColor: COLORS.surface,
    borderRadius: RADIUS.xl,
    padding: SPACING.lg,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  outline: {
    backgroundColor: 'transparent',
    borderColor: COLORS.border,
  },
});
