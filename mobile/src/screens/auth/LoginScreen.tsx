import React from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { ChefHat, Lock, Mail, ChevronRight } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';

export function LoginScreen() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const login = useAuthStore((state) => state.login);

  const handleLogin = (role: 'waiter' | 'kitchen' | 'driver' = 'waiter') => {
    // Simulação de login com seleção de cargo para facilitar seus testes
    login('fake-token', { 
      name: 'Kennedy', 
      role: role,
      company_slug: 'hamburgueria-ze'
    });
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <View style={styles.logoContainer}>
          <ChefHat color="#fff" size={48} />
        </View>
        <Text style={styles.title}>MesaFlow Mobile</Text>
        <Text style={styles.subtitle}>Acesse sua conta operacional</Text>
      </View>

      <View style={styles.form}>
        <View style={styles.inputContainer}>
          <Mail color="#64748b" size={20} style={styles.inputIcon} />
          <TextInput
            style={styles.input}
            placeholder="E-mail"
            placeholderTextColor="#64748b"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
          />
        </View>

        <View style={styles.inputContainer}>
          <Lock color="#64748b" size={20} style={styles.inputIcon} />
          <TextInput
            style={styles.input}
            placeholder="Senha"
            placeholderTextColor="#64748b"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
        </View>

        <Text style={styles.devNote}>Selecione um perfil para testar:</Text>
        
        <TouchableOpacity 
          style={[styles.button, { backgroundColor: '#ea580c' }]} 
          onPress={() => handleLogin('waiter')}
        >
          <Text style={styles.buttonText}>Entrar como Garçom</Text>
          <ChevronRight color="#fff" size={20} />
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.button, { backgroundColor: '#3b82f6' }]} 
          onPress={() => handleLogin('kitchen')}
        >
          <Text style={styles.buttonText}>Entrar como Cozinha</Text>
          <ChevronRight color="#fff" size={20} />
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.button, { backgroundColor: '#22c55e' }]} 
          onPress={() => handleLogin('driver')}
        >
          <Text style={styles.buttonText}>Entrar como Entregador</Text>
          <ChevronRight color="#fff" size={20} />
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, backgroundColor: '#0f172a', padding: 24, justifyContent: 'center' },
  header: { alignItems: 'center', marginBottom: 40 },
  logoContainer: { backgroundColor: '#ea580c', padding: 16, borderRadius: 24, marginBottom: 16 },
  title: { color: '#fff', fontSize: 32, fontWeight: '900' },
  subtitle: { color: '#94a3b8', fontSize: 16, marginTop: 8 },
  form: { gap: 12 },
  inputContainer: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#1e293b', borderRadius: 12, paddingHorizontal: 16 },
  inputIcon: { marginRight: 12 },
  input: { flex: 1, color: '#fff', paddingVertical: 16, fontSize: 16 },
  devNote: { color: '#64748b', fontSize: 12, fontWeight: 'bold', textTransform: 'uppercase', marginTop: 10, textAlign: 'center' },
  button: { 
    flexDirection: 'row',
    paddingVertical: 16, 
    paddingHorizontal: 20,
    borderRadius: 12, 
    alignItems: 'center', 
    justifyContent: 'space-between'
  },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' }
});
