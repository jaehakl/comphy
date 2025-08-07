import { useCallback } from "react";
import { InputNumber } from "rsuite";

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
    const handleChange = useCallback((newValue) => {
      if (validateInput(newValue, min, max)) {
        onChange(newValue);
      }
    }, [onChange, min, max]);
  
    return (
      <div>
        <small id={`${label}-label`}>{label}</small>
        <InputNumber 
          value={value}
          onChange={handleChange}
          min={min}
          max={max}
          step={step}
          disabled={disabled}
          style={{ width: 100 }}
          aria-labelledby={`${label}-label`}
        />
      </div>
    );
  }