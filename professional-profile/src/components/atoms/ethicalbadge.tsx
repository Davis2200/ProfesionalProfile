export const EthicalBadge = ({ label }: { label: string }) => (
  <span className="inline-flex items-center bg-brand-ethics/10 border border-brand-ethics/30 
                   text-brand-ethics px-3 py-1 rounded-full text-[10px] font-black 
                   uppercase tracking-widest leading-none">
    <span className="w-1.5 h-1.5 rounded-full bg-brand-ethics mr-2 animate-pulse" />
    {label}
  </span>
);