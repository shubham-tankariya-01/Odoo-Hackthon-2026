import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const Reports = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Reports & Analytics</h1>
          <p className="text-md-on-surface-variant mt-1 text-lg">(Utilization, maintenance frequency, most-used/idle)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card elevated className="p-8 h-80 flex flex-col group relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-md-primary/10 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
          <h3 className="font-bold text-lg mb-6 relative z-10">Utilization by department</h3>
          <div className="flex-1 flex items-end gap-4 justify-between pt-4 relative z-10">
            {/* Mock Bar Chart */}
            {[40, 70, 45, 90, 60, 30].map((h, i) => (
              <div key={i} className="w-full bg-md-surface-container-low rounded-t-md flex flex-col justify-end group/bar cursor-pointer">
                <div 
                  className="w-full bg-md-primary/80 rounded-t-md group-hover/bar:bg-md-primary transition-all duration-300" 
                  style={{ height: `${h}%` }}
                />
              </div>
            ))}
          </div>
        </Card>

        <Card elevated className="p-8 h-80 flex flex-col group relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-md-tertiary/10 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
          <h3 className="font-bold text-lg mb-6 relative z-10">Maintenance Frequency</h3>
          <div className="flex-1 relative z-10 w-full h-full">
            {/* Mock Line Chart */}
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 100 100">
              <path d="M0,80 L20,60 L40,70 L60,30 L80,50 L100,20" fill="none" stroke="currentColor" strokeWidth="3" className="text-md-tertiary" />
              <circle cx="0" cy="80" r="3" className="fill-md-tertiary" />
              <circle cx="20" cy="60" r="3" className="fill-md-tertiary" />
              <circle cx="40" cy="70" r="3" className="fill-md-tertiary" />
              <circle cx="60" cy="30" r="3" className="fill-md-tertiary" />
              <circle cx="80" cy="50" r="3" className="fill-md-tertiary" />
              <circle cx="100" cy="20" r="3" className="fill-md-tertiary" />
            </svg>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="hover:shadow-md transition-shadow">
          <h3 className="font-bold text-lg mb-4 text-md-primary">Most-used assets</h3>
          <ul className="space-y-3 text-sm">
            <li className="flex justify-between border-b border-md-outline/10 pb-2">
              <span className="font-medium">Room 302</span>
              <span className="text-md-on-surface-variant">30 bookings this month</span>
            </li>
            <li className="flex justify-between border-b border-md-outline/10 pb-2">
              <span className="font-medium">Van AF-0112</span>
              <span className="text-md-on-surface-variant">25 trips this month</span>
            </li>
            <li className="flex justify-between">
              <span className="font-medium">Projector AF-0062</span>
              <span className="text-md-on-surface-variant">15 uses</span>
            </li>
          </ul>
        </Card>
        
        <Card className="hover:shadow-md transition-shadow">
          <h3 className="font-bold text-lg mb-4 text-amber-700">Idle assets</h3>
          <ul className="space-y-3 text-sm">
            <li className="flex justify-between border-b border-md-outline/10 pb-2">
              <span className="font-medium">Scanner AF-0041</span>
              <span className="text-md-on-surface-variant">unused 60+ days</span>
            </li>
            <li className="flex justify-between">
              <span className="font-medium">Chair AF-0470</span>
              <span className="text-md-on-surface-variant">unused 45 days</span>
            </li>
          </ul>
        </Card>
      </div>

      <Card className="bg-md-tertiary/10 border border-md-tertiary/20">
        <h3 className="font-bold text-lg mb-4 text-md-tertiary">Assets due for maintenance / nearing retirement</h3>
        <ul className="space-y-2 text-sm mb-6">
          <li className="font-medium">Forklift AF-0098 - service due in 3 weeks</li>
          <li className="font-medium">Laptop AF-0125 - 4 years old (nearing retirement)</li>
        </ul>
        <Button variant="filled">Export Report</Button>
      </Card>
    </div>
  );
};
