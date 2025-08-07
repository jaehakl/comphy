import { useState, useMemo } from "react";
import { Button, InputNumber, Panel, Stack, Divider } from "rsuite";
import "rsuite/dist/rsuite.min.css";
import Plot from "react-plotly.js";
import { spectrum } from './tmm-core';

/** ------------------ Complex helpers ------------------ */
function c(re, im = 0) { return { re, im }; }
const cAdd = (a, b) => c(a.re + b.re, a.im + b.im);
const cSub = (a, b) => c(a.re - b.re, a.im - b.im);
const cMul = (a, b) => c(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
const cDiv = (a, b) => {
  const denom = b.re * b.re + b.im * b.im;
  return c((a.re * b.re + a.im * b.im) / denom, (a.im * b.re - a.re * b.im) / denom);
};
const cAbs2 = a => a.re * a.re + a.im * a.im;
const cExpI = theta => c(Math.cos(theta), Math.sin(theta));

/** ------------------ Q-matrix based TMM (complex) ------------------
 * layers : [{d: nm, n: real, k: imag}, ...]        // incident medium omitted(air)
 * Substrate is assumed n=1.5, k=0
 */
function tmmComplex(layers, lambdaArr) {
  const R = new Float64Array(lambdaArr.length);
  const T = new Float64Array(lambdaArr.length);

  for (let idx = 0; idx < lambdaArr.length; idx++) {
    const λ = lambdaArr[idx];
    let fm = [c(1), c(0), c(0), c(1)]; // 2×2 identity, row-major
    let depth = 0;

    for (let i = 0; i < layers.length; i++) {
      const l1 = layers[i];
      const l2 = i < layers.length - 1 ? layers[i + 1] : { d: 0, n: 1, k: 0 }; // next or ambient
      const tm = getQ(l1, l2, λ, depth);
      fm = matMul(tm, fm);
      depth += (l2.d || 0);
    }

    const r = cDiv(fm[1], fm[3]); // fm[1,0]/fm[1,1]
    const t = cSub(fm[0], cMul(fm[2], r)); // fm[0,0] - fm[0,1]*r
    R[idx] = cAbs2(r);
    T[idx] = cAbs2(t);
  }
  return { R, T };
}

function getQ(layer1, layer2, λ_nm, depth_nm) {
  const k0 = 2 * Math.PI / λ_nm; // wave number in nm⁻¹
  const n1 = c(layer1.n, layer1.k);
  const n2 = c(layer2.n, layer2.k);
  const c1 = cMul(n1, c(k0)); // (n1)*k0
  const c2 = cMul(n2, c(k0));
  const depth = depth_nm; // already nm

  const exp1 = cExpI((c1.re - c2.re) * depth); // approx imag parts small for phase – acceptable for demo
  const exp2 = cExpI((-c2.re - c1.re) * depth);
  const exp3 = cExpI((c2.re + c1.re) * depth);
  const exp4 = cExpI((-c1.re + c2.re) * depth);

  const num1 = cAdd(c2, c1);
  const num2 = cSub(c2, c1);
  const denom = cMul(c(c2.re, c2.im), c(2)); // 2*c2

  const q00 = cMul(cDiv(num1, denom), exp1);
  const q01 = cMul(cDiv(num2, denom), exp2);
  const q10 = cMul(cDiv(num2, denom), exp3);
  const q11 = cMul(cDiv(num1, denom), exp4);

  return [q00, q01, q10, q11];
}

function matMul(a, b) { // 2×2 complex matrices, row-major arrays length 4
  return [
    cAdd(cMul(a[0], b[0]), cMul(a[1], b[2])),
    cAdd(cMul(a[0], b[1]), cMul(a[1], b[3])),
    cAdd(cMul(a[2], b[0]), cMul(a[3], b[2])),
    cAdd(cMul(a[2], b[1]), cMul(a[3], b[3])),
  ];
}

/** ------------------ React UI ------------------ */
export default function App() {
  const [lambdaMin, setLambdaMin] = useState(390);
  const [lambdaMax, setLambdaMax] = useState(830);
  const [points, setPoints] = useState(441);
  const [layers, setLayers] = useState([
    { d: 100, n: 2.0, k: 0.0 },
  ]);

  const lambdaArr = useMemo(() => {
    const arr = new Float64Array(points);
    const step = (lambdaMax - lambdaMin) / (points - 1);
    for (let i = 0; i < points; i++) arr[i] = lambdaMin + i * step; // nm
    return arr;
  }, [lambdaMin, lambdaMax, points]);

  const { λs, R, T } = spectrum(layers);   // 배열 그대로 Plotly

  const plotData = useMemo(() => ([
    { x: Array.from(lambdaArr), y: Array.from(R), name: "R", type: "scatter" },
    { x: Array.from(lambdaArr), y: Array.from(T), name: "T", type: "scatter" },
  ]), [R, T, lambdaArr]);

  return (
    <div style={{ padding: 24, maxWidth: 960, margin: "0 auto" }}>
      <h2>TMM-Play (Cplx Q-Matrix)</h2>

      <Panel bordered header="Spectral Range" style={{ marginTop: 12 }}>
        <Stack spacing={24} wrap>
          <InputNumberWithLabel label="λ min (nm)" value={lambdaMin} onChange={setLambdaMin} />
          <InputNumberWithLabel label="λ max (nm)" value={lambdaMax} onChange={setLambdaMax} />
          <InputNumberWithLabel label="Points" value={points} onChange={setPoints} min={3} />
        </Stack>
      </Panel>

      <Panel bordered header="Layers" style={{ marginTop: 12 }}>
        {layers.map((l, idx) => (
          <Stack key={idx} spacing={12} alignItems="flex-end" style={{ marginBottom: 8 }}>
            <span>#{idx + 1}</span>
            <InputNumberWithLabel label="d (nm)" value={l.d} onChange={v => updateLayer(idx, { d: v })} />
            <InputNumberWithLabel label="n" step={0.01} value={l.n} onChange={v => updateLayer(idx, { n: v })} />
            <InputNumberWithLabel label="k" step={0.001} value={l.k} onChange={v => updateLayer(idx, { k: v })} />
            {layers.length > 1 && <Button size="xs" color="red" onClick={() => removeLayer(idx)}>Del</Button>}
          </Stack>
        ))}
        <Button appearance="ghost" onClick={() => setLayers([...layers, { d: 100, n: 2.0, k: 0 }])}>Add Layer</Button>
      </Panel>

      <Panel bordered header="Spectra" style={{ marginTop: 12 }}>
        <Plot data={plotData} layout={{ xaxis: { title: "λ (nm)" }, yaxis: { title: "R / T" }, margin: { t: 10 } }} style={{ width: "100%", height: 400 }} config={{ displayModeBar: false }} />
      </Panel>

      <Divider>
        Complex Q-Matrix algo based on your legacy Python implementation
      </Divider>
    </div>
  );

  function updateLayer(idx, patch) {
    const next = [...layers];
    next[idx] = { ...next[idx], ...patch };
    setLayers(next);
  }
  function removeLayer(idx) {
    setLayers(layers.filter((_, i) => i !== idx));
  }
}

function InputNumberWithLabel({ label, ...props }) {
  return (
    <div>
      <small>{label}</small>
      <InputNumber {...props} style={{ width: 100 }} />
    </div>
  );
}