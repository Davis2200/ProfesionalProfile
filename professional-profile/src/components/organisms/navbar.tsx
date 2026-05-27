"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X } from "lucide-react";

export const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { name: "Proyectos", href: "/#proyectos" },
    { name: "Ciencia", href: "/ciencia" },
    { name: "Responsabilidad", href: "/about" },
  ];

  return (
    <nav className="fixed top-0 w-full z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-6 h-20 flex justify-between items-center text-brand-text">
        <div className="font-black tracking-tighter text-black">
          <Link href="/">
            DAVID<span className="text-brand-action">NAVA.</span>
          </Link>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:flex gap-10 text-[10px] font-black uppercase tracking-[0.25em] text-slate-400">
          {navLinks.map((link) => (
            <Link 
              key={link.name} 
              href={link.href} 
              className="hover:text-brand-action transition-colors"
            >
              {link.name}
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-4">
          <button className="hidden md:block text-[10px] font-black uppercase tracking-widest border-2 border-brand-text px-6 py-2 rounded-technical hover:bg-brand-text hover:text-white transition-all">
            Contacto
          </button>

          {/* Hamburger Toggle */}
          <button 
            className="md:hidden p-2 text-slate-600 focus:outline-none"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="md:hidden bg-white border-b border-slate-100 overflow-hidden"
          >
            <div className="flex flex-col p-6 gap-6 text-[10px] font-black uppercase tracking-[0.25em]">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setIsOpen(false)}
                  className="text-slate-400 hover:text-brand-action transition-colors"
                >
                  {link.name}
                </Link>
              ))}
              <button className="w-full text-[10px] font-black uppercase tracking-widest border-2 border-brand-text py-4 rounded-technical hover:bg-brand-text hover:text-white transition-all">
                Contacto
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};