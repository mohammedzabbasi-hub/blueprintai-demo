export function Button({ className = "", children, ...props }) {
  return (
    <button
      className={`inline-flex items-center justify-center rounded-xl px-4 py-2 border ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
