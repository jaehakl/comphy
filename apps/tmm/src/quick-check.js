// src/quick-check.ts ― CI 없이도 터지면 바로 알림
import { spectrum } from './functions/tmm-core.js';

const sanity = [
  {
    name: 'Air only',
    stack: [],
    λ: 550,
    expectR: 0,
    expectT: 1,
    tol: 1e-6,
  },
  {
    name: 'SiO₂(500 nm)/Si',
    stack: [
      { d: 500, n: 1.45, k: 0 },
      { d:   0, n: 3.9,  k: 0.02 },
    ],
    λ: 550,
    expectR: 0.10681540250900184,
    tol: 1e-3,
  },
];

let fail = false;
for (const t of sanity) {
  const { R, T } = spectrum(t.stack, t.λ, t.λ, 1);
  const err = Math.abs(R[0] - t.expectR);
  if (err > t.tol || Math.abs(R[0] + T[0] - 1) > 1e-3) {
    // eslint-disable-next-line no-console
    console.error(`❌ ${t.name} failed: R=${R[0]}, T=${T[0]}`);
    fail = true;
  }
}
if (fail) process.exit(1);
console.log('✅ quick-check passed.');
