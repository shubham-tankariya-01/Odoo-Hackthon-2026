import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';

export const Layout = () => {
  return (
    <div className="flex h-screen bg-md-background overflow-hidden relative text-md-on-surface selection:bg-md-primary/20">
      {/* Decorative organic blur shapes (Material You signature) */}
      <div className="absolute top-[-10%] right-[-5%] w-[50vw] h-[50vw] rounded-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-md-secondary-container/40 to-transparent blur-3xl -z-10 opacity-70 pointer-events-none mix-blend-multiply" />
      <div className="absolute bottom-[-20%] left-[-10%] w-[60vw] h-[40vw] rounded-[100px] bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-md-tertiary/20 to-transparent blur-3xl -z-10 opacity-60 pointer-events-none mix-blend-multiply" />
      
      <Sidebar />
      
      <main className="flex-1 flex flex-col overflow-hidden h-full z-10 relative">
        <div className="flex-1 overflow-y-auto p-8 relative">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
