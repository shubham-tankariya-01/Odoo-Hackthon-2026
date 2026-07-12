import React, { HTMLAttributes } from 'react';
import { cn } from './Button';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  elevated?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, elevated = false, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "bg-md-surface-container rounded-[24px] p-6 transition-all duration-300 ease-md-emphasized shadow-sm hover:shadow-md",
          elevated && "shadow-md hover:shadow-lg hover:-translate-y-1",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";
