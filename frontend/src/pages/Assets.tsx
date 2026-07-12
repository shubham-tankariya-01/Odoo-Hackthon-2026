import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

export const Assets = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Asset registrations and directory</h1>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-end">
        <div className="flex-1 w-full relative">
          <Input 
            placeholder="Search by tag, serial, or alt code..." 
            className="w-full pl-10 h-12 rounded-t-xl"
          />
          <div className="absolute left-4 top-3.5 text-md-on-surface-variant">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
        </div>
        
        <div className="flex gap-2 w-full sm:w-auto">
          <select className="h-12 px-4 rounded-xl bg-md-surface-container-low border border-transparent focus:border-md-primary focus:outline-none transition-colors text-md-on-surface-variant text-sm font-medium cursor-pointer">
            <option>Category</option>
          </select>
          <select className="h-12 px-4 rounded-xl bg-md-surface-container-low border border-transparent focus:border-md-primary focus:outline-none transition-colors text-md-on-surface-variant text-sm font-medium cursor-pointer">
            <option>Status</option>
          </select>
          <select className="h-12 px-4 rounded-xl bg-md-surface-container-low border border-transparent focus:border-md-primary focus:outline-none transition-colors text-md-on-surface-variant text-sm font-medium cursor-pointer">
            <option>Department</option>
          </select>
        </div>
        
        <Button variant="filled" className="h-12">+ Register Asset</Button>
      </div>

      <Card className="overflow-hidden p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-md-surface-container-low text-md-on-surface-variant text-sm border-b border-md-outline/10">
                <th className="py-4 px-6 font-medium">Tag</th>
                <th className="py-4 px-6 font-medium">Name</th>
                <th className="py-4 px-6 font-medium">Category</th>
                <th className="py-4 px-6 font-medium">Status</th>
                <th className="py-4 px-6 font-medium">Location</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-md-outline/10 text-md-on-surface">
              {[
                { tag: 'AF-0012', name: 'Dell Laptop', category: 'Electronics', status: 'Allocated', location: 'Bangalore' },
                { tag: 'AF-0042', name: 'Projector', category: 'Electronics', status: 'Maintenance', location: 'HQ Floor 2' },
                { tag: 'AF-0089', name: 'Office chair', category: 'Furniture', status: 'Available', location: 'Warehouse' },
              ].map((asset, i) => (
                <tr key={i} className="hover:bg-md-surface-container-low/50 transition-colors group cursor-pointer">
                  <td className="py-4 px-6 font-medium font-mono text-sm group-hover:text-md-primary transition-colors">{asset.tag}</td>
                  <td className="py-4 px-6 font-medium">{asset.name}</td>
                  <td className="py-4 px-6 text-md-on-surface-variant">{asset.category}</td>
                  <td className="py-4 px-6">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                      asset.status === 'Available' ? 'border-green-500/30 text-green-700 bg-green-500/10' :
                      asset.status === 'Allocated' ? 'border-blue-500/30 text-blue-700 bg-blue-500/10' :
                      'border-amber-500/30 text-amber-700 bg-amber-500/10'
                    }`}>
                      {asset.status}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-md-on-surface-variant">{asset.location}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
