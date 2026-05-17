export default function CreatorStats({ creators = [] }) {
  const totalCreators = creators.length;

  const totalViews = creators.reduce(
    (sum, creator) => sum + Number(creator.total_views || 0),
    0,
  );

  const totalRevenue = creators.reduce(
    (sum, creator) => sum + Number(creator.total_revenue || 0),
    0,
  );

  const totalConversions = creators.reduce(
    (sum, creator) => sum + Number(creator.total_conversions || 0),
    0,
  );

  const bestCreator = [...creators].sort(
    (a, b) => Number(b.total_revenue || 0) - Number(a.total_revenue || 0),
  )[0];

  const stats = [
    { label: "Creators", value: totalCreators },
    { label: "Total Views", value: totalViews.toLocaleString() },
    { label: "Total Revenue", value: `$${totalRevenue.toLocaleString()}` },
    { label: "Conversions", value: totalConversions.toLocaleString() },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm"
        >
          <p className="text-sm text-gray-500">{stat.label}</p>
          <p className="mt-1 text-2xl font-bold text-gray-900">
            {stat.value}
          </p>
        </div>
      ))}

      {bestCreator && (
        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm md:col-span-4">
          <p className="text-sm text-gray-500">Best Revenue Creator</p>
          <p className="mt-1 text-xl font-bold text-gray-900">
            {bestCreator.name} — $
            {Number(bestCreator.total_revenue || 0).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
}