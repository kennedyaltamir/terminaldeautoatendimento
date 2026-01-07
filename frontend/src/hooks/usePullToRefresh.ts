import { useEffect, useState, useRef } from 'react';

export function usePullToRefresh(onRefresh: () => Promise<void>) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [pullDistance, setPullDistance] = useState(0);
  const startY = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);

  const THRESHOLD = 80; // Distância para disparar o refresh

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleTouchStart = (e: TouchEvent) => {
      if (window.scrollY === 0) {
        startY.current = e.touches[0].clientY;
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      const y = e.touches[0].clientY;
      const diff = y - startY.current;

      if (window.scrollY === 0 && diff > 0) {
        // Adiciona resistência ao puxar
        setPullDistance(Math.min(diff * 0.5, 120)); 
        // Previne scroll nativo se estiver puxando para refresh
        if (diff < 200) e.preventDefault(); 
      }
    };

    const handleTouchEnd = async () => {
      if (pullDistance > THRESHOLD) {
        setIsRefreshing(true);
        setPullDistance(THRESHOLD); // Mantém o indicador visível
        try {
          await onRefresh();
        } finally {
          setIsRefreshing(false);
          setPullDistance(0);
        }
      } else {
        setPullDistance(0);
      }
    };

    container.addEventListener('touchstart', handleTouchStart, { passive: false });
    container.addEventListener('touchmove', handleTouchMove, { passive: false });
    container.addEventListener('touchend', handleTouchEnd);

    return () => {
      container.removeEventListener('touchstart', handleTouchStart);
      container.removeEventListener('touchmove', handleTouchMove);
      container.removeEventListener('touchend', handleTouchEnd);
    };
  }, [pullDistance, onRefresh]);

  return { isRefreshing, pullDistance, containerRef };
}
