import React from 'react';
import { Loader } from '../../components/ui/Loader';

/**
 * @file LoadingScreen.tsx
 * @description Tela de transição para o processo de hidratação da sessão.
 * Utiliza o componente Loader do Design System.
 */
export default function LoadingScreen() {
  return <Loader fullScreen />;
}
