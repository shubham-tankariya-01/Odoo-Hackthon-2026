import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const Organization = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Organization setup</h1>
          <p className="text-md-on-surface-variant mt-1 text-lg">(Admin only)</p>
        </div>
        <Button variant="filled">+ Add</Button>
      </div>

      <div className="flex bg-md-surface-container-low rounded-full p-1 max-w-md">
        <button className="flex-1 py-2 px-4 rounded-full bg-md-primary text-md-on-primary font-medium text-sm transition-colors">Departments</button>
        <button className="flex-1 py-2 px-4 rounded-full text-md-on-surface hover:bg-md-on-surface/5 font-medium text-sm transition-colors">Categories</button>
        <button className="flex-1 py-2 px-4 rounded-full text-md-on-surface hover:bg-md-on-surface/5 font-medium text-sm transition-colors">Employees</button>
      </div>

      <Card className="overflow-hidden p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-md-surface-container-low text-md-on-surface-variant text-sm border-b border-md-outline/10">
                <th className="py-4 px-6 font-medium">Department</th>
                <th className="py-4 px-6 font-medium">Head</th>
                <th className="py-4 px-6 font-medium">Parent Dept</th>
                <th className="py-4 px-6 font-medium text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-md-outline/10 text-md-on-surface">
              {[
                { name: 'Engineering', head: 'Aditi Sen', parent: '-', status: 'Active' },
                { name: 'Facilities', head: 'Rohan Mehta', parent: '-', status: 'Active' },
                { name: 'Field ops (East)', head: 'Samir Iqbal', parent: 'Field Ops', status: 'Inactive' },
              ].map((dept, i) => (
                <tr key={i} className="hover:bg-md-surface-container-low/50 transition-colors">
                  <td className="py-4 px-6 font-medium">{dept.name}</td>
                  <td className="py-4 px-6">{dept.head}</td>
                  <td className="py-4 px-6 text-md-on-surface-variant">{dept.parent}</td>
                  <td className="py-4 px-6 text-right">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                      dept.status === 'Active' 
                        ? 'border-green-500/30 text-green-700 bg-green-500/10' 
                        : 'border-md-outline/30 text-md-on-surface-variant bg-md-surface-container-low'
                    }`}>
                      {dept.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
      
      <p className="text-sm text-md-on-surface-variant italic mt-4 text-center">
        Deleting a department here also retires the abbbbl + 3 more...
      </p>
    </div>
  );
};
