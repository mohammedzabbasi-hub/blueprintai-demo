export default function CreatorTable({ creators = [] }) {
  if (!creators.length) {
    return (
      <div className="rounded-2xl border border-gray-200 bg-white p-6 text-center text-gray-500">
        No creators added yet.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="bg-gray-50 text-gray-600">
          <tr>
            <th className="px-4 py-3">Creator</th>
            <th className="px-4 py-3">Followers</th>
            <th className="px-4 py-3">Videos</th>
            <th className="px-4 py-3">Views</th>
            <th className="px-4 py-3">Engagement</th>
            <th className="px-4 py-3">Conversions</th>
            <th className="px-4 py-3">Revenue</th>
          </tr>
        </thead>

        <tbody>
          {creators.map((creator) => {
            const engagement =
              Number(creator.total_likes || 0) +
              Number(creator.total_comments || 0) +
              Number(creator.total_shares || 0);

            return (
              <tr key={creator.id} className="border-t border-gray-100">
                <td className="px-4 py-3 font-medium">
                  {creator.name}
                  <span className="block text-xs text-gray-500">
                    @{creator.tiktok_handle}
                  </span>
                </td>
                <td className="px-4 py-3">
                  {Number(creator.follower_count || 0).toLocaleString()}
                </td>
                <td className="px-4 py-3">{creator.total_videos || 0}</td>
                <td className="px-4 py-3">
                  {Number(creator.total_views || 0).toLocaleString()}
                </td>
                <td className="px-4 py-3">{engagement.toLocaleString()}</td>
                <td className="px-4 py-3">
                  {Number(creator.total_conversions || 0).toLocaleString()}
                </td>
                <td className="px-4 py-3">
                  ${Number(creator.total_revenue || 0).toLocaleString()}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}