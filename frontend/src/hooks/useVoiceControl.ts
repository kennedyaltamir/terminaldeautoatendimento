"use client";

import { useState, useEffect, useCallback } from "react";
import { toast } from "sonner";

interface VoiceCommand {
  command: RegExp;
  action: (match: RegExpMatchArray) => void;
}

export function useVoiceControl(commands: VoiceCommand[]) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [isSupported, setIsSupported] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      // @ts-ignore
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        setIsSupported(true);
        const rec = new SpeechRecognition();
        rec.continuous = true;
        rec.interimResults = false;
        rec.lang = "pt-BR";

        rec.onresult = (event: any) => {
          const last = event.results.length - 1;
          const text = event.results[last][0].transcript.trim().toLowerCase();
          setTranscript(text);
          console.log("🎤 Voz detectada:", text);
          processCommand(text);
        };

        rec.onerror = (event: any) => {
          console.error("Erro no reconhecimento de voz:", event.error);
          if (event.error === 'not-allowed') {
            setIsListening(false);
            toast.error("Acesso ao microfone negado.");
          }
        };

        rec.onend = () => {
          // Reinicia se estiver ouvindo (Continuous loop)
          if (isListening) {
            try {
              rec.start();
            } catch (e) {
              // Ignora erro se já estiver iniciado
            }
          }
        };

        setRecognition(rec);
      }
    }
  }, [isListening]); // Dependência para recriar se necessário, mas idealmente estável

  const processCommand = (text: string) => {
    for (const cmd of commands) {
      const match = text.match(cmd.command);
      if (match) {
        console.log("✅ Comando reconhecido:", cmd.command);
        cmd.action(match);
        toast.success(`Comando de voz: ${text}`);
        return;
      }
    }
  };

  const toggleListening = useCallback(() => {
    if (!isSupported || !recognition) return;

    if (isListening) {
      recognition.stop();
      setIsListening(false);
      toast.info("Controle de voz pausado.");
    } else {
      try {
        recognition.start();
        setIsListening(true);
        toast.success("Ouvindo comandos de voz...");
      } catch (e) {
        console.error(e);
      }
    }
  }, [isListening, isSupported, recognition]);

  return {
    isListening,
    isSupported,
    transcript,
    toggleListening
  };
}
