import React, { useEffect } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import OrdersScreen from '../../screens/orders/OrdersScreen';
import WaiterTablesScreen from '../../screens/waiter/WaiterTablesScreen';
import OrderEntryScreen from '../../screens/waiter/OrderEntryScreen';
import OrderReviewScreen from '../../screens/waiter/OrderReviewScreen';
import WaiterCallsScreen from '../../screens/waiter/WaiterCallsScreen';
import PaymentScreen from '../../screens/waiter/PaymentScreen';
import PrinterDebugScreen from '../../screens/waiter/PrinterDebugScreen';
import { OrdersRealtimeService } from '../../services/orders.realtime.service';
import { OrdersSyncService } from '../../services/orders.sync.service';
import { WaiterSyncService } from '../../services/waiter.sync.service';
import { clockService } from '../../services/global.clock.service';
import { useOrdersStore } from '../../store/orders.store';
import { useWaiterStore, WaiterState } from '../../store/waiter.store';
import { useAuthStore } from '../../store/auth.store';
import { useSessionStore } from '../../store/session.store';
import { SessionBootstrapService } from '../../services/session.bootstrap.service';
import { colors } from '../../ui/tokens/colors';

const Stack = createNativeStackNavigator();

export const AppStack = () => {
  const authStatus = useAuthStore(state => state.status);
  const accessToken = useAuthStore(state => state.accessToken);
  const isSessionReady = useSessionStore(state => state.isReady);
  const userRole = useSessionStore(state => state.role);
  const slug = useSessionStore(state => state.slug);
  
  const updateSLAs = useOrdersStore(state => state.updateSLAs);
  const evaluateAlerts = useOrdersStore(state => state.evaluateAlerts);
  const handleRealtimeEvent = useOrdersStore(state => state.handleRealtimeEvent);
  const addServiceRequest = useWaiterStore((state: WaiterState) => state.addServiceRequest);

  useEffect(() => {
    if (authStatus === 'authenticated' && !isSessionReady) {
      SessionBootstrapService.run();
    }
  }, [authStatus, isSessionReady]);

  useEffect(() => {
    if (isSessionReady && slug && accessToken) {
      clockService.start();
      
      const unsubscribeClock = clockService.subscribe((ts) => {
        updateSLAs(ts);
        evaluateAlerts(ts);
        WaiterSyncService.processQueue();
      });

      OrdersRealtimeService.connect(
        slug, 
        accessToken, 
        (event) => {
          if (event.type === 'new_order') {
            OrdersSyncService.fetchAndAddOrder(slug, event.order_id);
          } else if (event.type === 'waiter_call') {
            addServiceRequest(event);
          } else {
            handleRealtimeEvent(event);
          }
        },
        () => {
          OrdersSyncService.performFullSync(slug);
        }
      );

      return () => {
        OrdersRealtimeService.disconnect();
        clockService.stop();
        unsubscribeClock();
      };
    }
  }, [isSessionReady, slug, accessToken, handleRealtimeEvent, updateSLAs, evaluateAlerts, addServiceRequest]);

  if (!isSessionReady) {
    return (
      <View style={styles.loader}>
        <ActivityIndicator color={colors.primary} size="large" />
      </View>
    );
  }

  const initialRoute = (userRole === 'kitchen') ? 'Orders' : 'WaiterTables';

  return (
    <Stack.Navigator 
      initialRouteName={initialRoute}
      screenOptions={{ headerShown: false }}
    >
      <Stack.Screen name="Orders" component={OrdersScreen} />
      <Stack.Screen name="WaiterTables" component={WaiterTablesScreen} />
      <Stack.Screen name="OrderEntry" component={OrderEntryScreen} />
      <Stack.Screen name="OrderReview" component={OrderReviewScreen} />
      <Stack.Screen name="WaiterCalls" component={WaiterCallsScreen} />
      <Stack.Screen name="Payment" component={PaymentScreen} />
      <Stack.Screen name="PrinterDebug" component={PrinterDebugScreen} />
    </Stack.Navigator>
  );
};

const styles = StyleSheet.create({
  loader: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background }
});
