import React, { ButtonHTMLAttributes } from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'filled' | 'tonal' | 'outlined' | 'text' | 'fab';
  size?: 'sm' | 'md' | 'lg' | 'icon';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'filled', size = 'md', children, ...props }, ref) => {
    
    const variants = {
      filled: "bg-md-primary text-md-on-primary hover:bg-md-primary/90 active:bg-md-primary/80 shadow-sm hover:shadow-md",
      tonal: "bg-md-secondary-container text-md-on-secondary-container hover:bg-md-secondary-container/90 active:bg-md-secondary-container/80 shadow-sm hover:shadow-md",
      outlined: "bg-transparent border border-md-outline text-md-primary hover:bg-md-primary/5 active:bg-md-primary/10",
      text: "bg-transparent text-md-primary hover:bg-md-primary/10 active:bg-md-primary/20",
      fab: "bg-md-tertiary text-white shadow-md hover:shadow-xl rounded-2xl w-14 h-14 p-0 flex items-center justify-center hover:scale-105"
    };

    const sizes = {
      sm: "h-9 px-4 text-sm",
      md: "h-10 px-6 text-sm",
      lg: "h-12 px-8 text-base",
      icon: "w-10 h-10 p-2 flex items-center justify-center"
    };

    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center font-medium transition-all duration-300 ease-md-emphasized active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-md-primary focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
          variant !== 'fab' && "rounded-full",
          variant !== 'fab' && sizes[size],
          variants[variant],
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
