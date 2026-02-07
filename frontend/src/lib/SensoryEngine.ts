import { toast } from 'sonner';

class SensoryEngine {
    private audioQueue: string[] = [];
    private isPlaying = false;

    public vibrate(type: 'SUCCESS' | 'ERROR' | 'INCIDENT' | 'CLICK') {
        if (typeof navigator === 'undefined' || !navigator.vibrate) return;
        const patterns = {
            SUCCESS: [10],
            ERROR: [50, 50, 50],
            INCIDENT: [200, 100, 200, 100, 200],
            CLICK: [5]
        };
        navigator.vibrate(patterns[type]);
        console.info(`[SENSORY_HAPTIC] Pattern: ${type}`);
    }

    public play(sound: 'success' | 'error' | 'alert' | 'new_order') {
        this.audioQueue.push(sound);
        this.processQueue();
    }

    private async processQueue() {
        if (this.isPlaying || this.audioQueue.length === 0) return;
        this.isPlaying = true;
        const sound = this.audioQueue.shift();
        const audio = new Audio(`/sounds/${sound}.mp3`);
        try {
            await audio.play();
            console.info(`[SENSORY_AUDIO] Playing: ${sound}`);
            audio.onended = () => {
                setTimeout(() => {
                    this.isPlaying = false;
                    this.processQueue();
                }, 500);
            };
        } catch (e) {
            this.isPlaying = false;
            this.processQueue();
        }
    }

    public notify(msg: string, type: 'success' | 'error' | 'info' = 'info') {
        toast[type](msg);
        this.vibrate(type === 'success' ? 'SUCCESS' : 'ERROR');
    }
}

export const sensory = new SensoryEngine();
