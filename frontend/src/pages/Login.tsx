import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

export const Login = () => {
  return (
    <div className="min-h-screen bg-md-background flex items-center justify-center relative overflow-hidden p-6 selection:bg-md-primary/20 text-md-on-surface">
      {/* Organic blur shapes */}
      <div className="absolute top-[-10%] right-[-5%] w-[50vw] h-[50vw] rounded-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-md-secondary-container/40 to-transparent blur-3xl -z-10 opacity-70 pointer-events-none mix-blend-multiply" />
      <div className="absolute bottom-[-20%] left-[-10%] w-[60vw] h-[40vw] rounded-[100px] bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-md-tertiary/20 to-transparent blur-3xl -z-10 opacity-60 pointer-events-none mix-blend-multiply" />

      <Card className="w-full max-w-md p-10 elevated">
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-md-primary text-md-on-primary text-xl font-bold mb-6 shadow-md shadow-md-primary/20">
            AF
          </div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">AssetFlow</h1>
          <p className="text-md-on-surface-variant mt-2">Log in to manage your assets</p>
        </div>

        <form className="space-y-6">
          <Input 
            label="Email"
            type="email"
            placeholder="name@company.com" 
          />
          
          <div className="space-y-1">
            <Input 
              label="Password"
              type="password"
              placeholder="••••••••"
            />
            <div className="flex justify-end">
              <Button variant="text" size="sm" type="button" className="px-2">
                Forgot password?
              </Button>
            </div>
          </div>

          <div className="pt-4">
            <Button variant="filled" className="w-full h-12 text-base">
              Log In
            </Button>
          </div>
        </form>

        <div className="mt-10 bg-md-surface-container-low rounded-2xl p-6 text-center">
          <p className="text-sm font-medium text-md-on-surface mb-4">New here?</p>
          <p className="text-xs text-md-on-surface-variant mb-6 leading-relaxed">
            Sign up creates an employee account. Admin roles are assigned later by your organization administrator.
          </p>
          <Button variant="tonal" className="w-full">
            Create Account
          </Button>
        </div>
      </Card>
    </div>
  );
};
