import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export const Dashboard = () => {
  const overviewData = [
    { name: 'Available', value: 128, color: '#6750A4' }, // md-primary
    { name: 'Allocated', value: 35, color: '#7D5260' },  // md-tertiary
    { name: 'Maintenance', value: 8, color: '#d97706' }, // amber-600
    { name: 'Active Bookings', value: 4, color: '#2563eb' }, // blue-600
    { name: 'Pending Transfers', value: 3, color: '#9333ea' }, // purple-600
    { name: 'Upcoming Returns', value: 12, color: '#16a34a' }, // green-600
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-md-on-surface tracking-tight">Today's Overview</h1>
          <p className="text-md-on-surface-variant mt-1 text-lg">Welcome back, here's what's happening.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="tonal">Book resource</Button>
          <Button variant="filled">+ Register asset</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side: 6 Tiles */}
        <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {overviewData.map((stat, i) => (
            <Card key={i} className="flex flex-col group relative overflow-hidden p-5">
              <div 
                className="absolute -right-6 -top-6 w-24 h-24 rounded-full blur-2xl transition-colors duration-500 opacity-10 group-hover:opacity-20"
                style={{ backgroundColor: stat.color }}
              />
              <span className="text-md-on-surface-variant font-medium text-sm">{stat.name}</span>
              <span className="text-4xl font-bold mt-2" style={{ color: stat.color }}>{stat.value}</span>
            </Card>
          ))}
        </div>

        {/* Right Side: Pie Chart */}
        <Card className="lg:col-span-1 flex flex-col items-center justify-center min-h-[300px] p-4">
          <h3 className="font-bold text-md-on-surface mb-2 self-start px-4">Distribution</h3>
          <div className="w-full flex-1">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={overviewData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {overviewData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    borderRadius: '16px', 
                    border: 'none',
                    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
                    backgroundColor: '#F3EDF7',
                    color: '#1C1B1F',
                    fontWeight: '500'
                  }}
                  itemStyle={{ color: '#1C1B1F' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <Card className="bg-red-500/10 border border-red-500/20 flex items-center justify-between p-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-red-500/20 flex items-center justify-center text-red-600 font-bold">!</div>
          <div>
            <h3 className="font-bold text-red-900">3 assets overdue for return</h3>
            <p className="text-red-700 text-sm">Flagged for follow-up</p>
          </div>
        </div>
        <Button variant="outlined" className="text-red-700 border-red-700 hover:bg-red-700/10">View details</Button>
      </Card>

      <Card elevated className="mt-8">
        <h2 className="text-xl font-bold mb-6">Recent Activity</h2>
        <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-md-outline/20 before:to-transparent">
          {[
            { id: 1, title: 'Laptop AF-0124', desc: 'Allocated to Priya Shah - IT dept', time: '10m ago' },
            { id: 2, title: 'Room 302', desc: 'Booking confirmed - 2:00 to 3:00 PM', time: '1h ago' },
            { id: 3, title: 'Projector AF-0062', desc: 'Maintenance resolved', time: '2h ago' },
          ].map((activity) => (
            <div key={activity.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-md-surface-container bg-md-primary text-md-on-primary shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10" />
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-md-surface-container-low p-4 rounded-2xl shadow-sm border border-md-outline/5 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-bold text-md-on-surface">{activity.title}</h4>
                  <span className="text-xs text-md-on-surface-variant font-medium">{activity.time}</span>
                </div>
                <p className="text-sm text-md-on-surface-variant">{activity.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
