/**
 * DOMAIN: MOBILE
 * OBJECTIVE: Captura de erros nativos.
 * FIX: Consolidação de código e correção de imports para lucide-react-native.
 */
import React, { Component, ReactNode, ErrorInfo } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { AlertTriangle, RefreshCw } from "lucide-react-native";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class GlobalErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("🚨 [Mobile Crash]:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <View style={styles.container}>
          <View style={styles.iconContainer}>
            <AlertTriangle size={48} color="#ef4444" />
          </View>
          <Text style={styles.title}>Algo deu errado</Text>
          <Text style={styles.desc}>Ocorreu um erro inesperado no aplicativo.</Text>
          
          <TouchableOpacity 
            style={styles.button}
            onPress={() => this.setState({ hasError: false, error: null })}
          >
            <RefreshCw size={20} color="#FFF" />
            <Text style={styles.buttonText}>Tentar Novamente</Text>
          </TouchableOpacity>
        </View>
      );
    }

    return this.props.children;
  }
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#020617', 
    alignItems: 'center', 
    justifyContent: 'center', 
    padding: 20 
  },
  iconContainer: {
    backgroundColor: 'rgba(239, 68, 68, 0.1)',
    padding: 20,
    borderRadius: 30,
    marginBottom: 20
  },
  title: { 
    fontSize: 24, 
    fontWeight: '900', 
    color: '#FFF', 
    textAlign: 'center' 
  },
  desc: { 
    fontSize: 14, 
    color: '#94a3b8', 
    textAlign: 'center', 
    marginTop: 10, 
    marginBottom: 30 
  },
  button: { 
    backgroundColor: '#ea580c', 
    paddingVertical: 15, 
    paddingHorizontal: 30, 
    borderRadius: 12, 
    flexDirection: 'row', 
    alignItems: 'center', 
    gap: 10 
  },
  buttonText: { 
    color: '#FFF', 
    fontWeight: 'bold' 
  }
});