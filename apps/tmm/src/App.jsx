import { useState, useMemo, useCallback } from "react";
import { Button, Panel, Stack, Divider, Message } from "rsuite";
import "rsuite/dist/rsuite.min.css";
import Plot from "react-plotly.js";
import { spectrum } from './functions/tmm-core';
import InputNumberWithLabel from './components/inputNumberWithLabel';

const LAMBDA_MIN = 100;
const LAMBDA_MAX = 2000;
const POINTS = 441;
const THICK_MIN = 0;
const THICK_MAX = 2000;
const INDEX_MIN = 1.0;
const INDEX_MAX = 5.0;
const ABSORPTION_MIN = 0;
const ABSORPTION_MAX = 0.1;


/** ------------------ React UI ------------------ */
export default function App() {
  const [lambdaMin, setLambdaMin] = useState(LAMBDA_MIN);
  const [lambdaMax, setLambdaMax] = useState(LAMBDA_MAX);
  const [points, setPoints] = useState(POINTS);
  const [layers, setLayers] = useState([
      { id: '1', d: 300, n: 2.0, k: 0.01 },
  ]);
  const [error, setError] = useState(null);

  // 입력값 검증
  const isValidInput = useMemo(() => {
    if (lambdaMin >= lambdaMax) return false;
    if (points < 3 || points > 1000) return false;
    if (lambdaMin < LAMBDA_MIN || lambdaMax > LAMBDA_MAX) return false;
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
    <div style={{ 
      padding: 32, 
      maxWidth: 1200, 
      margin: "0 auto", 
      backgroundColor: '#f8f9fa',
      minHeight: '100vh'
    }}>
      <div style={{ 
        backgroundColor: 'white', 
        borderRadius: 12, 
        padding: 32, 
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        marginBottom: 24
      }}>
        <h1 style={{ 
          margin: '0 0 8px 0', 
          color: '#2c3e50', 
          fontSize: '2.2rem',
          fontWeight: 600
        }}>
          TMM JS
        </h1>
        <p style={{ 
          margin: 0, 
          color: '#7f8c8d', 
          fontSize: '1rem',
          fontStyle: 'italic'
        }}>
          Transfer Matrix Method Calculator
        </p>
      </div>

      {error && (
        <Message type="error" style={{ 
          marginBottom: 16, 
          borderRadius: 8,
          fontSize: '0.95rem'
        }}>
          {error}
        </Message>
      )}

      <Panel 
        bordered 
        header={
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 8,
            fontSize: '1.1rem',
            fontWeight: 600,
            color: '#2c3e50'
          }}>
            <span>📊</span>
            스펙트럼 범위 설정
          </div>
        } 
        style={{ 
          marginBottom: 24,
          borderRadius: 8,
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)'
        }}
      >
        <Stack spacing={32} wrap style={{ padding: '8px 0' }}>
          <InputNumberWithLabel 
            label="λ 최소값 (nm)" 
            value={lambdaMin} 
            onChange={setLambdaMin}
            min={LAMBDA_MIN}
            max={lambdaMax - 1}
          />
          <InputNumberWithLabel 
            label="λ 최대값 (nm)" 
            value={lambdaMax} 
            onChange={setLambdaMax}
            min={lambdaMin + 1}
            max={LAMBDA_MAX}
          />
          <InputNumberWithLabel 
            label="포인트 수" 
            value={points} 
            onChange={setPoints} 
            min={3}
            max={POINTS}
          />
        </Stack>
      </Panel>

      <Panel 
        bordered 
        header={
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 8,
            fontSize: '1.1rem',
            fontWeight: 600,
            color: '#2c3e50'
          }}>
            <span>🔬</span>
            레이어 설정
          </div>
        } 
        style={{ 
          marginBottom: 24,
          borderRadius: 8,
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)'
        }}
      >
                 {layers.map((layer, idx) => (
           <div key={layer.id} style={{ 
             marginBottom: 8, 
             padding: 8, 
             border: '1px solid #e1e8ed', 
             borderRadius: 6,
             backgroundColor: '#fafbfc',
             transition: 'all 0.2s ease',
             ':hover': {
               borderColor: '#3498db',
               boxShadow: '0 2px 8px rgba(52, 152, 219, 0.1)'
             }
           }}>
             <Stack spacing={12} alignItems="center" wrap>
               <div style={{
                 width: 18,
                 height: 18,
                 borderRadius: '50%',
                 backgroundColor: '#3498db',
                 color: 'white',
                 display: 'flex',
                 alignItems: 'center',
                 justifyContent: 'center',
                 fontSize: '0.65rem',
                 fontWeight: 600,
                 flexShrink: 0
               }}>
                 {idx + 1}
               </div>
               <InputNumberWithLabel 
                 label="두께 (nm)" 
                 value={layer.d} 
                 onChange={v => updateLayer(idx, { d: v })}
                 min={THICK_MIN}
                 max={THICK_MAX}
                 step={0.1}
               />
               <InputNumberWithLabel 
                 label="굴절률 (n)" 
                 step={0.01} 
                 value={layer.n} 
                 onChange={v => updateLayer(idx, { n: v })}
                 min={INDEX_MIN}
                 max={INDEX_MAX}
               />
               <InputNumberWithLabel 
                 label="흡수계수 (k)" 
                 step={0.001} 
                 value={layer.k} 
                 onChange={v => updateLayer(idx, { k: v })}
                 min={ABSORPTION_MIN}
                 max={ABSORPTION_MAX}
               />
               {layers.length > 1 && (
                 <Button 
                   size="xs" 
                   color="red" 
                   onClick={() => removeLayer(idx)}
                   aria-label={`레이어 ${idx + 1} 삭제`}
                   style={{ 
                     minWidth: 60,
                     borderRadius: 4,
                     fontWeight: 500,
                     padding: '4px 8px',
                     fontSize: '0.75rem'
                   }}
                 >
                   🗑️
                 </Button>
               )}
             </Stack>
          </div>
        ))}
        <Button 
          appearance="ghost" 
          onClick={addLayer}
          aria-label="새 레이어 추가"
          style={{
            borderRadius: 8,
            padding: '8px 16px',
            fontWeight: 500,
            color: '#3498db',
            border: '2px dashed #3498db',
            backgroundColor: 'transparent',
            transition: 'all 0.2s ease'
          }}
        >
          ➕ 새 레이어 추가
        </Button>
      </Panel>

      <Panel 
        bordered 
        header={
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 8,
            fontSize: '1.1rem',
            fontWeight: 600,
            color: '#2c3e50'
          }}>
            <span>📈</span>
            스펙트럼 결과
          </div>
        } 
        style={{ 
          borderRadius: 8,
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)'
        }}
      >
        {plotData.length > 0 ? (
          <div style={{ padding: '8px 0' }}>
            <Plot 
              data={plotData} 
              layout={{ 
                xaxis: { 
                  title: "파장 λ (nm)",
                  gridcolor: '#ecf0f1',
                  zerolinecolor: '#bdc3c7'
                }, 
                yaxis: { 
                  title: "반사율/투과율",
                  gridcolor: '#ecf0f1',
                  zerolinecolor: '#bdc3c7'
                }, 
                margin: { t: 20, r: 20, b: 60, l: 60 },
                legend: { 
                  x: 0.02, 
                  y: 0.98,
                  bgcolor: 'rgba(255, 255, 255, 0.8)',
                  bordercolor: '#ecf0f1'
                },
                plot_bgcolor: '#ffffff',
                paper_bgcolor: '#ffffff'
              }} 
              style={{ width: "100%", height: 450 }} 
              config={{ 
                displayModeBar: false,
                responsive: true
              }} 
            />
          </div>
        ) : (
          <div style={{ 
            textAlign: 'center', 
            padding: 60, 
            color: '#7f8c8d',
            fontSize: '1.1rem'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: 16 }}>📊</div>
            유효한 입력값을 설정하면 스펙트럼이 표시됩니다.
          </div>
        )}
      </Panel>

      <div style={{ 
        textAlign: 'center', 
        marginTop: 32, 
        padding: 24,
        color: '#7f8c8d',
        fontSize: '0.9rem',
        borderTop: '1px solid #ecf0f1'
      }}>
        <p style={{ margin: 0 }}>
          기존 Python 구현을 기반으로 한 Complex Q-Matrix 알고리즘
        </p>
      </div>
    </div>
  );
}