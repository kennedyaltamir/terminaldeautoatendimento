import React from 'react';
import { View, StyleSheet, ViewProps } from 'react-native';
import { colors } from '../tokens/colors';
import { spacing } from '../tokens/spacing';

interface CardProps extends ViewProps {
  children: React.ReactNode;
  variant?: 'default' | 'outline';
}

export const Card: React.FC<CardProps> = ({ children, style, variant = 'default', ...props }) => {
  return (
    <View 
      style={[
        styles.base, 
        variant === 'outline' ? styles.outline : styles.default, 
        style
      ]} 
      {...props}
    >
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  base: {
    borderRadius: spacing.md,
    padding: spacing.lg,
  },
  default: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
  },
  outline: {
    backgroundColor: colors.transparent,
    borderWidth: 1,
    borderColor: colors.border,
  }
});
