import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

export const Transfers = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Asset allocation & Transfer</h1>
          <p className="text-md-on-surface-variant mt-1 text-lg">(The double-allocation block in action)</p>
        </div>
      </div>

      <Card className="border border-md-outline/10 p-8 relative overflow-hidden">
        {/* Glow effect */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-md-primary/5 rounded-full blur-3xl" />
        
        <h2 className="text-xl font-bold mb-6 relative z-10">Transfer Request</h2>
        
        <div className="space-y-6 relative z-10">
          <Input 
            label="Asset"
            defaultValue="AF-0124 - Dell laptop"
            readOnly
          />

          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 flex items-start gap-3">
            <div className="w-5 h-5 rounded-full bg-red-500/20 text-red-600 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">!</div>
            <div>
              <p className="text-red-800 font-medium text-sm">Already allocated to Priya Shah (Engineering)</p>
              <p className="text-red-700/80 text-xs mt-1">Direct re-allocation is blocked - submit a transfer request below.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-end">
            <Input 
              label="From"
              defaultValue="Priya Shah"
              readOnly
            />
            
            <div className="flex flex-col w-full relative">
              <label className="text-xs font-medium text-md-on-surface-variant mb-1 ml-4">To</label>
              <select className="h-14 px-4 bg-md-surface-container-low text-md-on-surface rounded-t-lg rounded-b-none border-b-2 border-md-outline focus:outline-none focus:border-md-primary transition-colors duration-200">
                <option>Select Employee...</option>
                <option>Rohan Mehta</option>
                <option>Samir Iqbal</option>
              </select>
            </div>
          </div>

          <div className="flex flex-col w-full relative">
            <label className="text-xs font-medium text-md-on-surface-variant mb-1 ml-4">Reason</label>
            <textarea 
              rows={3}
              className="px-4 py-3 bg-md-surface-container-low text-md-on-surface placeholder:text-md-on-surface-variant/50 rounded-t-lg rounded-b-none border-b-2 border-md-outline focus:outline-none focus:border-md-primary transition-colors duration-200 resize-none"
            ></textarea>
          </div>

          <div className="pt-2">
            <Button variant="filled">Submit Request</Button>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-md-outline/10 relative z-10">
          <h3 className="font-medium text-md-on-surface mb-4">Allocation History</h3>
          <ul className="space-y-4 text-sm">
            <li className="flex gap-4">
              <span className="text-md-on-surface-variant w-16 shrink-0 font-medium">Apr 12</span>
              <span className="text-md-on-surface">Allocated to Priya Shah - Engineering</span>
            </li>
            <li className="flex gap-4">
              <span className="text-md-on-surface-variant w-16 shrink-0 font-medium">Jan 24</span>
              <span className="text-md-on-surface">Returned by Arjun Das - Condition: good</span>
            </li>
          </ul>
        </div>
      </Card>
    </div>
  );
};
