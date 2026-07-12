import React from 'react';
import { Card } from '../components/ui/Card';

export const Maintenance = () => {
  const columns = [
    { title: 'Pending', count: 1, color: 'bg-md-surface-container-low', border: 'border-md-outline/20' },
    { title: 'Approved', count: 1, color: 'bg-blue-500/10', border: 'border-blue-500/20' },
    { title: 'Technician assigned', count: 1, color: 'bg-indigo-500/10', border: 'border-indigo-500/20' },
    { title: 'In progress', count: 1, color: 'bg-amber-500/10', border: 'border-amber-500/20' },
    { title: 'Resolved', count: 1, color: 'bg-green-500/10', border: 'border-green-500/20' },
  ];

  const cards = {
    'Pending': [{ tag: 'AF-0062', name: 'Projector bulb LCD burning out' }],
    'Approved': [{ tag: 'AF-0125', name: 'Dell laptop noisy compressor' }],
    'Technician assigned': [{ tag: 'AF-0098', name: 'Forklift brake pad issues' }],
    'In progress': [{ tag: 'AF-0192', name: 'Printer jam parts ordered' }],
    'Resolved': [{ tag: 'AF-0222', name: 'Office chair repair replaced 3 Jul', highlight: true }],
  };

  return (
    <div className="h-full flex flex-col space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Maintenance Management</h1>
          <p className="text-md-on-surface-variant mt-1 text-lg">(Approval workflow as kanban board)</p>
        </div>
      </div>

      <div className="flex-1 overflow-x-auto pb-4">
        <div className="flex gap-6 h-full min-w-max">
          {columns.map(col => (
            <div key={col.title} className={`w-80 rounded-3xl p-4 flex flex-col gap-4 ${col.color} border ${col.border}`}>
              <div className="flex justify-between items-center px-2">
                <h3 className="font-bold text-md-on-surface">{col.title}</h3>
                <span className="bg-white/50 text-md-on-surface-variant text-xs font-bold px-2.5 py-1 rounded-full">{col.count}</span>
              </div>
              
              <div className="flex-1 space-y-4">
                {cards[col.title as keyof typeof cards]?.map((card, i) => (
                  <Card key={i} elevated className={`p-5 cursor-pointer group ${card.highlight ? 'border-2 border-green-500/50 bg-green-50' : 'bg-md-surface'}`}>
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-xs font-bold text-md-primary font-mono">{card.tag}</span>
                    </div>
                    <p className="font-medium text-md-on-surface text-sm leading-snug group-hover:text-md-primary transition-colors">{card.name}</p>
                  </Card>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <p className="text-sm text-md-on-surface-variant italic text-center">
        Approving a card moves the asset to under maintenance, resolving returns it to available.
      </p>
    </div>
  );
};
