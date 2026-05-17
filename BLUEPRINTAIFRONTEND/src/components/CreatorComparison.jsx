export default function CreatorComparison({ comparison }) {
  if (!comparison) {
    return (
      <div className="rounded-2xl border border-gray-200 bg-white p-6 text-gray-500">
        Creator comparison will appear here once creator data is added.
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-bold text-gray-900">Creator Comparison</h2>

      <p className="mt-2 text-gray-600">{comparison.summary}</p>

      {comparison.best_creator && (
        <div className="mt-4 rounded-xl bg-gray-50 p-4">
          <p className="text-sm text-gray-500">Top Creator</p>
          <p className="text-lg font-semibold text-gray-900">
            {comparison.best_creator.name} — Score:{" "}
            {comparison.best_creator.performance_score}/100
          </p>
        </div>
      )}

      <div className="mt-5 space-y-3">
        {comparison.creators?.map((creator, index) => (
          <div
            key={creator.id}
            className="flex items-center justify-between rounded-xl border border-gray-100 p-3"
          >
            <div>
              <p className="font-medium">
                #{index + 1} {creator.name}
              </p>
              <p className="text-sm text-gray-500">
                @{creator.tiktok_handle}
              </p>
            </div>

            <p className="font-semibold">
              {creator.performance_score}/100
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}