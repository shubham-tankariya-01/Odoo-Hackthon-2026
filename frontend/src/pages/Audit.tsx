import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const Audit = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Asset Audit</h1>
          <p className="text-md-on-surface-variant mt-1 text-lg">(Audit cycle, checklist, auto-generated discrepancy report)</p>
        </div>
      </div>

      <Card className="border border-md-outline/10 bg-md-surface-container-low p-6">
        <h3 className="font-bold text-lg">Q3 Audit: Engineering dept - 148 ppl</h3>
        <p className="text-md-on-surface-variant mt-1">Auditors: A. Desai, K. Rajpal</p>
      </Card>

      <Card className="p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-md-surface-container-low text-md-on-surface-variant text-sm border-b border-md-outline/10">
                <th className="py-4 px-6 font-medium">Asset</th>
                <th className="py-4 px-6 font-medium">Expected Location</th>
                <th className="py-4 px-6 font-medium text-right">Verification</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-md-outline/10 text-md-on-surface">
              {[
                { tag: 'AF-0012', name: 'Dell laptop', loc: 'Desk B12', status: 'Verified' },
                { tag: 'AF-0021', name: 'Office chair', loc: 'Desk B14', status: 'Missing' },
                { tag: 'AF-0044', name: 'Monitor', loc: 'Desk B13', status: 'Damaged' },
              ].map((asset, i) => (
                <tr key={i} className="hover:bg-md-surface-container-low/50 transition-colors">
                  <td className="py-4 px-6">
                    <span className="font-mono text-xs text-md-primary mr-2">{asset.tag}</span>
                    <span className="font-medium">{asset.name}</span>
                  </td>
                  <td className="py-4 px-6 text-md-on-surface-variant">{asset.loc}</td>
                  <td className="py-4 px-6 text-right">
                    <button className={`inline-flex items-center px-4 py-1.5 rounded-full text-xs font-bold transition-all hover:scale-105 active:scale-95 border ${
                      asset.status === 'Verified' ? 'border-green-500 text-green-700 bg-green-500/10' :
                      asset.status === 'Missing' ? 'border-red-500 text-red-700 bg-red-500/10' :
                      'border-amber-500 text-amber-700 bg-amber-500/10'
                    }`}>
                      {asset.status === 'Verified' && <span className="mr-1">✓</span>}
                      {asset.status === 'Missing' && <span className="mr-1">!</span>}
                      {asset.status === 'Damaged' && <span className="mr-1">⚠</span>}
                      {asset.status}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Card className="bg-amber-500/10 border border-amber-500/30 p-6 flex flex-col md:flex-row items-center justify-between gap-4 group hover:shadow-md hover:bg-amber-500/20 transition-all">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-700 font-bold text-xl shrink-0 group-hover:scale-110 transition-transform">⚠</div>
          <div>
            <h3 className="font-bold text-amber-900">2 assets flagged</h3>
            <p className="text-amber-800 text-sm">Discrepancy report generated automatically.</p>
          </div>
        </div>
        <Button variant="tonal" className="bg-amber-500/20 text-amber-900 hover:bg-amber-500/30">Close audit cycle</Button>
      </Card>
    </div>
  );
};
