import React from 'react';
import { NavLink } from 'react-router-dom';
import { cn } from '../ui/Button';
import { 
  LayoutDashboard, 
  Building2, 
  Package, 
  ArrowRightLeft, 
  CalendarClock, 
  Wrench, 
  ClipboardCheck, 
  BarChart3, 
  Bell 
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Organization setup', href: '/organization', icon: Building2 },
  { name: 'Assets', href: '/assets', icon: Package },
  { name: 'Allocation & Transfer', href: '/transfers', icon: ArrowRightLeft },
  { name: 'Resource Booking', href: '/booking', icon: CalendarClock },
  { name: 'Maintenance', href: '/maintenance', icon: Wrench },
  { name: 'Audit', href: '/audit', icon: ClipboardCheck },
  { name: 'Reports', href: '/reports', icon: BarChart3 },
  { name: 'Notifications', href: '/notifications', icon: Bell },
];

export const Sidebar = () => {
  return (
    <div className="w-64 h-screen bg-md-surface-container flex flex-col pt-6 pb-4">
      <div className="px-6 mb-8">
        <h1 className="text-2xl font-bold text-md-on-surface tracking-tight">AssetFlow</h1>
      </div>
      
      <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) => cn(
              "flex items-center px-4 py-3 text-sm font-medium rounded-full transition-all duration-300 ease-md-emphasized group",
              isActive 
                ? "bg-md-primary text-md-on-primary shadow-sm" 
                : "text-md-on-surface hover:bg-md-on-surface/10 hover:text-md-on-surface active:bg-md-on-surface/20 active:scale-95"
            )}
          >
            <item.icon className={cn("mr-3 h-5 w-5", "group-hover:scale-110 transition-transform")} />
            {item.name}
          </NavLink>
        ))}
      </nav>
      
      <div className="px-6 mt-auto pt-6">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-full bg-md-tertiary text-white flex items-center justify-center font-bold">
            AF
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-medium">Admin User</span>
            <span className="text-xs text-md-on-surface-variant">admin@company.com</span>
          </div>
        </div>
      </div>
    </div>
  );
};
