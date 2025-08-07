import { useCallback } from "react";
import { Slider, InputNumber, Stack } from "rsuite";

const validateInput = (value, min, max) => {
    if (isNaN(value) || !isFinite(value)) return false;
    if (min !== undefined && value < min) return false;
    if (max !== undefined && value > max) return false;
    return true;
  };
  
export default function InputNumberWithLabel({ 
    label, 
    value, 
    onChange, 
    min, 
    max, 
    step = 1,
    disabled = false 
  }) {
    const handleSliderChange = useCallback((newValue) => {
      onChange(Number(newValue));
    }, [onChange]);

    const handleInputChange = useCallback((newValue) => {
      if (validateInput(Number(newValue), min, max)) {
        onChange(Number(newValue));
      }
    }, [onChange, min, max]);
  
    return (
      <div style={{ width: 260 }}>
        <label 
          htmlFor={`${label}-input`}
          style={{ 
            display: 'block',
            fontSize: '0.75rem',
            fontWeight: 600,
            color: '#2c3e50',
            marginBottom: 4,
            lineHeight: 1.1
          }}
        >
          {label}
        </label>
        <Stack spacing={8} alignItems="center" style={{ marginTop: 1 }}>
          <Slider
            value={value}
            onChange={handleSliderChange}
            min={min}
            max={max}
            step={step}
            disabled={disabled}
            style={{ 
              flex: 1, 
              minWidth: 140,
              height: 4
            }}
            aria-labelledby={`${label}-label`}
          />
          <InputNumber 
            id={`${label}-input`}
            value={value}
            onChange={handleInputChange}
            min={min}
            max={max}
            step={step}
            disabled={disabled}
            style={{ 
              width: 80,
              borderRadius: 4,
              border: '1px solid #e1e8ed',
              fontSize: '0.8rem'
            }}
            aria-labelledby={`${label}-label`}
          />
        </Stack>
      </div>
    );
  }