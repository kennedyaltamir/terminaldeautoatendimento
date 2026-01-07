import React from 'react';
import { View, Text, TextInput, StyleSheet, TextInputProps } from 'react-native';
import { colors } from '../tokens/colors';
import { spacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, style, ...props }) => {
  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}
      <TextInput
        style={[
          styles.input,
          error ? styles.inputError : styles.inputDefault,
          style
        ]}
        placeholderTextColor={colors.text.muted}
        {...props}
      />
      {error && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginBottom: spacing.md,
  },
  label: {
    color: colors.text.secondary,
    fontSize: typography.size.sm,
    fontWeight: typography.weight.semibold,
    marginBottom: spacing.xs,
    marginLeft: spacing.xs,
  },
  input: {
    height: 52,
    borderRadius: spacing.sm,
    paddingHorizontal: spacing.md,
    fontSize: typography.size.md,
    color: colors.text.primary,
    backgroundColor: colors.surface,
    borderWidth: 1,
  },
  inputDefault: {
    borderColor: colors.border,
  },
  inputError: {
    borderColor: colors.status.danger,
  },
  errorText: {
    color: colors.status.danger,
    fontSize: typography.size.xs,
    marginTop: spacing.xs,
    marginLeft: spacing.xs,
  }
});
