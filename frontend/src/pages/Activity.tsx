import React from 'react';
import { Card } from '../components/ui/Card';

export const Activity = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Activity logs & Notifications</h1>
      </div>

      <div className="flex bg-md-surface-container-low rounded-full p-1 max-w-[400px]">
        <button className="flex-1 py-2 px-4 rounded-full bg-md-primary text-md-on-primary font-medium text-sm shadow-sm transition-colors">All</button>
        <button className="flex-1 py-2 px-4 rounded-full text-md-on-surface hover:bg-md-on-surface/5 font-medium text-sm transition-colors">Alerts</button>
        <button className="flex-1 py-2 px-4 rounded-full text-md-on-surface hover:bg-md-on-surface/5 font-medium text-sm transition-colors">Approvals</button>
        <button className="flex-1 py-2 px-4 rounded-full text-md-on-surface hover:bg-md-on-surface/5 font-medium text-sm transition-colors">Bookings</button>
      </div>

      <Card className="p-0 overflow-hidden">
        <div className="divide-y divide-md-outline/10">
          {[
            { msg: 'Laptop AF-0124 assigned to Priya Shah', time: '10m ago', type: 'info', icon: '💻' },
            { msg: 'Maintenance request AF-0055 approved', time: '18m ago', type: 'success', icon: '✓' },
            { msg: 'Booking confirmed: Room 302 - 2:00 to 3:00 PM', time: '1h ago', type: 'info', icon: '📅' },
            { msg: 'Transfer approved: AF-0033 to Facilities dept', time: '3h ago', type: 'success', icon: '✓' },
            { msg: 'Overdue return: AF-0021 was due 3 days ago', time: '1d ago', type: 'alert', icon: '⚠' },
            { msg: 'Audit discrepancy flagged: AF-0044 damaged', time: '2d ago', type: 'alert', icon: '⚠' },
          ].map((log, i) => (
            <div key={i} className="flex items-center gap-4 p-4 hover:bg-md-surface-container-low/50 transition-colors group cursor-pointer">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-sm transition-transform group-hover:scale-110 ${
                log.type === 'info' ? 'bg-blue-100 text-blue-600' :
                log.type === 'success' ? 'bg-green-100 text-green-600' :
                'bg-amber-100 text-amber-600'
              }`}>
                {log.icon}
              </div>
              <div className="flex-1">
                <p className="font-medium text-md-on-surface group-hover:text-md-primary transition-colors">{log.msg}</p>
              </div>
              <div className="text-xs font-medium text-md-on-surface-variant whitespace-nowrap">
                {log.time}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
