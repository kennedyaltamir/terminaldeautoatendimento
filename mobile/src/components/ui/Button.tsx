import React from 'react';
import { 
  TouchableOpacity, 
  ActivityIndicator, 
  StyleSheet, 
  ViewStyle, 
  TextStyle 
} from 'react-native';
import { COLORS, SPACING, RADIUS } from '../../theme/tokens';
import { Typography } from './Typography';

/**
 * @file Button.tsx
 * @description Componente de ação primário com suporte a variantes e estados.
 */

type ButtonVariant = 'primary' | 'outline' | 'ghost';

interface ButtonProps {
  label: string;
  onPress: () => void;
  variant?: ButtonVariant;
  isLoading?: boolean;
  disabled?: boolean;
  style?: ViewStyle;
}

export const Button = ({ 
  label, 
  onPress, 
  variant = 'primary', 
  isLoading = false, 
  disabled = false,
  style 
}: ButtonProps) => {
  const isPrimary = variant === 'primary';
  const isOutline = variant === 'outline';

  const containerStyle = [
    styles.base,
    isPrimary && styles.primary,
    isOutline && styles.outline,
    disabled && styles.disabled,
    style,
  ];

  const textStyle: TextStyle = {
    color: isPrimary ? '#FFFFFF' : isOutline ? COLORS.primary : COLORS.text.secondary,
    fontWeight: 'bold',
  };

  return (
    <TouchableOpacity 
      onPress={onPress} 
      disabled={disabled || isLoading}
      activeOpacity={0.7}
      style={containerStyle as ViewStyle}
    >
      {isLoading ? (
        <ActivityIndicator color={isPrimary ? '#FFFFFF' : COLORS.primary} />
      ) : (
        <Typography variant="body" style={textStyle}>
          {label}
        </Typography>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  base: {
    height: 56,
    borderRadius: RADIUS.lg,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: SPACING.xl,
    flexDirection: 'row',
  },
  primary: {
    backgroundColor: COLORS.primary,
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  outline: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  disabled: {
    backgroundColor: COLORS.surface,
    borderColor: 'transparent',
    opacity: 0.5,
  },
});
