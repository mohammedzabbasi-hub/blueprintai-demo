export default function CreativeFilters({
  search,
  setSearch,
  hookType,
  setHookType,
  creatorType,
  setCreatorType,
  hookOptions = [],
  creatorOptions = [],
}) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
      <input
        className="border rounded-xl px-3 py-2"
        placeholder="Search creatives..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <select
        className="border rounded-xl px-3 py-2"
        value={hookType}
        onChange={(e) => setHookType(e.target.value)}
      >
        <option value="">All hook types</option>
        {hookOptions.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>

      <select
        className="border rounded-xl px-3 py-2"
        value={creatorType}
        onChange={(e) => setCreatorType(e.target.value)}
      >
        <option value="">All creator types</option>
        {creatorOptions.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>
    </div>
  );
}
