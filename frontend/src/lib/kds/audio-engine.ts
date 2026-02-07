/**
 * DOMAIN: INFRASTRUCTURE
 * OBJECTIVE: Singleton Audio Manager with Logging & Governance.
 * VERSION: 2.0 (Audited)
 */
import { kdsLogger } from './logger';

class KdsAudioEngine {
  private static instance: KdsAudioEngine;
  private sounds: Record<string, HTMLAudioElement> = {};
  private isMuted: boolean = false;
  private lastPlayed: number = 0;
  private DEBOUNCE_MS = 1000;

  private constructor() {
    if (typeof window !== 'undefined') {
      this.sounds = {
        new_order: new Audio('/sounds/new_order.mp3'),
        bump: new Audio('/sounds/bump.mp3'),
        alert: new Audio('/sounds/alert.mp3')
      };
      // Preload
      Object.values(this.sounds).forEach(s => s.load());
      
      const savedMute = localStorage.getItem('mesaflow_kds_muted');
      this.isMuted = savedMute === 'true';
    }
  }

  public static getInstance(): KdsAudioEngine {
    if (!KdsAudioEngine.instance) {
      KdsAudioEngine.instance = new KdsAudioEngine();
    }
    return KdsAudioEngine.instance;
  }

  public toggleMute() {
    this.isMuted = !this.isMuted;
    localStorage.setItem('mesaflow_kds_muted', String(this.isMuted));
    
    kdsLogger.log({
      domain: 'AUDIO',
      action: 'TOGGLE_MUTE',
      meta: { newState: this.isMuted ? 'MUTED' : 'ACTIVE' },
      severity: 'INFO'
    });

    return this.isMuted;
  }

  public getMuteState() {
    return this.isMuted;
  }

  public play(key: 'new_order' | 'bump' | 'alert') {
    if (this.isMuted) {
      kdsLogger.log({ domain: 'AUDIO', action: 'SKIP_PLAY', meta: { reason: 'MUTED', sound: key } });
      return;
    }
    
    const now = Date.now();
    if (now - this.lastPlayed < this.DEBOUNCE_MS) {
      kdsLogger.log({ domain: 'AUDIO', action: 'SKIP_PLAY', meta: { reason: 'DEBOUNCED', sound: key } });
      return;
    }

    const sound = this.sounds[key];
    if (sound) {
      sound.currentTime = 0;
      sound.play()
        .then(() => {
          kdsLogger.log({ domain: 'AUDIO', action: 'PLAY_SUCCESS', meta: { sound: key } });
        })
        .catch(e => {
          kdsLogger.log({ 
            domain: 'AUDIO', 
            action: 'PLAY_ERROR', 
            severity: 'WARN', 
            meta: { error: e.message, sound: key } 
          });
        });
      this.lastPlayed = now;
    }
  }
}

export const audioManager = KdsAudioEngine.getInstance();
 