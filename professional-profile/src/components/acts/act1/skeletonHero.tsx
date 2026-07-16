export default function SkeletonHero() {
  return (
    <div className="min-h-[80vh] w-full flex items-center justify-center bg-[var(--color-fondo-tranquilo)] animate-pulse">
      <div className="space-y-6 w-full max-w-2xl px-4">
        <div className="h-16 bg-gray-200 rounded-2xl w-3/4 mx-auto" />
        <div className="h-16 bg-gray-200 rounded-2xl w-1/2 mx-auto" />
        <div className="h-4 bg-gray-200 rounded-full w-full" />
        <div className="h-12 bg-gray-200 rounded-full w-40 mx-auto mt-8" />
      </div>
    </div>
  );
}