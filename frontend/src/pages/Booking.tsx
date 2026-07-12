import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const Booking = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Resource Booking</h1>
      </div>

      <Card className="p-8">
        <div className="flex flex-col md:flex-row gap-6 mb-8">
          <div className="flex flex-col w-full md:w-1/2 relative">
            <label className="text-xs font-medium text-md-on-surface-variant mb-1 ml-4">Resource</label>
            <select className="h-14 px-4 bg-md-surface-container-low text-md-on-surface rounded-t-lg rounded-b-none border-b-2 border-md-outline focus:outline-none focus:border-md-primary transition-colors duration-200 font-medium">
              <option>Conference Room 3B - Floor 3, HQ</option>
            </select>
          </div>
          
          <div className="flex flex-col w-full md:w-1/2 relative">
            <label className="text-xs font-medium text-md-on-surface-variant mb-1 ml-4">Date</label>
            <input type="date" defaultValue="2026-07-12" className="h-14 px-4 bg-md-surface-container-low text-md-on-surface rounded-t-lg rounded-b-none border-b-2 border-md-outline focus:outline-none focus:border-md-primary transition-colors duration-200" />
          </div>
        </div>

        <div className="relative border-l-2 border-md-outline/20 ml-16 space-y-0 py-4">
          {/* Time markers */}
          {['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'].map((time) => (
            <div key={time} className="h-16 relative group">
              <div className="absolute -left-16 top-0 text-sm font-medium text-md-on-surface-variant w-12 text-right">{time}</div>
              <div className="absolute -left-2 top-2 w-3.5 h-3.5 rounded-full bg-md-surface-container border-2 border-md-outline/40 group-hover:border-md-primary transition-colors" />
              <div className="absolute left-0 top-2.5 w-full h-px bg-md-outline/10 border-dashed border-b group-hover:border-solid group-hover:bg-md-primary/20 transition-all" />
            </div>
          ))}

          {/* Bookings */}
          <div className="absolute top-[20px] left-6 right-6 h-[48px] bg-md-primary/10 border border-md-primary/30 rounded-lg p-3 shadow-sm hover:shadow-md hover:scale-[1.01] transition-all cursor-pointer group">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-md-primary rounded-l-lg" />
            <div className="flex justify-between items-center h-full">
              <span className="font-medium text-md-primary text-sm">Design Sync - 9:00 to 10:00 AM</span>
              <span className="text-xs font-bold bg-md-primary text-md-on-primary px-2 py-0.5 rounded-full">Priya Shah</span>
            </div>
          </div>
          
          <div className="absolute top-[180px] left-6 right-6 h-[96px] bg-red-500/10 border border-red-500/30 rounded-lg p-3 shadow-sm opacity-60 overflow-hidden group">
            <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 10px, #ef4444 10px, #ef4444 20px)' }} />
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500 rounded-l-lg" />
            <div className="relative flex justify-between items-start h-full">
              <span className="font-medium text-red-700 text-sm">Requested 11:30 to 13:00 - waitlist - slot is unavailable</span>
            </div>
          </div>
        </div>

        <div className="mt-10 flex justify-start">
          <Button variant="filled">Book a slot</Button>
        </div>
      </Card>
    </div>
  );
};
