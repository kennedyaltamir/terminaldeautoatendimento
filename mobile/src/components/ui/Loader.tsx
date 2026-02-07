import React from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { COLORS } from '../../theme/tokens';

/**
 * @file Loader.tsx
 * @description Sinalizador de carregamento padronizado.
 */

interface LoaderProps {
  fullScreen?: boolean;
  size?: 'small' | 'large';
}

export const Loader = ({ fullScreen = false, size = 'large' }: LoaderProps) => {
  if (fullScreen) {
    return (
      <View style={styles.fullScreen}>
        <ActivityIndicator size={size} color={COLORS.primary} />
      </View>
    );
  }

  return (
    <View style={styles.inline}>
      <ActivityIndicator size={size} color={COLORS.primary} />
    </View>
  );
};

const styles = StyleSheet.create({
  fullScreen: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: COLORS.background,
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 999,
  },
  inline: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
