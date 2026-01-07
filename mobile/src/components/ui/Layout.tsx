import React from 'react';
import { View, StyleSheet, ViewStyle, SafeAreaView } from 'react-native';
import { SPACING, COLORS } from '../../theme/tokens';

/**
 * @file Layout.tsx
 * @description Helpers utilitários para organização espacial e containers.
 */

interface StackProps {
  children: React.ReactNode;
  gap?: keyof typeof SPACING;
  horizontal?: boolean;
  style?: ViewStyle;
}

export const Stack = ({ children, gap = 'md', horizontal = false, style }: StackProps) => {
  const childrenArray = React.Children.toArray(children);
  
  return (
    <View style={[
      { flexDirection: horizontal ? 'row' : 'column' },
      style
    ]}>
      {childrenArray.map((child, index) => (
        <React.Fragment key={index}>
          {child}
          {index < childrenArray.length - 1 && (
            <View style={{ 
              height: horizontal ? 0 : SPACING[gap], 
              width: horizontal ? SPACING[gap] : 0 
            }} />
          )}
        </React.Fragment>
      ))}
    </View>
  );
};

export const Spacer = ({ size = 'md' }: { size?: keyof typeof SPACING }) => (
  <View style={{ height: SPACING[size], width: SPACING[size] }} />
);

export const Container = ({ children, style }: { children: React.ReactNode, style?: ViewStyle }) => (
  <SafeAreaView style={[styles.container, style]}>
    <View style={styles.inner}>
      {children}
    </View>
  </SafeAreaView>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  inner: {
    flex: 1,
    paddingHorizontal: SPACING.lg,
  },
});
