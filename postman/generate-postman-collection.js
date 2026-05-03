import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));

const collection = {
  info: {
    name: 'AI Violence Detection System',
    description: 'Laravel dashboard API and local Python inference service endpoints.',
    schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
  },
  variable: [
    { key: 'laravel_url', value: 'http://127.0.0.1:8000' },
    { key: 'weapon_service_url', value: 'http://127.0.0.1:5000' },
    { key: 'violence_service_url', value: 'http://127.0.0.1:5001' },
    { key: 'inference_token', value: '' },
  ],
  item: [
    {
      name: 'Laravel App',
      item: [
        {
          name: 'Health Check',
          request: {
            method: 'GET',
            url: '{{laravel_url}}/up',
          },
        },
        {
          name: 'List Incidents',
          request: {
            method: 'GET',
            header: [{ key: 'Accept', value: 'application/json' }],
            url: '{{laravel_url}}/api/incidents',
          },
        },
        {
          name: 'Create Weapon Incident',
          request: {
            method: 'POST',
            header: [
              { key: 'Accept', value: 'application/json' },
              { key: 'Content-Type', value: 'application/json' },
              { key: 'X-Inference-Token', value: '{{inference_token}}' },
            ],
            body: {
              mode: 'raw',
              raw: JSON.stringify({
                camera_id: 'LAPTOP_CAM',
                district: 'Local Test',
                event_type: 'Weapon Detected',
                confidence: 0.91,
                weapon_detected: true,
                alert_level: 'critical',
                timestamp: '2026-05-04T00:20:00',
                snapshot_url: '/storage/incidents/snapshots/example_weapon.jpg',
                clip_path: '/storage/incidents/videos/example_weapon.mp4',
              }, null, 2),
            },
            url: '{{laravel_url}}/api/incidents',
          },
        },
        {
          name: 'Create Violence Incident',
          request: {
            method: 'POST',
            header: [
              { key: 'Accept', value: 'application/json' },
              { key: 'Content-Type', value: 'application/json' },
              { key: 'X-Inference-Token', value: '{{inference_token}}' },
            ],
            body: {
              mode: 'raw',
              raw: JSON.stringify({
                camera_id: 'LAPTOP_CAM',
                district: 'Local Test',
                event_type: 'Violence Detected',
                confidence: 0.88,
                violence_score: 0.88,
                weapon_detected: false,
                alert_level: 'high',
                timestamp: '2026-05-04T00:25:00',
                snapshot_url: '/storage/incidents/snapshots/example_violence.jpg',
                clip_path: '/storage/incidents/videos/example_violence.mp4',
              }, null, 2),
            },
            url: '{{laravel_url}}/api/incidents',
          },
        },
      ],
    },
    {
      name: 'Weapon Detection Service',
      item: [
        { name: 'Status', request: { method: 'GET', url: '{{weapon_service_url}}/status' } },
        { name: 'Stream', request: { method: 'GET', url: '{{weapon_service_url}}/stream' } },
        { name: 'Start AI', request: { method: 'POST', url: '{{weapon_service_url}}/start' } },
        { name: 'Stop AI', request: { method: 'POST', url: '{{weapon_service_url}}/stop' } },
      ],
    },
    {
      name: 'Violence Detection Service',
      item: [
        { name: 'Status', request: { method: 'GET', url: '{{violence_service_url}}/status' } },
        { name: 'Stream', request: { method: 'GET', url: '{{violence_service_url}}/stream' } },
        { name: 'Start AI', request: { method: 'POST', url: '{{violence_service_url}}/start' } },
        { name: 'Stop AI', request: { method: 'POST', url: '{{violence_service_url}}/stop' } },
      ],
    },
  ],
};

writeFileSync(
  join(root, 'AI-Violence-Detection-System.postman_collection.json'),
  `${JSON.stringify(collection, null, 2)}\n`,
);

console.log('Wrote postman/AI-Violence-Detection-System.postman_collection.json');
