// DOMAIN: REALTIME
// LAST_MODIFIED: 2026-01-15 16:10:00
import ws from 'k6/ws';
import { check } from 'k6';

export let options = { vus: 10, duration: '30s' };

export default function () {
    const url = 'ws://localhost:8000/ws/hamburgueria-ze';
    ws.connect(url, null, function (socket) {
        socket.on('message', (msg) => {
            const data = JSON.parse(msg);
            if (data.type === 'delivery.location') {
                check(data, { 'is v2': (d) => d.v === 2, 'has eta': (d) => d.payload.eta_seconds > 0 });
            }
        });
        socket.setTimeout(() => socket.close(), 5000);
    });
}

