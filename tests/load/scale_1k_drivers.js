// DOMAIN: LOAD_TEST
// LAST_MODIFIED: 2026-01-15 16:20:00
import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
    stages: [
        { duration: '1m', target: 1000 },
        { duration: '3m', target: 1000 },
        { duration: '1m', target: 0 },
    ],
    thresholds: { http_req_duration: ['p(95)<200'] },
};

export default function () {
    const params = { headers: { 'Authorization': 'Bearer TOKEN', 'Content-Type': 'application/json' } };
    http.post('http://localhost:8000/api/admin/delivery/orders/UUID/location', 
              JSON.stringify({ lat: -19.22, lng: -44.93 }), params);
    sleep(3); // Throttle simulation
}

