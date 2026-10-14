import http from 'k6/http';
import { check } from 'k6';

const rate = Number(__ENV.RATE || 50);
export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-arrival-rate',
      rate,
      timeUnit: '1s',
      duration: __ENV.DURATION || '30s',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
    http_req_duration: ['p(95)<300'],
    dropped_iterations: ['count==0'],
  },
};
export default function () {
  const id = 1 + Math.floor(Math.random() * 10000);
  const response = http.get(`${__ENV.BASE_URL || 'http://localhost:8000'}/events/${id}`);
  check(response, {
    'status 200': r => r.status === 200,
    'correct event': r => {
      try { return r.json('id') === id; } catch (_) { return false; }
    },
  });
}
