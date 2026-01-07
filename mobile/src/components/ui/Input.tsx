import React, { useState } from 'react';
import { 
  View, 
  TextInput, 
  StyleSheet, 
  TextInputProps, 
  ViewStyle 
} from 'react-native';
import { COLORS, SPACING, RADIUS } from '../../theme/tokens';
import { Typography } from './Typography';

/**
 * @file Input.tsx
 * @description Componente de entrada de texto padronizado.
 */

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  containerStyle?: ViewStyle;
  icon?: React.ReactNode;
}

export const Input = ({ 
  label, 
  error, 
  containerStyle, 
  icon, 
  onFocus, 
  onBlur, 
  ...props 
}: InputProps) => {
  const [isFocused, setIsFocused] = useState(false);

  const handleFocus = (e: any) => {
    setIsFocused(true);
    onFocus?.(e);
  };

  const handleBlur = (e: any) => {
    setIsFocused(false);
    onBlur?.(e);
  };

  return (
    <View style={[styles.container, containerStyle]}>
      {label && (
        <Typography variant="label" style={styles.label}>
          {label}
        </Typography>
      )}
      
      <View style={[
        styles.inputWrapper,
        isFocused && styles.inputFocused,
        !!error && styles.inputError
      ]}>
        {icon && <View style={styles.iconWrapper}>{icon}</View>}
        
        <TextInput
          style={styles.input}
          placeholderTextColor={COLORS.text.muted}
          onFocus={handleFocus}
          onBlur={handleBlur}
          {...props}
        />
      </View>

      {error && (
        <Typography variant="caption" color={COLORS.status.error} style={styles.errorText}>
          {error}
        </Typography>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginBottom: SPACING.md,
  },
  label: {
    marginBottom: SPACING.xs,
    marginLeft: SPACING.xs,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: RADIUS.lg,
    borderWidth: 1,
    borderColor: COLORS.border,
    height: 56,
    paddingHorizontal: SPACING.md,
  },
  inputFocused: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.background,
  },
  inputError: {
    borderColor: COLORS.status.error,
  },
  iconWrapper: {
    marginRight: SPACING.sm,
  },
  input: {
    flex: 1,
    color: COLORS.text.primary,
    fontSize: 16,
    height: '100%',
  },
  errorText: {
    marginTop: SPACING.xs,
    marginLeft: SPACING.xs,
  },
});
