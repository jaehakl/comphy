import { useState, useMemo, useCallback } from "react";
import { Button, Panel, Stack, Divider, Message } from "rsuite";
import "rsuite/dist/rsuite.min.css";
import Plot from "react-plotly.js";
import { spectrum } from './functions/tmm-core';
import InputNumberWithLabel from './components/inputNumberWithLabel';


/** ------------------ React UI ------------------ */
export default function App() {
  const [lambdaMin, setLambdaMin] = useState(390);
  const [lambdaMax, setLambdaMax] = useState(830);
  const [points, setPoints] = useState(441);
  const [layers, setLayers] = useState([
    { id: '1', d: 100, n: 2.0, k: 0.0 },
  ]);
  const [error, setError] = useState(null);

  // 입력값 검증
  const isValidInput = useMemo(() => {
    if (lambdaMin >= lambdaMax) return false;
    if (points < 3 || points > 10000) return false;
    if (lambdaMin < 20 || lambdaMax > 20000) return false;
    return layers.every(layer => 
      layer.d > 0 && layer.n > 0 && layer.k >= 0
    );
  }, [lambdaMin, lambdaMax, points, layers]);

  // 파장 배열 계산 (메모이제이션)
  const lambdaArr = useMemo(() => {
    if (!isValidInput) return new Float64Array(0);
    
    const arr = new Float64Array(points);
    const step = (lambdaMax - lambdaMin) / (points - 1);
    for (let i = 0; i < points; i++) arr[i] = lambdaMin + i * step;
    return arr;
  }, [lambdaMin, lambdaMax, points, isValidInput]);

  // 스펙트럼 계산 (메모이제이션)
  const spectrumResult = useMemo(() => {
    if (!isValidInput || lambdaArr.length === 0) {
      return { λs: [], R: [], T: [] };
    }
    
    try {
      setError(null);
      return spectrum(layers.map(({ d, n, k }) => ({ d, n, k })), lambdaMin, lambdaMax, points);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '계산 중 오류가 발생했습니다.';
      setError(errorMsg);
      return { λs: [], R: [], T: [] };
    }
  }, [layers, isValidInput, lambdaArr]);

  // 플롯 데이터 (메모이제이션)
  const plotData = useMemo(() => {
    if (spectrumResult.λs.length === 0) return [];
    
    return [
      { 
        x: Array.from(lambdaArr), 
        y: Array.from(spectrumResult.R), 
        name: "반사율 (R)", 
        type: "scatter",
        line: { color: '#ff6b6b' }
      },
      { 
        x: Array.from(lambdaArr), 
        y: Array.from(spectrumResult.T), 
        name: "투과율 (T)", 
        type: "scatter",
        line: { color: '#4ecdc4' }
      },
    ];
  }, [spectrumResult, lambdaArr]);

  const updateLayer = useCallback((idx, patch) => {
    setLayers(prev => {
      const next = [...prev];
      next[idx] = { ...next[idx], ...patch };
      return next;
    });
  }, []);

  const removeLayer = useCallback((idx) => {
    setLayers(prev => prev.filter((_, i) => i !== idx));
  }, []);

  const addLayer = useCallback(() => {
    const newId = (layers.length + 1).toString();
    setLayers(prev => [...prev, { id: newId, d: 100, n: 2.0, k: 0 }]);
  }, [layers.length]);

  return (
    <div style={{ padding: 24, maxWidth: 960, margin: "0 auto" }}>
      <h2>TMM-Play (Complex Q-Matrix)</h2>

      {error && (
        <Message type="error" style={{ marginBottom: 12 }}>
          {error}
        </Message>
      )}

      <Panel bordered header="스펙트럼 범위" style={{ marginTop: 12 }}>
        <Stack spacing={24} wrap>
          <InputNumberWithLabel 
            label="λ 최소값 (nm)" 
            value={lambdaMin} 
            onChange={setLambdaMin}
            min={20}
            max={lambdaMax - 1}
          />
          <InputNumberWithLabel 
            label="λ 최대값 (nm)" 
            value={lambdaMax} 
            onChange={setLambdaMax}
            min={lambdaMin + 1}
            max={20000}
          />
          <InputNumberWithLabel 
            label="포인트 수" 
            value={points} 
            onChange={setPoints} 
            min={3}
            max={10000}
          />
        </Stack>
      </Panel>

      <Panel bordered header="레이어 설정" style={{ marginTop: 12 }}>
        {layers.map((layer, idx) => (
          <Stack key={layer.id} spacing={12} alignItems="flex-end" style={{ marginBottom: 8 }}>
            <span>#{idx + 1}</span>
            <InputNumberWithLabel 
              label="두께 (nm)" 
              value={layer.d} 
              onChange={v => updateLayer(idx, { d: v })}
              min={0.1}
              step={0.1}
            />
            <InputNumberWithLabel 
              label="굴절률 (n)" 
              step={0.01} 
              value={layer.n} 
              onChange={v => updateLayer(idx, { n: v })}
              min={0.1}
            />
            <InputNumberWithLabel 
              label="흡수계수 (k)" 
              step={0.001} 
              value={layer.k} 
              onChange={v => updateLayer(idx, { k: v })}
              min={0}
            />
            {layers.length > 1 && (
              <Button 
                size="xs" 
                color="red" 
                onClick={() => removeLayer(idx)}
                aria-label={`레이어 ${idx + 1} 삭제`}
              >
                삭제
              </Button>
            )}
          </Stack>
        ))}
        <Button 
          appearance="ghost" 
          onClick={addLayer}
          aria-label="새 레이어 추가"
        >
          레이어 추가
        </Button>
      </Panel>

      <Panel bordered header="스펙트럼 결과" style={{ marginTop: 12 }}>
        {plotData.length > 0 ? (
          <Plot 
            data={plotData} 
            layout={{ 
              xaxis: { title: "파장 λ (nm)" }, 
              yaxis: { title: "반사율/투과율" }, 
              margin: { t: 10 },
              legend: { x: 0.02, y: 0.98 }
            }} 
            style={{ width: "100%", height: 400 }} 
            config={{ displayModeBar: false }} 
          />
        ) : (
          <div style={{ textAlign: 'center', padding: 40, color: '#666' }}>
            유효한 입력값을 설정하면 스펙트럼이 표시됩니다.
          </div>
        )}
      </Panel>

      <Divider>
        기존 Python 구현을 기반으로 한 Complex Q-Matrix 알고리즘
      </Divider>
    </div>
  );
}