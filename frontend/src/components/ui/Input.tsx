import React, { InputHTMLAttributes } from 'react';
import { cn } from './Button';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, ...props }, ref) => {
    return (
      <div className="flex flex-col w-full relative">
        {label && (
          <label className="text-xs font-medium text-md-on-surface-variant mb-1 ml-4">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={cn(
            "h-14 px-4 bg-md-surface-container-low text-md-on-surface placeholder:text-md-on-surface-variant/50",
            "rounded-t-lg rounded-b-none border-b-2 border-md-outline",
            "focus:outline-none focus:border-md-primary transition-colors duration-200",
            error && "border-red-500 focus:border-red-500",
            className
          )}
          {...props}
        />
        {error && (
          <span className="text-xs text-red-500 mt-1 ml-4">{error}</span>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";
