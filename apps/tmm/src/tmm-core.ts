/* src/tmm-core.ts — PHP SetTM / Matrix / Reflect 1:1 변환 */

export interface Layer { d: number; n: number; k: number }

type C = { re: number; im: number };
const C = (re = 0, im = 0): C => ({ re, im });
const add = (a: C, b: C) => C(a.re + b.re, a.im + b.im);
const sub = (a: C, b: C) => C(a.re - b.re, a.im - b.im);
const mul = (a: C, b: C) =>
  C(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);

function tm(u: Layer, d: Layer, λ: number) {
  const k0 = 2 * Math.PI / λ;
  const n1 = u.n * k0, k1 = u.k * k0;
  const n2 = d.n * k0, k2 = d.k * k0;
  const x  = d.d;

  const emp = Math.exp((-k1 + k2) * x);
  const epp = Math.exp((+k1 + k2) * x);
  const emm = Math.exp((-k1 - k2) * x);
  const epm = Math.exp((+k1 - k2) * x);

  const nabs2 = 2 * (n2 * n2 + k2 * k2);
  const ap = ((n2 + n1) * n2 + (k2 + k1) * k2) / nabs2;
  const am = ((n2 - n1) * n2 + (k2 - k1) * k2) / nabs2;
  const bp = ((n2 + n1) * k2 - (k2 + k1) * n2) / nabs2;
  const bm = ((n2 - n1) * k2 - (k2 - k1) * n2) / nabs2;

  const c = (w: number) => Math.cos(w * x);
  const s = (w: number) => Math.sin(w * x);

  /* PHP q[0]..q[7] */
  const q: C[] = [
    C(emp * (ap * c(n1 - n2) + bp * s(n1 - n2))),
    C(emp * (ap * s(n1 - n2) - bp * c(n1 - n2))),
    C(epp * (am * c(-n1 - n2) + bm * s(-n1 - n2))),
    C(epp * (am * s(-n1 - n2) - bm * c(-n1 - n2))),
    C(emm * (am * c(+n1 + n2) + bm * s(+n1 + n2))),
    C(emm * (am * s(+n1 + n2) - bm * c(+n1 + n2))),
    C(epm * (ap * c(-n1 + n2) + bp * s(-n1 + n2))),
    C(epm * (ap * s(-n1 + n2) - bp * c(-n1 + n2))),
  ];

  return [
    [q[0], q[2]],
    [q[4], q[6]],
  ] as [[C, C], [C, C]];
}

const mmul = (A: [[C, C], [C, C]], B: [[C, C], [C, C]]) => {
  const R: [[C, C], [C, C]] = [
    [C(), C()],
    [C(), C()],
  ];
  for (let i = 0; i < 2; ++i)
    for (let j = 0; j < 2; ++j)
      for (let k = 0; k < 2; ++k)
        R[i][j] = add(R[i][j], mul(A[i][k], B[k][j]));
  return R;
};

export function spectrum(
  layersIn: Layer[], λ0 = 390, λ1 = 830, step = 1
) {
  const air: Layer = { d: 0, n: 1, k: 0 };

  /* PHP : top-air + user-layers + bottom-air */
  const layers = [air, ...layersIn];
  const lastDepth = layersIn.length ? layersIn.at(-1)!.d : 0;
  layers.push({ d: lastDepth, n: 1, k: 0 });

  const λs: number[] = [], R: number[] = [], T: number[] = [];

  for (let λ = λ0; λ <= λ1; λ += step) {
    let F: [[C, C], [C, C]] = [
      [C(1), C()],
      [C(), C(1)],
    ];
    for (let i = 1; i < layers.length; ++i)
      F = mmul(tm(layers[i - 1], layers[i], λ), F);

    /* r = –fm[1,0]/fm[1,1] (PHP 부호 관례) */
    const a = F[1][0], b = F[1][1];
    const den = b.re * b.re + b.im * b.im;
    const r = C(
      -(a.re * b.re + a.im * b.im) / den,
      -(a.im * b.re - a.re * b.im) / den
    );

    /* t = fm[0,0] + fm[0,1] * r */
    const t = add(F[0][0], mul(F[0][1], r));

    const rv = r.re ** 2 + r.im ** 2;
    const tv = (layers.at(-1)!.n / air.n) * (t.re ** 2 + t.im ** 2);

    λs.push(λ); R.push(rv); T.push(tv);
  }
  return { λs, R, T };
}
