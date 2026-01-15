import React from 'react';
import { View, Text } from 'react-native';
import { ErrorStateView } from '../src/components/ui/ErrorStateView';

export function UISweep() {
  console.log('🧪 UI SWEEP START');

  const types = ['403', '500', 'OFFLINE', 'TIMEOUT', 'UNKNOWN'] as const;

  return (
    <View>
      <Text>UI Sweep</Text>
      {types.map((type) => (
        <ErrorStateView
          key={type}
          type={type}
          message={`Teste visual ${type}`}
          onRetry={() => console.log(`retry ${type}`)}
        />
      ))}
    </View>
  );
}
