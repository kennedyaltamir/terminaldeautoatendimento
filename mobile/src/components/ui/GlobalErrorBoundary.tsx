
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { ErrorStateView } from './ErrorStateView';
import { logger } from '../../services/logger.service';

interface Props { children: ReactNode; }
interface State { hasError: boolean; }

export class GlobalErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false };

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    logger.error('CRASH_HANDLER', 'Erro de renderização capturado', {
      error: error.toString(),
      componentStack: errorInfo.componentStack,
    });
  }

  public render() {
    if (this.state.hasError) {
      return (
        <ErrorStateView 
          type="UNKNOWN" 
          message="Ocorreu um erro visual inesperado."
          onRetry={() => this.setState({ hasError: false })}
        />
      );
    }

    return this.props.children; // FIX: children reside em props
  }
}

