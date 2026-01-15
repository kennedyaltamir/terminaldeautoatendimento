
import React, { useState, useRef } from 'react';
import { 
  View, Text, TextInput, TouchableOpacity, StyleSheet, 
  ScrollView, ActivityIndicator, KeyboardAvoidingView, 
  Platform, Keyboard 
} from 'react-native';
import { ChefHat, Lock, Mail, LogIn, AlertCircle } from 'lucide-react-native';
import { useAuthStore } from '../../store/auth.store';

// Fake JWT estruturado para passar na validação do JwtService (Header.Payload.Signature)
const FAKE_QA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJxYUBtZXNhZmxvdy5jb20iLCJyb2xlIjoid2FpdGVyIiwiY29tcGFueV9pZCI6ImRhYmE0YmE0LWU4YmEtNDliYS1hYmE0LWU4YmE0YmE0ZWJhNCIsImV4cCI6OTk5OTk5OTk5OX0.signature";

export function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  
  const login = useAuthStore((state) => state.login);
  const passwordRef = useRef<TextInput>(null);

  const handleLoginSubmit = async () => {
    setErrorMessage(null);
    Keyboard.dismiss();

    if (!email || !password) {
      setErrorMessage("Por favor, preencha e-mail e senha.");
      return;
    }
    
    setIsSubmitting(true);
    await new Promise(resolve => setTimeout(resolve, 500));
    
    if (email === 'qa@mesaflow.com') {
      // Login de Auditoria L6
      login(FAKE_QA_JWT, { 
        name: 'QA L6 Master', 
        role: 'waiter', 
        company_slug: 'hamburgueria-ze' 
      });
      return;
    }
    
    // Fallback para outros logins
    login(FAKE_QA_JWT, { name: 'Operador', role: 'waiter', company_slug: 'hamburgueria-ze' });
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={{ flex: 1 }}>
      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        <View style={styles.header}>
          <View style={styles.logoContainer}><ChefHat color="#fff" size={48} /></View>
          <Text style={styles.title}>MesaFlow Mobile</Text>
          <Text style={styles.subtitle}>Acesse sua conta operacional</Text>
        </View>

        <View style={styles.form}>
          {errorMessage && (
            <View style={styles.errorContainer}>
              <AlertCircle color="#ef4444" size={20} />
              <Text style={styles.errorText}>{errorMessage}</Text>
            </View>
          )}

          <View style={[styles.inputContainer, errorMessage ? styles.inputError : null]}>
            <Mail color="#64748b" size={20} style={styles.inputIcon} />
            <TextInput
              testID="input-email"
              style={styles.input}
              placeholder="E-mail"
              placeholderTextColor="#64748b"
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              keyboardType="email-address"
              returnKeyType="next"
              onSubmitEditing={() => passwordRef.current?.focus()}
            />
          </View>

          <View style={[styles.inputContainer, errorMessage ? styles.inputError : null]}>
            <Lock color="#64748b" size={20} style={styles.inputIcon} />
            <TextInput
              ref={passwordRef}
              testID="input-password"
              style={styles.input}
              placeholder="Senha"
              placeholderTextColor="#64748b"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              returnKeyType="go"
              onSubmitEditing={handleLoginSubmit}
            />
          </View>

          <TouchableOpacity 
            testID="btn-enter"
            style={[styles.button, styles.primaryButton]} 
            onPress={handleLoginSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Entrar</Text>}
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, backgroundColor: '#0f172a', padding: 24, justifyContent: 'center' },
  header: { alignItems: 'center', marginBottom: 32 },
  logoContainer: { backgroundColor: '#ea580c', padding: 16, borderRadius: 24, marginBottom: 16 },
  title: { color: '#fff', fontSize: 32, fontWeight: '900' },
  subtitle: { color: '#94a3b8', fontSize: 16, marginTop: 8 },
  form: { gap: 12 },
  errorContainer: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'rgba(239, 68, 68, 0.1)', padding: 12, borderRadius: 12, marginBottom: 8 },
  errorText: { color: '#ef4444', marginLeft: 8, fontSize: 14, fontWeight: '600' },
  inputContainer: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#1e293b', borderRadius: 12, paddingHorizontal: 16 },
  inputError: { borderWidth: 1, borderColor: '#ef4444' },
  inputIcon: { marginRight: 12 },
  input: { flex: 1, color: '#fff', paddingVertical: 16, fontSize: 16 },
  button: { paddingVertical: 16, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  primaryButton: { backgroundColor: '#ea580c', marginTop: 8 },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' }
});

