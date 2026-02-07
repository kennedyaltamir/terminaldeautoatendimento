import React from 'react';
import { Text, StyleSheet, TextStyle, TextProps } from 'react-native';
import { COLORS } from '../../theme/tokens';

/**
 * @file Typography.tsx
 * @description Componente base para textos padronizados.
 */

type TypographyVariant = 'h1' | 'h2' | 'body' | 'caption' | 'label';

interface TypographyProps extends TextProps {
  variant?: TypographyVariant;
  color?: string;
  align?: 'left' | 'center' | 'right';
}

export const Typography = ({ 
  variant = 'body', 
  color, 
  align = 'left', 
  style, 
  children, 
  ...props 
}: TypographyProps) => {
  const textStyle = [
    styles.base,
    styles[variant],
    { color: color || styles[variant].color, textAlign: align },
    style,
  ];

  return (
    <Text style={textStyle as TextStyle} {...props}>
      {children}
    </Text>
  );
};

const styles = StyleSheet.create({
  base: {
    fontFamily: 'System', // Expo usará a fonte padrão do sistema
  },
  h1: {
    fontSize: 32,
    fontWeight: '900',
    color: COLORS.text.primary,
    letterSpacing: -0.5,
  },
  h2: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text.primary,
  },
  body: {
    fontSize: 16,
    fontWeight: '400',
    color: COLORS.text.primary,
    lineHeight: 24,
  },
  caption: {
    fontSize: 12,
    fontWeight: '500',
    color: COLORS.text.secondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text.secondary,
  },
});
