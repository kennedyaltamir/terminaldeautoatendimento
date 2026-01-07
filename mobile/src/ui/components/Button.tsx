import React from 'react';
import { 
  TouchableOpacity, 
  Text, 
  StyleSheet, 
  ActivityIndicator, 
  TouchableOpacityProps 
} from 'react-native';
import { colors } from '../tokens/colors';
import { spacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

interface ButtonProps extends TouchableOpacityProps {
  title: string;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  title, 
  variant = 'primary', 
  isLoading, 
  disabled, 
  style, 
  ...props 
}) => {
  const isDanger = variant === 'danger';
  
  return (
    <TouchableOpacity
      activeOpacity={0.7}
      disabled={disabled || isLoading}
      style={[
        styles.base,
        styles[variant],
        disabled && styles.disabled,
        style
      ]}
      {...props}
    >
      {isLoading ? (
        <ActivityIndicator color={colors.text.primary} />
      ) : (
        <Text style={[
          styles.text, 
          variant === 'ghost' && styles.textGhost,
          isDanger && styles.textDanger
        ]}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  base: {
    height: 52,
    borderRadius: spacing.sm,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: spacing.xl,
    flexDirection: 'row',
  },
  primary: {
    backgroundColor: colors.primary,
  },
  secondary: {
    backgroundColor: colors.secondary,
  },
  danger: {
    backgroundColor: colors.status.danger,
  },
  ghost: {
    backgroundColor: colors.transparent,
    borderWidth: 1,
    borderColor: colors.border,
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    color: colors.text.primary,
    fontSize: typography.size.md,
    fontWeight: typography.weight.bold,
  },
  textGhost: {
    color: colors.text.secondary,
  },
  textDanger: {
    color: colors.text.primary,
  }
});
